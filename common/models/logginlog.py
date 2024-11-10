import os
import datetime
from common.models.configs import config, LOGS_DIR

def log_message(message, level="INFO"):
    """
    Função para registrar uma mensagem de log com um nível específico.
    Args:
        message (str): A mensagem de log.
        level (str): O nível de log, como "INFO", "WARNING", "ERROR", etc.
    """
    log_dir = os.path.join(LOGS_DIR, config['directories']['logs']['archive'])
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]

    # Garante que o diretório de log exista
    os.makedirs(os.path.dirname(log_dir), exist_ok=True)

    # Escreve a mensagem de log no arquivo
    with open(log_dir, 'a') as log_file:
        log_file.write(f"{timestamp} - {level} - {message}\n")
    
    # Opcional: Exibe a mensagem no console também
    print(f"{timestamp} - {level} - {message}")
