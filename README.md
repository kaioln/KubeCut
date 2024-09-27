## jKpCutPro


## Descrição
Este projeto é responsável por transcrever vídeos, extrair áudio, analisar sentimentos e criar cortes com base nos melhores segmentos do conteúdo, salvando as legendas e os vídeos cortados de forma organizada.


## Estrutura do Projeto
- `main.py`: Script principal para transcrição e edição de vídeos.
- `start.sh`: Script para iniciar o processo.
- `subtitles/`: Pasta onde as legendas transcritas serão salvas.
- `videos/`: Pasta onde os vídeos a serem processados devem ser colocados.
- `clips/`: Pasta onde os vídeos cortados serão salvos.
- `logs/`: Pasta onde os logs do processo serão armazenados.


## Funções


### `clean_text(text)`
Remove caracteres especiais e limpa o texto.


### `extract_audio(video_path, audio_output_path)`
Extrai o áudio de um vídeo e salva em um arquivo.


### `transcribe_audio(audio_path)`
Transcreve o áudio utilizando o modelo Whisper.


### `format_time(seconds)`
Formata o tempo em segundos para o formato SRT.


### `get_next_subtitle_number(output_dir, base_name)`
Obtém o próximo número de legenda disponível para salvar.


### `save_subtitles(segments, video_path, output_dir)`
Salva os segmentos transcritos como um arquivo SRT.


### `analyze_sentiment(text: str)`
Analisa o sentimento de um texto e retorna o rótulo e o score.


### `select_best_segments(segments: list, min_sentiment_score: float, max_segments: int = 5, min_duration: int = 60, max_duration: int = 90) -> list`
Seleciona os melhores segmentos com base na análise de sentimentos e duração, garantindo cortes fluidos.


### `combine_segments(selected_segments, min_duration, max_duration, max_segments)`
Combina segmentos adjacentes em cortes válidos.


### `create_combined_segment(current_segment, start_time)`
Cria um segmento combinado a partir de segmentos atuais.


### `save_cuts(segments, video_path, output_dir, suffix)`
Salva os grupos de segmentos como um arquivo SRT editado e salva os vídeos cortados em ordem e organizados.


### `transcribe_video(video_path, subtitle_output_dir, min_sentiment_score)`
Transcreve o vídeo e salva as legendas editadas com os melhores segmentos, cortando o vídeo de acordo com os timings gerados.


## Como Usar
1. Coloque os vídeos que deseja processar na pasta `videos/`.
2. Altere os caminhos no arquivo `start.sh` e no começo do `main.py`.
3. Crie o comando `./start.sh` usando o código: `chmod +x start.sh`
4. Execute o script usando `./start.sh` no terminal.
5. As legendas e os vídeos cortados serão salvos nas pastas `subtitles/` e `clips/`, respectivamente.
. Os logs do processo podem ser encontrados na pasta `logs/`.


## Caminhos
```bash

<caminho_do_video>: O caminho para o vídeo que você deseja processar.
<caminho_do_output>: O diretório onde as legendas e cortes serão salvos.
<ponto_de_corte>: O valor mínimo do score de sentimento para considerar um segmento.

Logs
Os logs do processo serão salvos no arquivo logs/process.log, onde você pode verificar detalhes sobre a execução e possíveis erros.

