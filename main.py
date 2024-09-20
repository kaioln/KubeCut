import sys
import moviepy.editor as mp
import whisper
import os
import logging
import re
from transformers import pipeline
from logging.handlers import RotatingFileHandler
import warnings
import language_tool_python
from spellchecker import SpellChecker

# Ignorar warnings
warnings.filterwarnings("ignore")

# Configuração do logging com rotação de arquivos
log_filename = "/mnt/c/Users/TI/Project/logs/process.log"
handler = RotatingFileHandler(log_filename, maxBytes=5 * 1024 * 1024, backupCount=5)  # 5MB por arquivo, até 5 backups
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[handler, logging.StreamHandler(sys.stdout)]
)

# Inicializa o LanguageTool para correção ortográfica e gramatical
language_tool = language_tool_python.LanguageTool('pt-BR')

# Inicializa o corretor ortográfico para português
spell = SpellChecker(language='pt')

def extract_audio(video_path: str, audio_output_path: str):
    if not os.path.isfile(video_path):
        logging.error(f"Arquivo de vídeo não encontrado: {video_path}")
        raise FileNotFoundError(f"Arquivo de vídeo não encontrado: {video_path}")
    
    try:
        logging.info(f"Extraindo áudio do vídeo: {video_path}")
        video = mp.VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_output_path)
        logging.info(f"Áudio extraído e salvo em: {audio_output_path}")
    except Exception as e:
        logging.error(f"Erro ao extrair áudio: {e}")
        raise

def transcribe_audio(audio_path: str):
    if not os.path.isfile(audio_path):
        logging.error(f"Arquivo de áudio não encontrado: {audio_path}")
        raise FileNotFoundError(f"Arquivo de áudio não encontrado: {audio_path}")

    try:
        logging.info(f"Iniciando a transcrição do áudio: {audio_path}")
        model = whisper.load_model("large")  # Usando o modelo 'large' para maior precisão
        result = model.transcribe(audio_path, verbose=True, language='pt')  # Especifica o idioma como Português
        logging.info("Transcrição concluída com sucesso")
        return result.get("segments", [])
    except Exception as e:
        logging.error(f"Erro ao transcrever o áudio: {e}")
        raise

def format_time(seconds: float) -> str:
    """Formata o tempo em horas:minutos:segundos,milissegundos para o formato SRT"""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"

def get_next_subtitle_number(output_dir: str, base_name: str) -> str:
    """Obtém o próximo número sequencial com dois dígitos para os arquivos de legendas"""
    if not os.path.isdir(output_dir):
        logging.error(f"Diretório de saída não encontrado: {output_dir}")
        raise NotADirectoryError(f"Diretório de saída não encontrado: {output_dir}")

    existing_files = [f for f in os.listdir(output_dir) if f.startswith(base_name) and f.endswith('.srt')]
    numbers = []

    for file in existing_files:
        try:
            number = int(file.split('_')[-1].split('.')[0])
            numbers.append(number)
        except ValueError:
            logging.warning(f"Nome de arquivo inválido: {file}. Ignorando.")
            continue

    next_number = max(numbers, default=0) + 1
    return f"{next_number:02}"

def corrigir_gramatica(texto: str) -> str:
    try:
        # Correção ortográfica usando SpellChecker
        palavras = texto.split()
        palavras_corrigidas = []
        for palavra in palavras:
            # Remove pontuação da palavra para correção
            palavra_limpia = re.sub(r'[^\w\s]', '', palavra)
            if palavra_limpia.lower() not in spell:
                correcoes = spell.candidates(palavra_limpia.lower())
                if correcoes:
                    # Seleciona a correção mais provável
                    palavra_corrigida = correcoes.pop()
                    # Mantém a capitalização original
                    if palavra.istitle():
                        palavra_corrigida = palavra_corrigida.capitalize()
                    else:
                        palavra_corrigida = palavra_corrigida
                    palavras_corrigidas.append(palavra_corrigida)
                else:
                    palavras_corrigidas.append(palavra)
            else:
                palavras_corrigidas.append(palavra)
        texto_corrigido = ' '.join(palavras_corrigidas)
        
        # Correção gramatical com LanguageTool
        matches = language_tool.check(texto_corrigido)
        texto_corrigido = language_tool_python.utils.correct(texto_corrigido, matches)
        return texto_corrigido
    except Exception as e:
        logging.error(f"Erro ao corrigir gramática: {e}")
        return texto

def corrigir_pontuacao(texto: str) -> str:
    # Adiciona espaço antes de pontuações que não possuem espaço
    texto = re.sub(r'(?<! )([,.!?])', r' \1', texto)
    # Substitui múltiplos espaços por um único
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

def dividir_frases(texto: str, limite: int = 100) -> str:
    # Divide o texto em frases com base em pontuação final
    frases = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', texto)
    frases_corrigidas = []

    for frase in frases:
        if len(frase) > limite:
            # Divide a frase com base em vírgulas ou ponto e vírgula
            frases_divididas = re.split(r'(?<=,|\;)', frase)
            frases_divididas = [f.strip() for f in frases_divididas if f.strip()]
            frases_corrigidas.extend(frases_divididas)
        else:
            frases_corrigidas.append(frase.strip())

    return ' '.join(frases_corrigidas)

