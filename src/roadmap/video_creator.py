import os
from pathlib import Path
from common.models.configs import SUBTITLE_DIR, CLIPS_DIR
from common.models.logginlog import log_message
from common.models.subtitle import add_subtitle
from common.models.generate_srt import generate_srt_from_video
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.fx.all import audio_loop
from moviepy.video.fx.all import fadein, fadeout

def create_video(image_paths, audio_output_path, unique_id, background_music_path, output_path="output.mp4"):
    audio = None  # Inicializar a variável `audio` para evitar erros
    clips = []  # Inicializar `clips` como uma lista vazia
    duration_per_image = 5  # Duração de cada imagem em segundos
    try:
        if not audio_output_path or not isinstance(audio_output_path, str):
            raise ValueError(f"O parâmetro 'audio_output_path' deve ser uma string válida. Recebido: {audio_output_path}")
        if not os.path.exists(audio_output_path):
            raise FileNotFoundError(f"Arquivo de áudio não encontrado: {audio_output_path}")

        
        video_name = os.path.splitext(os.path.basename(output_path))[0]

        clip_subfolder = Path(CLIPS_DIR) / f"{video_name}_{unique_id}"
        clip_subfolder.mkdir(parents=True, exist_ok=True)

        subtitles_subfolder = Path(SUBTITLE_DIR) / f"{video_name}_{unique_id}"
        subtitles_subfolder.mkdir(parents=True, exist_ok=True)

        srt_filename = os.path.join(subtitles_subfolder, f"{video_name}_{unique_id}.srt")  # Caminho SRT
        clip_filename = f"{video_name}_{unique_id}.mp4"  # Nome do clipe com índice
        clip_path = os.path.join(clip_subfolder, clip_filename)

        # Verificar se os arquivos de imagem existem
        for image_path in image_paths:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {image_path}")
            
            if not image_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValueError(f"Formato inválido de arquivo: {image_path}")
            
            # Cria o clipe de imagem, com duração de 5 segundos por imagem (ajustar conforme necessário)
            img_clip = ImageClip(image_path, duration=duration_per_image)
            # Adiciona animações (exemplo: zoom in)
            img_clip = img_clip.fx(lambda c: c.resize(lambda t: 1 + 0.02 * t))  # Zoom in progressivo

            # Adiciona fade-in e fade-out
            img_clip = fadeout(img_clip, 1)
            # img_clip = fadein(img_clip, 1).fadeout(1)

            clips.append(img_clip)
        
        # Verificar se o áudio existe
        if not os.path.exists(audio_output_path):
            raise FileNotFoundError(f"Arquivo de áudio não encontrado: {audio_output_path}")
        
        # Carregar o áudio
        audio = AudioFileClip(audio_output_path)
        
        # Carregar música de fundo
        background_music = AudioFileClip(background_music_path).volumex(0.2)  # Reduz o volume para 20%
        
        # Calcular a duração total do vídeo com base no áudio
        video_duration = audio.duration

        if background_music.duration < video_duration:
            # Se a música de fundo for mais curta que o vídeo, repete para cobrir toda a duração
            background_music = audio_loop(background_music, duration=video_duration)
        else:
            # Se a música de fundo for mais longa, corta para a duração do vídeo
            background_music = background_music.subclip(0, video_duration)
        
        # Ajustar a duração das imagens para se alinhar com o áudio
        clips = [clip.set_duration(video_duration / len(clips)) for clip in clips]  # Distribui o tempo igualmente
        
        # Concatenar todos os clipes de imagem
        final_clip = concatenate_videoclips(clips, method="compose")
        
        # Definir o áudio para o vídeo
        final_audio = CompositeAudioClip([audio, background_music])
        final_clip = final_clip.set_audio(final_audio)
        
        # Salvar o vídeo final
        final_clip.write_videofile(str(clip_path), fps=24, codec="libx264", audio_codec="aac")

        # Gerar e adicionar legendas
        log_message("Gerando arquivo de transcrição.")
        srt_filename = generate_srt_from_video(clip_path, srt_filename)
        log_message("Carregando legendas...")
        add_subtitle(clip_path, srt_filename)
        log_message(f"Clip salvo: {clip_path}", level="INFO")

    except Exception as e:
        log_message(f"Erro durante a criação do vídeo: {str(e)}", level="ERROR")
        raise
    finally:
        # Liberar recursos se foram inicializados
        if audio:
            audio.close()
        # Fechar clipes apenas se a lista não estiver vazia
        if clips:
            for clip in clips:
                if hasattr(clip, 'close'):
                    clip.close()
