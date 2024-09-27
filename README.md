` # Video Transcription and Subtitle Generation  Este projeto realiza a transcrição de vídeos, extrai segmentos com base na análise de sentimentos e salva essas informações em arquivos de legenda no formato SRT. Utiliza a biblioteca Whisper para transcrição e MoviePy para manipulação de vídeos.  ## Instalação das Dependências  Para instalar as dependências necessárias, use o seguinte comando:  ```bash  pip install -r requirements.txt   `

### Bibliotecas usadas:

*   **moviepy**: Para manipulação de arquivos de vídeo.
    
*   **whisper**: Para transcrição de áudio em texto.
    
*   **transformers**: Para análise de sentimentos.
    
*   **torch**: Para suporte ao modelo de aprendizado profundo do Whisper.
    
*   **logging**: Para registrar informações sobre o processo de execução.
    

Como usar
---------

### Executar o script:

O script principal pode ser executado a partir da linha de comando. A sintaxe é:

`chmod x+ start.sh ( para criar o comando )./start.sh   `

Estrutura do Código:
--------------------

*   **extract\_audio(video\_path, audio\_output\_path)**: Extrai o áudio de um vídeo e salva em um arquivo.
    
*   **transcribe\_audio(audio\_path)**: Transcreve o áudio usando o modelo Whisper.
    
*   **save\_subtitles(segments, video\_path, output\_dir)**: Salva os segmentos transcritos como um arquivo SRT.
    
*   **analyze\_sentiment(text)**: Analisa o sentimento de um texto.
    
*   **select\_best\_segments(segments, min\_sentiment\_score)**: Seleciona os melhores segmentos com base na análise de sentimentos.
    
*   **save\_cuts(segments, video\_path, output\_dir, suffix)**: Salva os grupos de segmentos como um arquivo SRT editado.
    
*   **transcribe\_video(video\_path, subtitle\_output\_dir, min\_sentiment\_score)**: Função principal que coordena a transcrição e o salvamento das legendas.
    

Logs:
-----

O projeto registra informações sobre cada etapa do processo em um arquivo de log localizado em /mnt/c/Users/TI/Project/logs/process.log.