## jKpCutPro
---------

## Descrição
---------

Este projeto é responsável por transcrever vídeos, extrair áudio, analisar sentimentos e criar cortes com base nos melhores segmentos do conteúdo, salvando as legendas e os vídeos cortados de forma organizada. O sistema utiliza modelos de aprendizado de máquina para análises detalhadas, oferecendo uma experiência de edição eficiente.

## Estrutura do Projeto
--------------------

*   main.py: Script principal para transcrição e edição de vídeos.
    
*   start.sh: Script para iniciar o processo.
    
*   subtitles/: Pasta onde as legendas transcritas serão salvas.
    
*   clips/: Pasta onde os vídeos cortados serão salvos.
    
*   logs/: Pasta onde os logs do processo serão armazenados.
    
*   videos/: Pasta onde os vídeos a serem processados devem ser colocados.
    
*   config.json: Arquivo de configuração para modelos e parâmetros de processamento.
    

## Funções
-------

### load\_config()

Carrega as configurações do arquivo JSON.

### ensure\_directories\_exist()

Garante que as pastas necessárias existam antes de configurar o logging.

### clean\_text(text)

Remove caracteres especiais e limpa o texto.

### extract\_audio(video\_path, audio\_output\_path)

Extrai o áudio de um vídeo e salva em um arquivo.

### transcribe\_audio(audio\_path)

Transcreve o áudio utilizando o modelo Whisper.

### format\_time(seconds)

Formata o tempo em segundos para o formato SRT.

### generate\_unique\_id()

Gera um ID único baseado no timestamp.

### save\_subtitles(segments, video\_path, output\_dir, unique\_id)

Salva os segmentos transcritos como um arquivo SRT com ID único.

### analyze\_sentiment(text: str)

Analisa o sentimento de um texto e retorna o rótulo e o score.

### extract\_topics(segments, num\_topics=5, num\_keywords=10)

Extrai tópicos dos segmentos transcritos utilizando o LDA (Latent Dirichlet Allocation).

### select\_best\_segments(segments: list, min\_sentiment\_score: float, max\_segments: int = 5, min\_duration: int = 60, max\_duration: int = 90) -> list

Seleciona os melhores segmentos com base na análise de sentimentos e duração, garantindo cortes fluidos.

### combine\_segments(selected\_segments, min\_duration, max\_duration, max\_segments)

Combina segmentos adjacentes em cortes válidos.

### create\_combined\_segment(current\_segment, start\_time)

Cria um segmento combinado a partir de segmentos atuais.

### save\_cuts(segments, video\_path, output\_dir, unique\_id)

Salva os grupos de segmentos como arquivos SRT editados e salva os vídeos cortados em ordem e organizados.

### main(video\_path)

Função principal que orquestra a extração, transcrição, análise e corte de vídeo.

Como Usar
---------

1.  Coloque os vídeos que deseja processar na pasta videos/.
    
2.  Altere os caminhos no arquivo start.sh e no começo do main.py.
    
3.  Crie o comando chmod +x start.sh para tornar o script executável.
    
4.  Execute o script usando ./start.sh no terminal.
    
5.  As legendas e os vídeos cortados serão salvos nas pastas subtitles/ e clips/, respectivamente.
    
6.  Os logs do processo podem ser encontrados na pasta logs/.
    

Caminhos
--------
`O caminho para o vídeo que você deseja processar.`
`O diretório onde as legendas e cortes serão salvos.`
`O valor mínimo do score de sentimento para considerar um segmento.`

## Logs
----

`Os logs do processo serão salvos no arquivo logs/process.log, onde você pode verificar detalhes sobre a execução e possíveis erros.`