def corrigir_legenda(texto: str) -> str:
    """Aplica correções ortográficas, gramaticais, de pontuação e divisão de frases"""
    texto = corrigir_gramatica(texto)    # Correção ortográfica e gramatical
    texto = corrigir_pontuacao(texto)    # Correção de pontuação
    texto = dividir_frases(texto)        # Divisão de frases longas
    return texto

def save_subtitles(segments: list, video_path: str, output_dir: str):
    if not segments:
        logging.warning("Nenhum segmento para salvar.")
        return None

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    subtitle_number = get_next_subtitle_number(output_dir, video_name)
    subtitle_filename = f"{video_name}_{subtitle_number}.srt"
    subtitle_path = os.path.join(output_dir, subtitle_filename)

    try:
        logging.info(f"Salvando a transcrição como legenda em: {subtitle_path}")
        with open(subtitle_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments):
                start_time = format_time(segment['start'])
                end_time = format_time(segment['end'])
                text = corrigir_legenda(segment['text'])

                f.write(f"{i + 1}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")

        logging.info(f"Legenda salva com sucesso em: {subtitle_path}")
        return subtitle_path
    except Exception as e:
        logging.error(f"Erro ao salvar a legenda: {e}")
        raise

def analyze_sentiment(text: str) -> tuple:
    model_name = 'distilbert-base-uncased-finetuned-sst-2-english'
    sentiment_analyzer = pipeline('sentiment-analysis', model=model_name)
    result = sentiment_analyzer(text)[0]
    return result['label'], result['score']

def select_best_segments(segments: list, min_sentiment_score: float) -> list:
    selected_segments = []

    for segment in segments:
        text = segment['text']
        label, score = analyze_sentiment(text)
        if score >= min_sentiment_score:
            segment['sentiment'] = label
            segment['sentiment_score'] = score
            selected_segments.append(segment)

    return selected_segments

def group_segments(segments: list, max_duration: int = 60) -> list:
    grouped_segments = []
    current_group = []
    current_duration = 0

    def is_cohesive(group: list) -> bool:
        return len(group) > 0

    for segment in segments:
        segment_duration = segment['end'] - segment['start']
        if current_duration + segment_duration > max_duration:
            if is_cohesive(current_group):
                grouped_segments.append(current_group)
            current_group = [segment]
            current_duration = segment_duration
        else:
            current_group.append(segment)
            current_duration += segment_duration

    if is_cohesive(current_group):
        grouped_segments.append(current_group)

    return grouped_segments

def save_cuts(groups: list, video_path: str, output_dir: str, suffix: str) -> str:
    if not groups:
        logging.warning("Nenhum grupo para salvar.")
        return None

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    subtitle_number = get_next_subtitle_number(output_dir, video_name)
    subtitle_filename = f"{video_name}_{subtitle_number}{suffix}.srt"
    subtitle_path = os.path.join(output_dir, subtitle_filename)

    try:
        logging.info(f"Salvando a legenda editada como: {subtitle_path}")
        with open(subtitle_path, 'w', encoding='utf-8') as f:
            for i, group in enumerate(groups):
                start_time = format_time(group[0]['start'])
                end_time = format_time(group[-1]['end'])

                texto_completo = " ".join([segment['text'] for segment in group])
                texto_corrigido = corrigir_legenda(texto_completo)

                f.write(f"{i + 1}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{texto_corrigido}\n\n")

        logging.info(f"Legenda editada salva com sucesso em: {subtitle_path}")
        return subtitle_path
    except Exception as e:
        logging.error(f"Erro ao salvar a legenda editada: {e}")
        raise

def transcribe_video(video_path: str, subtitle_output_dir: str, min_sentiment_score: float) -> str:
    try:
        audio_output_path = "temp_audio.wav"

        extract_audio(video_path, audio_output_path)
        segments = transcribe_audio(audio_output_path)
        best_segments = select_best_segments(segments, min_sentiment_score)
        grouped_segments = group_segments(best_segments, max_duration=60)
        cut_subtitle_path = save_cuts(grouped_segments, video_path, subtitle_output_dir, "Corte")

        logging.info(f"Processo de transcrição concluído com sucesso. Legenda editada salva em: {cut_subtitle_path}")
        return cut_subtitle_path
    except Exception as e:
        logging.error(f"Erro durante o processo de transcrição: {e}")
        raise
    finally:
        if os.path.exists(audio_output_path):
            os.remove(audio_output_path)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        logging.error("Uso incorreto. Deve ser: python3 main.py <video_path> <subtitle_output_dir> <min_sentiment_score>")
        print("Uso: python3 main.py <video_path> <subtitle_output_dir> <min_sentiment_score>")
        sys.exit(1)

    video_path = sys.argv[1]
    subtitle_output_dir = sys.argv[2]
    min_sentiment_score = float(sys.argv[3])

    try:
        cut_subtitle_path = transcribe_video(video_path, subtitle_output_dir, min_sentiment_score)
        print("Legenda editada salva em:", cut_subtitle_path)
    except Exception as e:
        logging.error(f"Falha ao processar o vídeo: {e}")
        print("Ocorreu um erro. Verifique o arquivo de log para mais detalhes.")
