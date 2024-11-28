import os
from openai import OpenAI
import requests

os.environ["OPENAI_API_KEY"] = "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"

def gerar_imagem(descricao):
    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.images.generate(
            model="dall-e-3",
            prompt=descricao,
            n=1, 
            size="1024x1024" 
        )

        image_url = response.data[0].url
        print(f"Imagem gerada: {image_url}")
        return image_url

    except Exception as e:
        print(f"Erro ao gerar imagem: {e}")

def baixar_imagem(url, nome_arquivo="imagem.png"):
    response = requests.get(url)
    if response.status_code == 200:
        with open(nome_arquivo, "wb") as f:
            f.write(response.content)
        print(f"Imagem salva como {nome_arquivo}")
    else:
        print("Erro ao baixar a imagem.")

url_imagem = gerar_imagem("""Retrato vívido e melancólico, de ângulo alto, de uma mulher, em um planeta alienígena árido e azul, usando um traje de voo futurista preto e vermelho e um capacete totalmente fechado. Início da noite.""")
baixar_imagem(url_imagem)