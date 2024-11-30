from common.models.text_to_speech import text_to_audio

text = "fiquei sabendo que o zezo rasgou o wistler e agora ta chorando no grupo, e o trezentos so ficou vendo."
filename = "audio_exemplo"

audio_path = text_to_audio(text, filename)
if audio_path:
    print(f"Áudio gerado e salvo em: {audio_path}")