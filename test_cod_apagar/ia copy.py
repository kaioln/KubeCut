import os
from pydub import AudioSegment
from openai import OpenAI

# Define sua chave da API diretamente aqui ou como uma variável de ambiente
os.environ["OPENAI_API_KEY"] = "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"

# Inicializa o cliente OpenAI com a chave da API
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def transcrever_audio(arquivo_audio):
    """Transcreve o áudio de um arquivo para texto."""
    # Converte o arquivo de áudio para o formato suportado
    audio = AudioSegment.from_mp3(arquivo_audio)
    audio.export("temp.wav", format="wav")  # Exporta como WAV para transcrição

    # Transcrição do áudio usando Whisper
    with open("temp.wav", "rb") as file:
        transcricao = client.audio.transcriptions.create(
            model="whisper-1",
            file=file,
        )
    return transcricao.text

def resumir_texto(texto):
    """Resume o texto usando a API da OpenAI."""
    response = client.chat.completions.create(
        model="gpt-4",  # Ou "gpt-4" se você tiver acesso
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": f"Resuma o seguinte texto: {texto}"}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

def main():
    caminho_arquivo_audio = "audio.mp3"  # Caminho para seu arquivo de áudio
    print("Transcrevendo o áudio...")
    texto_transcrito = transcrever_audio(caminho_arquivo_audio)
    print("Texto transcrito:", texto_transcrito)

    print("Resumindo o texto...")
    resumo = resumir_texto(texto_transcrito)
    print("Resumo do texto:", resumo)

if __name__ == "__main__":
    main()
