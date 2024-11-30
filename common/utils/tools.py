from datetime import datetime
import re

def generate_unique_id():
    """Gera um ID único baseado no timestamp."""    
    return datetime.now().strftime("%Y%m%d%H%M%S")

def format_time(seconds):
    """Converte tempo em segundos para o formato SRT (HH:MM:SS,mmm)."""
    millisec = int((seconds - int(seconds)) * 1000)
    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millisec:03}"

def sanitize_prompt(text):
    text = re.sub(r'[^\w\s,.]', '', text)  # Remove caracteres especiais, exceto pontuação básica
    text = text.strip()
    return text