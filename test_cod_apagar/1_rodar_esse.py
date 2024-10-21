import whisper
from moviepy.editor import VideoFileClip
import os

def extract_audio_from_video1(video_path, audio_path):
    """Extrai o áudio de um vídeo e salva como um arquivo WAV."""
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
        print(f"Áudio extraído e salvo em: {audio_path}")
    except Exception as e:
        print(f"Erro ao extrair áudio: {e}")

def transcribe_audio_whisper1(audio_path):
    """Transcreve o áudio usando Whisper."""
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result['text']

def split_transcript_into_segments1(transcript, max_words_per_segment=5):
    """Divide a transcrição em segmentos de 4 a 5 palavras."""
    words = transcript.split()
    segments = []
    for i in range(0, len(words), max_words_per_segment):
        segment = ' '.join(words[i:i + max_words_per_segment])
        segments.append(segment)
    return segments

def format_time1(seconds):
    """Formata o tempo no estilo SRT (hh:mm:ss,milliseconds)."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"

def generate_srt1(segments, output_srt_path, duration_per_segment=3):
    """Gera um arquivo SRT com os segmentos fornecidos."""
    with open(output_srt_path, 'w', encoding='utf-8') as srt_file:
        for i, segment in enumerate(segments):
            start_time = i * duration_per_segment
            end_time = start_time + duration_per_segment
            srt_file.write(f"{i + 1}\n")
            srt_file.write(f"{format_time1(start_time)} --> {format_time1(end_time)}\n")
            srt_file.write(f"{segment}\n\n")

    print(f"SRT gerado em: {output_srt_path}")

def generate_srt_from_video1(video_path, srt_output_path, max_words_per_segment=5):
    """Gera um arquivo SRT a partir de um vídeo."""
    # Caminho temporário para o áudio extraído
    audio_path = video_path.replace('.mp4', '.wav')
    
    # Extraí o áudio do vídeo
    extract_audio_from_video1(video_path, audio_path)
    
    # Transcreve o áudio usando Whisper
    transcript = transcribe_audio_whisper1(audio_path)
    
    # Divide a transcrição em segmentos de 4 a 5 palavras
    segments = split_transcript_into_segments1(transcript, max_words_per_segment)
    
    # Gera o arquivo SRT
    generate_srt1(segments, srt_output_path)

    # Remove o arquivo de áudio temporário
    if os.path.exists(audio_path):
        os.remove(audio_path)

# Exemplo de uso
video_path = 'teste.mp4'
srt_output_path = 'teste.srt'
generate_srt_from_video1(video_path, srt_output_path)
