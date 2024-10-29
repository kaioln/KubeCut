import sys
import os
import logging
from datetime import datetime
import cv2
import moviepy.editor as mp
from pathlib import Path
import json
import subprocess
import shutil
import pysrt
import glob
import analise_video_ia
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from openai import OpenAI

# Carrega as variáveis do arquivo .env
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def load_config():
    """Carrega as configurações do arquivo JSON."""
    with open('config.json', 'r') as f:
        return json.load(f)

# Carregar as configurações
config = load_config()

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent

# Diretórios
SUBTITLE_DIR = BASE_DIR / config['directories']['subtitles']
CLIPS_DIR = BASE_DIR / config['directories']['clips']
FINAL_DIR = BASE_DIR / config['directories']['processed']
LOGS_DIR = BASE_DIR / config['directories']['logs']['dir']
VIDEOS_DIR = BASE_DIR / config['directories']['videos']
AUDIO_DIR = BASE_DIR / config['directories']['audio']
WORDS_DIR = BASE_DIR / config['directories']['prohibited_words']['dir']

# Parametros
max_words_per_segment = config['max_words_per_segment']
font_file = config['font_file']

# Configuração do logging
log_filename = LOGS_DIR / config['directories']['logs']['archive']
LOGS_DIR.mkdir(parents=True, exist_ok=True)
file_handler = logging.FileHandler(log_filename, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[file_handler])

def extract_audio(video_path, audio_output_path):
    """Extrai o áudio de um vídeo e salva em um arquivo temporário na pasta de áudio."""  
    logging.info(f"Extraindo áudio do vídeo: {video_path}")
    try:
        video = mp.VideoFileClip(str(video_path))
        audio = video.audio
        
        # Especificar o caminho de saída para o arquivo de áudio
        audio.write_audiofile(str(audio_output_path), codec='mp3')  # Salvar na pasta de áudio
        logging.info(f"Áudio extraído e salvo em: {audio_output_path}")
    except Exception as e:
        logging.error(f"Erro ao extrair áudio: {e}")
        raise

def format_time(seconds):
    """Converte tempo em segundos para o formato SRT (HH:MM:SS,mmm)."""
    millisec = int((seconds - int(seconds)) * 1000)
    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millisec:03}"

def generate_unique_id():
    """Gera um ID único baseado no timestamp."""    
    return datetime.now().strftime("%Y%m%d%H%M%S")
    
def save_subtitles(segments, output_dir, unique_id, video_name):
    """Salva os segmentos transcritos como arquivos SRT na pasta subtitles."""
    subtitles_subfolder = output_dir / f"{video_name}_{unique_id}"
    subtitles_subfolder.mkdir(parents=True, exist_ok=True)

    logging.info(f"Salvando legendas em: {subtitles_subfolder}")

    for i, segment in enumerate(segments):
        subtitle_filename = f"{video_name}_{unique_id}_{i + 1}.srt"
        subtitle_path = subtitles_subfolder / subtitle_filename

        logging.info(f"Salvando a transcrição como legenda em: {subtitle_path}")

        try:
            with open(subtitle_path, 'w', encoding='utf-8') as f:
                start_time = format_time(segment['start'])
                end_time = format_time(segment['end'])
                text = segment['text']

                f.write(f"1\n")  # ID do segmento
                f.write(f"{start_time} --> {end_time}\n") 
                f.write(f"{text.strip()}\n")  # Texto

            logging.info(f"Legenda salva com sucesso em: {subtitle_path}")
        except Exception as e:
            logging.error(f"Erro ao salvar a legenda: {e}")
            raise

    return subtitles_subfolder 

