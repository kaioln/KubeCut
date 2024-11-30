from pydub.generators import Sine

# Criar um som básico com uma nota musical (exemplo: Lá 440 Hz)
tone = Sine(440).to_audio_segment(duration=5000)  # 5 segundos

# Adicionar efeitos ou variações
tone_with_effect = tone.fade_in(1000).fade_out(1000)

# Salvar o áudio
tone_with_effect.export("background_music.mp3", format="mp3")
