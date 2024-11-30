import os
from common.models.configs import AUDIO_DIR
from common.models.client_api import client
from common.utils.extract_excerpt import extract_narration

def text_to_audio(text, filename):
    try:
        # Extrair apenas o texto narrado
        narration_text = extract_narration(text)
        if not narration_text:
            print("Nenhuma narração encontrada no texto!")
            return None
        
        # Caminho para salvar o arquivo de áudio
        output_path = os.path.join(AUDIO_DIR, f'{filename}.mp3')
        
        # Gerando o áudio usando a API da OpenAI
        with client.audio.speech.with_streaming_response.create(
            model="tts-1-hd",  # Modelo TTS da OpenAI
            voice="onyx",  # Escolha a voz desejada
            input=narration_text  # Texto a ser convertido em fala
        ) as response:
            # Salvando o áudio gerado no arquivo
            with open(output_path, "wb") as f:
                for chunk in response.iter_bytes(chunk_size=1024):
                    f.write(chunk)
        
        print(f"Áudio salvo em: {output_path}")
        return output_path

    except Exception as e:
        print(f"Erro ao gerar áudio: {e}")
        return None
