import os
from pathlib import Path
import subprocess
import shutil
import pysrt
from common.utils.tools import format_time
from common.models.logginlog import log_message
from common.models.configs import config

font_file = config['font_file']

def save_subtitles(segments, output_dir, unique_id, video_name):
    """Salva os segmentos transcritos como arquivos SRT na pasta subtitles."""
    subtitles_subfolder = Path(output_dir) / f"{video_name}_{unique_id}"
    subtitles_subfolder.mkdir(parents=True, exist_ok=True)

    log_message(f"Salvando legendas em: {subtitles_subfolder}", level="INFO")

    for i, segment in enumerate(segments):
        subtitle_filename = f"{video_name}_{unique_id}_{i + 1}.srt"
        subtitle_path = os.path.join(subtitles_subfolder, subtitle_filename)

        log_message(f"Salvando a transcrição como legenda em: {subtitle_path}", level="INFO")

        try:
            with open(subtitle_path, 'w', encoding='utf-8') as f:
                start_time = format_time(segment['start'])
                end_time = format_time(segment['end'])
                text = segment['text']

                f.write(f"1\n")  # ID do segmento
                f.write(f"{start_time} --> {end_time}\n") 
                f.write(f"{text.strip()}\n")  # Texto

            log_message(f"Legenda salva com sucesso em: {subtitle_path}", level="INFO")
        except Exception as e:
            log_message(f"Erro ao salvar a legenda: {e}", level="ERROR")
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
            log_message("O caminho do clipe é None.", level="ERROR")
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
        log_message(f"Legenda adicionada com sucesso no vídeo '{clip_path}'. Arquivo de saída temporário: {temp_output_path}", level="INFO")
        
        shutil.move(temp_output_path, clip_path)
        log_message(f"O arquivo temporário foi movido para substituir o original: {clip_path}", level="INFO")
        
    except ValueError as e:
        log_message(f"Erro de valor: {e}", level="ERROR")
    except FileNotFoundError as e:
        log_message(e)
    except subprocess.CalledProcessError as e:
        log_message(f"Erro ao adicionar legenda: {e}", level="ERROR")
    except Exception as e:
        log_message(f"Ocorreu um erro: {e}", level="ERRIR")
    finally:
        if srt_temp_file and os.path.exists(srt_temp_file):
            os.remove(srt_temp_file)
            log_message(f"Arquivo temporário {srt_temp_file} removido com sucesso.", level="INFO")
