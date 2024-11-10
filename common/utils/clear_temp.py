import os
import glob
from common.models.logginlog import log_message

def clean_temp_archives(diretorio):
    """
    Limpa todos os arquivos e diretórios dentro do diretório TEMP especificado.
    Args:
        diretorio (str): Caminho para o diretório TEMP que será limpo.
    """
    # Obtém todos os arquivos e pastas dentro do diretório TEMP
    arquivos_temp = glob.glob(os.path.join(diretorio, '*'))
    
    if arquivos_temp:
        for item in arquivos_temp:
            try:
                # Remove arquivos ou pastas
                if os.path.isfile(item):
                    os.remove(item)
                    log_message(f"Arquivo {item} removido com sucesso.", level="INFO")
                elif os.path.isdir(item):
                    os.rmdir(item)  # Remove o diretório vazio
                    log_message(f"Diretório {item} removido com sucesso.", level="INFO")
            except Exception as e:
                log_message(f"Erro ao remover {item}: {e}", level="ERROR")
    else:
        log_message("Nenhum arquivo ou diretório encontrado para limpar.", level="WARNING")
