import sys
import os
import moviepy.editor as mp
from pathlib import Path
from src.editor import analysis
from common.models.configs import SUBTITLE_DIR, CLIPS_DIR
from common.models.logginlog import log_message
from common.models.subtitle import add_subtitle
from common.models.video_editor import adjust_focus
from common.models.generate_srt import generate_srt_from_video
from common.utils.tools import generate_unique_id

def save_clips(video_paths, unique_id, video_name):
    """Salva os clipes selecionados de uma lista de vídeos em uma nova pasta, usando SRTs para nomeação e referência."""
    # Criar a pasta de clipes e legendas apenas uma vez, fora do loop
    clip_subfolder = Path(CLIPS_DIR) / f"{video_name}_{unique_id}"
    clip_subfolder.mkdir(parents=True, exist_ok=True)

    subtitles_subfolder = Path(SUBTITLE_DIR) / f"{video_name}_{unique_id}"
    subtitles_subfolder.mkdir(parents=True, exist_ok=True)

    clips_saved = []

    # Iterar sobre a lista de vídeos
    for idx, video_path in enumerate(video_paths, start=1):

        srt_filename = os.path.join(subtitles_subfolder, f"{video_name}_{unique_id}_{idx:02d}.srt")  # Caminho SRT
        clip_filename = f"{video_name}_{unique_id}_{idx:02d}.mp4"  # Nome do clipe com índice
        clip_path = os.path.join(clip_subfolder, clip_filename)

        try:
            video = mp.VideoFileClip(str(video_path))
            
            # Ajustar o foco no clipe
            focused_clip = adjust_focus(video)  # Define a plataforma aqui
            
            # Adicionar transições suaves
            focused_clip = focused_clip.fx(mp.vfx.fadein, duration=0.5).fx(mp.vfx.fadeout, duration=0.5)
            
            # Salvar o clipe com foco ajustado e transições
            focused_clip.write_videofile(str(clip_path))  # codec="libx264", audio_codec="aac"
            
            clips_saved.append(clip_path)

            # Gerar e adicionar legendas
            log_message("Gerando arquivo de transcrição.")
            srt_filename = generate_srt_from_video(clip_path, srt_filename)
            log_message("Carregando legendas...")
            add_subtitle(clip_path, srt_filename)
            log_message(f"Clip salvo: {clip_path}", level="INFO")
        
        except Exception as e:
            log_message(f"Erro ao salvar o clipe {clip_filename}: {e}", level="ERROR")
    
    return clips_saved

def process_video(video_path):
    """Processa o vídeo completo, extraindo o áudio, transcrevendo, selecionando e salvando clipes."""  
    unique_id = generate_unique_id()  # Gera um ID único
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    try:
        selected_segments = analysis.processar_video_para_cortes(video_path)
        clips_saved = save_clips(selected_segments, unique_id, video_name)
        
        # Log resumido e final
        log_message(f"Processamento concluído: {len(selected_segments)} segmentos escolhidos, {len(clips_saved)} clipes salvos.", level="INFO")
    
    except Exception as e:
        log_message(f"Erro no processamento do vídeo: {e}", level="ERROR")

if __name__ == "__main__":
    video_file_path = sys.argv[1]
    process_video(video_file_path)