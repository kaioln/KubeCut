# Video Transcription and Subtitle Generation

Este projeto realiza a transcrição de vídeos, extrai segmentos com base na análise de sentimentos e salva essas informações em arquivos de legenda no formato SRT. Utiliza a biblioteca Whisper para transcrição e MoviePy para manipulação de vídeos.

## Dependências

Certifique-se de ter as seguintes bibliotecas instaladas. Você pode instalar todas as dependências listadas no arquivo `requirements.txt` usando:

```bash
pip install -r requirements.txt
Bibliotecas usadas:
moviepy: Para manipulação de arquivos de vídeo.
whisper: Para transcrição de áudio em texto.
transformers: Para análise de sentimentos.
torch: Para suporte ao modelo de aprendizado profundo do Whisper.
logging: Para registrar informações sobre o processo de execução.
Como usar
Executar o script:

O script principal pode ser executado a partir da linha de comando. A sintaxe é:

bash
Copiar código
python3 main.py <video_path> <subtitle_output_dir> <min_sentiment_score>
<video_path>: O caminho para o vídeo que deseja transcrever.
<subtitle_output_dir>: O diretório onde as legendas devem ser salvas.
<min_sentiment_score>: O valor mínimo de pontuação de sentimento para considerar um segmento.
Estrutura do Código:

extract_audio(video_path, audio_output_path): Extrai o áudio de um vídeo e salva em um arquivo.
transcribe_audio(audio_path): Transcreve o áudio usando o modelo Whisper.
save_subtitles(segments, video_path, output_dir): Salva os segmentos transcritos como um arquivo SRT.
analyze_sentiment(text): Analisa o sentimento de um texto.
select_best_segments(segments, min_sentiment_score): Seleciona os melhores segmentos com base na análise de sentimentos.
save_cuts(segments, video_path, output_dir, suffix): Salva os grupos de segmentos como um arquivo SRT editado.
transcribe_video(video_path, subtitle_output_dir, min_sentiment_score): Função principal que coordena a transcrição e o salvamento das legendas.
Logs:

O projeto registra informações sobre cada etapa do processo em um arquivo de log localizado em /mnt/c/Users/TI/Project/logs/process.log.