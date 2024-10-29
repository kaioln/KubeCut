import os
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pydub import AudioSegment
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor
import re
import subprocess
from dotenv import load_dotenv
from openai import OpenAI

# Carrega as variáveis do arquivo .env
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Certificar-se de que a pasta "temp" existe
if not os.path.exists("temp"):
    os.makedirs("temp")

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

def gerar_srt(segments, srt_path="temp/transcricao.srt"):
    """Gera um arquivo SRT a partir dos segmentos do Whisper."""
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments):
            inicio = str(timedelta(seconds=int(segment.start)))
            fim = str(timedelta(seconds=int(segment.end)))
            texto = segment.text.strip()

            f.write(f"{i + 1}\n")
            f.write(f"{inicio} --> {fim}\n")
            f.write(f"{texto}\n\n")

    print(f"SRT gerado em: {srt_path}")

def transcrever_video(video_path):
    """Extrai o áudio do vídeo e faz a transcrição completa."""
    print("Extraindo áudio do vídeo...")
    audio_path = "temp/audio_temp.mp3"
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, codec="mp3", bitrate="192k", ffmpeg_params=["-ar", "44100"])

    print("Dividindo áudio em partes menores...")
    audio_partes = dividir_audio(audio_path)
    os.remove(audio_path)  # Remove o áudio completo para economizar espaço

    print("Iniciando transcrição...")
    transcricao, segmentos = transcrever_audio_partes(audio_partes)

    # Gera o SRT a partir dos segmentos
    # gerar_srt(segmentos)

    return transcricao

def analisar_transcricao(transcricao):
    """Envia a transcrição completa para o GPT-4 para sugerir cortes de forma mais resumida."""
    prompt = f"""
    Abaixo está a transcrição de um vídeo. Analise e divida os trechos em duas categorias: 
    pontos relevantes e pontos irrelevantes. 
    Crie uma síntese objetiva dos principais momentos do vídeo para cada corte, 
    com 10 variações de 2 a 3 minutos cada, que transmitam a ideia central e um fluxo coerente.

    Cada corte deve ter:

    Pontos relevantes: momentos importantes, com marcação de minutos e segundos.
    Pontos irrelevantes: trechos que podem ser ignorados, com marcação de minutos e segundos.
    Um resumo com no máximo 255 caracteres.
    Cinco hashtags relevantes ao conteúdo.
    Um score de viralização entre 0 e 10, indicando o potencial de engajamento.

    {transcricao}

    Sugira apenas os trechos que contêm os momentos mais importantes, em minutos e segundos.
    Formato de saída (OBS.: Não alterar este modelo de saída!):

    Pontos relevantes:

    De 00:01 a 03:00: Discussão sobre investimento
    De 06:00 a 08:00: Conclusão financeira
    Pontos irrelevantes:

    De 00:00 a 00:40: Introdução irrelevante
    De 03:40 a 04:45: Comentários pessoais
    Hashtags: #investimento #finanças #sucesso #crescimento #dinheiro Resumo: Foco nas melhores estratégias de investimento e no crescimento financeiro. Score: 8.5

    Repita o formato acima para os 10 cortes, garantindo que cada vídeo mantenha um sentido lógico e apresente variações de momentos importantes para atender diferentes enfoques.

    Formato de resposta: incorreta (NÃO ME TRAGA RESPOSTAS NESSE FORMATO ABAIXO!!!!):
    - De 20:40 ao final: Abordagens iniciais

    Indique quais minutos são irrelevantes e podem ser ignorados.
    ALERTA: A precisão dos minutos e segundos é crucial para a extração dos cortes.
    """

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Imprimindo o conteúdo da resposta no terminal
    print("Sugestões do GPT-4:\n", response.choices[0].message.content)
    
    return response.choices[0].message.content

def converter_tempo(tempo):
    """Converte o tempo em 'hh:mm:ss' para segundos."""
    partes = list(map(int, tempo.split(':')))
    if len(partes) == 3:
        horas, minutos, segundos = partes
    elif len(partes) == 2:  # Caso o tempo esteja em formato 'mm:ss'
        horas = 0
        minutos, segundos = partes
    else:
        raise ValueError(f"Formato de tempo inválido: {tempo}")
    
    return horas * 3600 + minutos * 60 + segundos