def add_subtitle(clip_path, srt_filename, font_size=18, 
                 font_color="16777215", border_color="0", border_width=2,
                 alignment=2):

    srt_temp_file = None  # Inicializa como None para garantir que exista
    try:
        # Verificar se os parâmetros não são None
        if not clip_path or not srt_filename or not font_file:
            raise ValueError("Parâmetros inválidos. clip_path, srt_filename e font_file não podem ser None.")
        
        # Verificar se o arquivo SRT e o vídeo existem
        if not os.path.exists(srt_filename):
            raise FileNotFoundError(f"Arquivo SRT não encontrado: {srt_filename}")
        
        if not os.path.exists(clip_path):
            raise FileNotFoundError(f"Arquivo de vídeo não encontrado: {clip_path}")
        
        subs = pysrt.open(srt_filename)
        srt_temp_file = 'temp_subtitles.srt'
        with open(srt_temp_file, 'w', encoding='utf-8') as f:
            for sub in subs:
                f.write(f"{sub.index}\n")
                start_time = f"{sub.start.hours:02}:{sub.start.minutes:02}:{sub.start.seconds:02},{sub.start.milliseconds:03}"
                end_time = f"{sub.end.hours:02}:{sub.end.minutes:02}:{sub.end.seconds:02},{sub.end.milliseconds:03}"
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{sub.text}\n\n")
        if clip_path is not None:
            temp_output_path = clip_path.replace('.mp4', '_temp.mp4')
        else:
            logging.error("O caminho do clipe é None.")
        temp_output_path = clip_path.replace('.mp4', '_temp.mp4')
        
        command = [
            'ffmpeg',
            '-y',
            '-loglevel', 'error',
            '-i', clip_path,
            '-r', '30',  # Taxa de quadros (padrão do ffmpeg é 25)
            '-vf', (
                f"subtitles={srt_temp_file}:"
                f"force_style='FontName={font_file},"
                f"FontSize={font_size},"
                f"PrimaryColour={font_color},"
                f"BorderStyle=1,"
                f"Outline={border_width},"
                f"OutlineColour={border_color},"
                f"Alignment={alignment}',"
                f"setpts=PTS/1.05,"
                f"eq=contrast=1.2:saturation=1.1"
            ),
            '-movflags', '+faststart',
            '-metadata', 'comment=Video processed for copyright camouflage',
            '-af', 'atempo=1.05',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-b:a', '192k',
            temp_output_path
        ]
        
        subprocess.call(command, shell=False)
        logging.info(f"Legenda adicionada com sucesso no vídeo '{clip_path}'. Arquivo de saída temporário: {temp_output_path}")
        
        shutil.move(temp_output_path, clip_path)
        logging.info(f"O arquivo temporário foi movido para substituir o original: {clip_path}")
        
    except ValueError as e:
        logging.error(f"Erro de valor: {e}")
    except FileNotFoundError as e:
        logging.error(e)
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao adicionar legenda: {e}")
    except Exception as e:
        logging.error(f"Ocorreu um erro: {e}")
    finally:
        if srt_temp_file and os.path.exists(srt_temp_file):
            os.remove(srt_temp_file)
            logging.info(f"Arquivo temporário {srt_temp_file} removido com sucesso.")

