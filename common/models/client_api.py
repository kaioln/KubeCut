import os
#import mysql.connector
from dotenv import load_dotenv
from openai import OpenAI
from common.models.configs import BASE_DIR

# Carrega variáveis de ambiente do arquivo .env
dotenv_path = os.path.join(BASE_DIR, 'config', '.env')
load_dotenv(dotenv_path)

# Configuração do cliente OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Configuração do YouTube
yt_key = os.getenv('YOUTUBE_API_KEY')

# configurar banco
# conn = mysql.connector.connect(
#         host=os.getenv("DB_HOST"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         database=os.getenv("DB_NAME")
#     )