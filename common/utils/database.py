from datetime import datetime
import mysql.connector
from common.models.logginlog import log_message
#from common.models.client_api import conn

def save_log(id_user, input_video, hashtag, summary):
    try:
        cursor = conn.cursor()

        # Comando SQL para inserir dados
        insert_query = """
        INSERT INTO logs (id_user, input_video, hashtag, summary, created_at)
        VALUES (%s, %s, %s, %s, NOW())
        """
        data = (id_user, input_video, hashtag, summary)

        # Executa o comando e salva no banco
        cursor.execute(insert_query, data)
        conn.commit()

        log_message("Registro inserido com sucesso.")
    except mysql.connector.Error as err:
        log_message(f"Erro ao inserir no banco de dados: {err}", level="ERROR")
    finally:
        # Fechar o cursor e a conexão, se estiverem abertos
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()