def adjust_focus(clip, platform):
    """Ajusta o foco e realiza o crop do vídeo mantendo as proporções e com foco em rostos."""
    
    # Dimensões da plataforma de destino
    platform_dimensions = {
        'instagram_feed': (1080, 1080),
        'instagram_reels': (1080, 1920),
        'tiktok': (1080, 1920),
        'youtube': (1920, 1080)
    }
    
    if platform not in platform_dimensions:
        raise ValueError(f"Plataforma {platform} não suportada. Escolha entre: {list(platform_dimensions.keys())}")

    target_width, target_height = platform_dimensions[platform]

    # Dimensões do vídeo original
    original_width, original_height = clip.size
    
    # Calcular a proporção do vídeo original e do destino
    original_ratio = original_width / original_height
    target_ratio = target_width / target_height

    # Detectar a face no primeiro frame
    frame = clip.get_frame(0)
    frame_cv = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Carregar o classificador de faces pré-treinado do OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detectar faces no frame
    gray = cv2.cvtColor(frame_cv, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        # Supondo que a primeira face detectada é a principal
        (x, y, w, h) = faces[0]
        center_x = x + w // 2
        center_y = y + h // 2
    else:
        # Se nenhuma face for detectada, manter o foco central
        center_x = original_width // 2
        center_y = original_height // 2

    # Aplicar o corte proporcional baseado na detecção de rosto
    if original_ratio > target_ratio:
        # Cortar horizontalmente (mais largo que o necessário)
        new_width = int(target_ratio * original_height)
        x1 = max(center_x - new_width // 2, 0)
        x2 = min(x1 + new_width, original_width)
        y1, y2 = 0, original_height
    else:
        # Cortar verticalmente (mais alto que o necessário)
        new_height = int(original_width / target_ratio)
        y1 = max(center_y - new_height // 2, 0)
        y2 = min(y1 + new_height, original_height)
        x1, x2 = 0, original_width

    # Aplicar o crop ao clipe
    cropped_clip = clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)

    # Redimensionar para as dimensões de destino
    resized_clip = cropped_clip.resize(newsize=(target_width, target_height))

    return resized_clip

def save_clips(video_paths, unique_id, video_name):
    """Salva os clipes selecionados de uma lista de vídeos em uma nova pasta, usando SRTs para nomeação e referência."""
    
    # Criar a pasta de clipes e legendas apenas uma vez, fora do loop
    clip_subfolder = CLIPS_DIR / f"{video_name}_{unique_id}" 
    clip_subfolder.mkdir(parents=True, exist_ok=True)

    subtitles_subfolder = SUBTITLE_DIR / f"{video_name}_{unique_id}"
    subtitles_subfolder.mkdir(parents=True, exist_ok=True)

    clips_saved = []

    # Iterar sobre a lista de vídeos
    for idx, video_path in enumerate(video_paths, start=1):
        srt_filename = subtitles_subfolder / f"{video_name}_{unique_id}_{idx:02d}.srt"  # Caminho SRT
        clip_filename = f"{video_name}_{unique_id}_{idx:02d}.mp4"  # Nome do clipe com índice
        clip_path = clip_subfolder / clip_filename

        try:
            video = mp.VideoFileClip(str(video_path))
            
            # Ajustar o foco no clipe
            focused_clip = adjust_focus(video, platform="tiktok")  # Define a plataforma aqui
            
            # Adicionar transições suaves
            focused_clip = focused_clip.fx(mp.vfx.fadein, duration=0.5).fx(mp.vfx.fadeout, duration=0.5)
            
            # Salvar o clipe com foco ajustado e transições
            focused_clip.write_videofile(str(clip_path))  # codec="libx264", audio_codec="aac"
            
            clips_saved.append(clip_path)

            # Gerar e adicionar legendas
            srt_filename = generate_srt_from_video(str(clip_path), srt_filename)
            add_subtitle(str(clip_path), srt_filename)
            logging.info(f"Clip salvo: {clip_path}")
        
        except Exception as e:
            logging.error(f"Erro ao salvar o clipe {clip_filename}: {e}")
    
    return clips_saved

def clean_up_audio_files():
    """Remove todos os arquivos de áudio após o término do processo, incluindo temporários."""
    logging.info("Removendo arquivos de áudio...")
    for audio_file in AUDIO_DIR.glob('*'):
        try:
            audio_file.unlink()
            logging.info(f"Arquivo de áudio removido: {audio_file}")
        except Exception as e:
            logging.error(f"Erro ao remover o arquivo de áudio {audio_file}: {e}")

def split_transcript_into_segments(segments):
    """Divide a transcrição em segmentos respeitando o tempo."""
    divided_segments = []

    for segment in segments:
        # Acessando os atributos diretamente, como objetos
        text = segment.text.strip()
        words = text.split()
        start_time = segment.start
        end_time = segment.end
        for i in range(0, len(words), max_words_per_segment):
            chunk_words = words[i:i + max_words_per_segment]
            chunk_text = ' '.join(chunk_words)

            chunk_start = start_time + (i / len(words)) * (end_time - start_time)
            chunk_end = start_time + ((i + len(chunk_words)) / len(words)) * (end_time - start_time)

            divided_segments.append({
                "start": chunk_start,
                "end": chunk_end,
                "text": chunk_text
            })

    return divided_segments

# Dicionário de palavras ofensivas e suas substituições
def load_prohibited_words(file_path):
    """Carrega palavras proibidas de um arquivo de texto e retorna um dicionário."""
    prohibited_words = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word, replacement = line.strip().split('=')
            prohibited_words[word] = replacement
    return prohibited_words

# Função para substituir palavras ofensivas com base no dicionário
def censor_text(text, prohibited_words):
    """Substitui palavras proibidas no texto de acordo com o dicionário."""
    for word, replacement in prohibited_words.items():
        text = text.replace(word, replacement)
    return text

def generate_srt(segments, srt_output_path):
    """Gera um arquivo SRT a partir de uma lista de segmentos, com filtro de palavras ofensivas."""
    prohibited_words_path = WORDS_DIR / config['directories']['prohibited_words']['archive']
    WORDS_DIR.mkdir(parents=True, exist_ok=True)
    prohibited_words = load_prohibited_words(prohibited_words_path)
    subs = pysrt.SubRipFile()

    for i, segment in enumerate(segments):
        start_time = pysrt.SubRipTime(seconds=segment['start'])
        end_time = pysrt.SubRipTime(seconds=segment['end'])

        # Substitui palavras ofensivas no texto do segmento
        text = censor_text(segment['text'], prohibited_words)
        
        sub = pysrt.SubRipItem(index=i + 1, start=start_time, end=end_time, text=text)
        subs.append(sub)
    
    # Salva o arquivo SRT
    subs.save(srt_output_path, encoding='utf-8')
    logging.info(f"Arquivo SRT salvo em: {srt_output_path}")
    return srt_output_path

def dividir_audio(audio_path, intervalo=10 * 60):
    """Divide o áudio em partes menores de 'intervalo' segundos."""
    audio = AudioSegment.from_file(audio_path)
    duracao = len(audio) // 1000  # duração em segundos
    partes = []

    for i in range(0, duracao, intervalo):
        inicio = i * 1000
        fim = min((i + intervalo) * 1000, len(audio))
        parte = audio[inicio:fim]
        parte_path = f"temp/audio_parte_{i // intervalo}.mp3"
        parte.export(parte_path, format="mp3")
        partes.append(parte_path)

    return partes

def transcrever_audio_partes(audio_partes):
    """Transcreve cada parte do áudio e retorna texto e segmentos."""
    transcricao_completa = ""
    todos_segmentos = []

    def transcrever(parte):
        with open(parte, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
            )
            return response.text, response.segments

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(transcrever, audio_partes)

    for transcricao_parcial, segmentos_parciais in results:
        transcricao_completa += transcricao_parcial + "\n"
        todos_segmentos.extend(segmentos_parciais)

    # Removendo os arquivos temporários de áudio após a transcrição
    for parte in audio_partes:
        if os.path.exists(parte):
            os.remove(parte)

    return transcricao_completa, todos_segmentos

def generate_srt_from_video(video_path, srt_output_path):
    """Gera um arquivo SRT a partir de um vídeo."""
    if video_path is not None:
        audio_output_path = video_path.replace('.mp4', '.mp3')
    else:
        logging.error("O caminho do vídeo é None.")
    audio_output_path = video_path.replace('.mp4', '.mp3')
    extract_audio(video_path, audio_output_path)

    audio_partes = dividir_audio(audio_output_path)
    transcricao, segmentos = transcrever_audio_partes(audio_partes)

    segments = split_transcript_into_segments(segmentos)
    srt_output_path = generate_srt(segments, srt_output_path)

    if os.path.exists(audio_output_path):
        os.remove(audio_output_path)

    return srt_output_path

def process_video(video_path):
    """Processa o vídeo completo, extraindo o áudio, transcrevendo, selecionando e salvando clipes."""  
    unique_id = generate_unique_id()  # Gera um ID único
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    try:
        selected_segments = analise_video_ia.processar_video_para_cortes(video_path)
        clips_saved = save_clips(selected_segments, unique_id, video_name)
        
        # Log resumido e final
        logging.info(f"Processamento concluído: {len(selected_segments)} segmentos escolhidos, {len(clips_saved)} clipes salvos.")
    
    except Exception as e:
        logging.error(f"Erro no processamento do vídeo: {e}")
    finally:
        clean_up_audio_files()

def clean_temp_archives(diretorio):
    padrao_temp = os.path.join(diretorio, '*TEMP*')
    arquivos_temp = glob.glob(padrao_temp)
    if arquivos_temp:
        for arquivo in arquivos_temp:
            # Verifica se é um arquivo (não uma pasta) antes de tentar remover
            if os.path.isfile(arquivo):
                try:
                    os.remove(arquivo)
                    print(f"Arquivo {arquivo} removido com sucesso.")
                except Exception as e:
                    print(f"Erro ao remover {arquivo}: {e}")
            else:
                print(f"{arquivo} é um diretório, não será removido.")
    else:
        print("Nenhum arquivo TEMP encontrado.")

if __name__ == "__main__":
    video_file_path = sys.argv[1]
    process_video(video_file_path)
    clean_temp_archives(BASE_DIR)