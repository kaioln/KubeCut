import re

def extract_narration(prompt_text):
    narration_lines = []
    
    # Regex para capturar o texto após "NARRADOR:" 
    narration_pattern = r"Narrador:\s(.*?)(?=\n|$)"
    
    matches = re.findall(narration_pattern, prompt_text, re.DOTALL)
    
    if matches:
        narration_lines.extend(matches)
    
    # Retorna as falas separadas por uma nova linha (ou customize como preferir)
    return "\n".join(narration_lines)

def extract_theme(prompt_text):
    theme_lines = []
    
    # Regex para capturar o texto após "TEMA:" 
    theme_pattern = r"Tema Trilha Sonora:\s(.*?)(?=\n|$)"
    
    matches = re.findall(theme_pattern, prompt_text, re.DOTALL)
    
    if matches:
        theme_lines.extend(matches)
    
    # Retorna as falas separadas por uma nova linha (ou customize como preferir)
    return "\n".join(theme_lines)
