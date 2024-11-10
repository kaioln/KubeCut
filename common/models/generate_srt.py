import os
import pysrt
from common.models.configs import config, WORDS_DIR
from common.models.logginlog import log_message
from common.models.transcrible_audio import transcrible_audio

max_words_per_segment = config['max_words_per_segment']

def load_prohibited_words(file_path):
    """Carrega palavras proibidas de um arquivo de texto e retorna um dicionário."""
    prohibited_words = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word, replacement = line.strip().split('=')
            prohibited_words[word] = replacement
    return prohibited_words

def censor_text(text, prohibited_words):
    """Substitui palavras proibidas no texto de acordo com o dicionário."""
    for word, replacement in prohibited_words.items():
        text = text.replace(word, replacement)
    return text

def generate_srt(segments, srt_output_path):
    """Gera um arquivo SRT a partir de uma lista de segmentos, com filtro de palavras ofensivas."""
    prohibited_words_path = os.path.join(WORDS_DIR, config['directories']['prohibited_words']['archive'])

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
    log_message(f"Arquivo SRT salvo em: {srt_output_path}", level="INFO")
    return srt_output_path

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

def generate_srt_from_video(video_path, srt_output_path):
    """Gera um arquivo SRT a partir de um vídeo."""

    transcricao, segmentos = transcrible_audio(video_path)

    segments = split_transcript_into_segments(segmentos)
    srt_output_path = generate_srt(segments, srt_output_path)

    return srt_output_path