def juntar_videos(cortes):
    """Junta os vídeos especificados na lista 'cortes' em um ou mais vídeos concatenados."""

    cortes = list(dict.fromkeys(cortes))  # Remove duplicatas

    if not cortes:
        print("Nenhum corte para juntar.")
        return

    # Criar um arquivo temporário para a lista de arquivos
    file_list_path = "temp/file_list.txt"
    with open(file_list_path, "w") as f:
        for corte in cortes:
            f.write(f"file '{os.path.abspath(corte)}'\n")

    # Lista para os caminhos dos vídeos de saída
    video_output_paths = ["temp/video_final_1.mp4"]

    # Executar o comando FFmpeg para cada arquivo de saída
    for video_output_path in video_output_paths:
        try:
            command = [
                "ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                "-i", file_list_path,
                "-vf", "fps=60", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", video_output_path
            ]
            subprocess.call(command, shell=False)
            print(f"Vídeo final {video_output_path} criado com sucesso!")
        except Exception as e:
            print(f"Erro ao criar o vídeo final {video_output_path}: {e}")
        # finally:
        #     if os.path.exists(file_list_path):
        #         os.remove(file_list_path)

    return video_output_paths
  

def extrair_tempo(linha):
    # Usar regex para capturar os tempos no formato hh:mm ou mm:ss
    match = re.findall(r'\d{2}:\d{2}(?::\d{2})?', linha)
    
    if len(match) == 2:
        inicio = match[0]
        fim = match[1]
        return inicio, fim
    else:
        raise ValueError(f"Formato de tempo inválido: {linha}")

def extrair_trechos_relevantes(sugestoes):
    """Extrai os trechos relevantes da sugestão do GPT-4."""
    trechos_relevantes = []
    continuar = False  # Flag para identificar se estamos nos trechos relevantes
    
    for linha in sugestoes.split("\n"):
        if "Pontos relevantes:" in linha:
            continuar = True
        elif "Pontos irrelevantes:" in linha:
            continuar = False
        elif continuar and "-" in linha:
            # Extrai o trecho relevante com base no formato
            inicio, fim = extrair_tempo(linha)
            trechos_relevantes.append((inicio, fim))
    
    return trechos_relevantes

def extrair_cortes(video_path, sugestoes):
    """Extrai cortes do vídeo original com base nos trechos relevantes sugeridos pelo GPT-4."""
    cortes = []
    trechos_relevantes = extrair_trechos_relevantes(sugestoes)
    
    for inicio, fim in trechos_relevantes:
        try:
            inicio_seg = converter_tempo(inicio)
            fim_seg = converter_tempo(fim)
            
            # Calcula a duração do corte
            duracao_corte = fim_seg - inicio_seg
            if duracao_corte < 10:
                print(f"Corte de {inicio} a {fim} é menor que 10 segundos e será ignorado.")
                continue

            output_video = f"temp/corte_{len(cortes) + 1}.mp4"
            ffmpeg_extract_subclip(video_path, inicio_seg, fim_seg, targetname=output_video)

            if os.path.exists(output_video) and os.path.getsize(output_video) > 0:
                cortes.append(output_video)
            else:
                print(f"Arquivo de corte {output_video} não foi gerado corretamente.")
        except Exception as e:
            print(f"Erro ao processar o trecho {inicio} a {fim}: {e}")
            continue

    return cortes

# Código principal que usa as funções acima
def processar_video_para_cortes(video_path):
    """Processa o vídeo e gera cortes sugeridos pelo GPT-4."""
    print("Transcrevendo o vídeo...")
    transcricao = transcrever_video(video_path)

    print("Analisando transcrição para gerar sugestões de cortes...")
    sugestoes = analisar_transcricao(transcricao)

    print("Extraindo cortes com base nas sugestões de trechos relevantes...")
    cortes = extrair_cortes(video_path, sugestoes)

    print("Juntando cortes em um único vídeo final...")
    video_final = juntar_videos(cortes)

    print("Processo completo!")

    return video_final
