import os
import moviepy.editor as mp
import re
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from common.models.transcrible_audio import transcrible_audio
from common.models.configs import TEMP_DIR
from common.models.logginlog import log_message
from common.models.prompt_ai import generate_response

def analisar_transcricao(transcricao):
    """Envia a transcrição completa para o GPT-4 para sugerir cortes de forma mais resumida."""
    prompt = f"""
    Abaixo está a transcrição de um vídeo. Analise e divida os trechos em duas categorias: 
    Pontos relevantes e Pontos irrelevantes. 
    Crie uma síntese objetiva dos principais momentos do vídeo para cada corte, 
    com variações de 2 a 3 minutos cada, que transmitam a ideia central e um fluxo coerente.

    {transcricao}

    Cada corte deve ter:
    Pontos relevantes: momentos importantes, com marcação de minutos e segundos.
    Pontos irrelevantes: trechos que podem ser ignorados, com marcação de minutos e segundos.
    
    Gere uma lista de hashtags que maximize o engajamento e sejam viralizáveis nas redes sociais, especialmente no TikTok, Instagram e YouTube. As hashtags devem:

    1- Ser relevantes para o conteúdo e refletir as tendências mais populares da plataforma.
    2- Atrair público-alvo interessado no tema.
    3- Utilizar termos e frases de alto engajamento para que a publicação alcance maior visibilidade.
    4- Incluir hashtags de tendências atuais e gerais que ampliem o alcance, mas ainda tenham relação direta com o tema do conteúdo.
    5- Me forneça uma lista com cerca de 5 hashtags.

    Um resumo com no máximo 255 caracteres.
    Um score de viralização entre 0 e 10, indicando o potencial de engajamento, para as plataformas de tiktok, shorts, reels.

    Sugira apenas os trechos que contêm os momentos mais importantes, em minutos e segundos.
    Formato de saída (OBS.: Não alterar este modelo de saída!):
    ---
    *Corte 4:*
    Pontos relevantes:
    - De 00:01 a 03:00: Discussão sobre investimento
    Pontos irrelevantes:
    - De 00:00 a 00:40: Introdução irrelevante
    Hashtags:
    #investimento #finanças #sucesso #crescimento #dinheiro 
    Resumo: 
    Foco nas melhores estratégias de investimento e no crescimento financeiro.
    Score:
    8.5
    ---

    Repita o formato acima para os 10 cortes, garantindo que cada vídeo mantenha um sentido lógico e apresente variações de momentos importantes para atender diferentes enfoques.

    Formato de resposta: incorreta (NÃO ME TRAGA RESPOSTAS NESSE FORMATO ABAIXO!!!!):
    - De 20:40 ao final: Abordagens iniciais

    Indique quais minutos são irrelevantes e podem ser ignorados.
    ALERTA: A precisão dos minutos e segundos é crucial para a extração dos cortes. Extraia apenas 1 ponto de cada com seu tempo total.
    """
    response_ai = generate_response(prompt)

    return response_ai

def converter_tempo(tempo):
    """Converte o tempo em 'hh:mm:ss' para segundos."""
    partes = list(map(int, tempo.split(':')))
    if len(partes) == 3:
        horas, minutos, segundos = partes
    elif len(partes) == 2:  # Caso o tempo esteja em formato 'mm:ss'
        horas = 0
        minutos, segundos = partes
    else:
        raise ValueError(f"Formato de tempo inválido: {tempo}")
    
    return horas * 3600 + minutos * 60 + segundos

def extrair_tempo(linha):
    # Usar regex para capturar os tempos no formato hh:mm ou mm:ss
    match = re.findall(r'\d{2}:\d{2}(?::\d{2})?', linha)

    if len(match) == 1 and any(termo in linha.lower() for termo in ["ao final", "ao fim", "até o fim", "no final", "até o final", "no fim"]):
        # Retorna o início e um indicador de que é até o final
        return match[0], None
    elif len(match) == 2:
        inicio = match[0]
        fim = match[1]
        return inicio, fim
    else:
        raise ValueError(f"Formato de tempo inválido: {linha}")

def extrair_trechos_relevantes(sugestoes):
    """Extrai e agrupa trechos relevantes contínuos da sugestão do GPT-4."""
    trechos_relevantes = []
    continuar = False
    inicio_atual, fim_atual = None, None

    for linha in sugestoes.split("\n"):
        if "Pontos relevantes:" in linha:
            continuar = True
        elif "Pontos irrelevantes:" in linha:
            continuar = False
        elif continuar and "-" in linha:
            inicio, fim = extrair_tempo(linha)

            # Agrupar trechos contínuos
            if fim_atual and converter_tempo(inicio) == converter_tempo(fim_atual):
                fim_atual = fim  # Extende o fim do trecho atual
            else:
                if inicio_atual and fim_atual:  
                    trechos_relevantes.append((inicio_atual, fim_atual))
                inicio_atual, fim_atual = inicio, fim  # Inicia um novo trecho

    if inicio_atual and fim_atual:
        trechos_relevantes.append((inicio_atual, fim_atual))  # Adiciona o último trecho

    return trechos_relevantes
    #return trechos_relevantes[:10]

def extrair_cortes(video_path, sugestoes):
    """Extrai cortes do vídeo original com base nos trechos relevantes sugeridos pelo GPT-4."""
    cortes = []
    trechos_relevantes = extrair_trechos_relevantes(sugestoes)
    
    # Carrega o vídeo para obter a duração
    video = mp.VideoFileClip(video_path)
    duracao_total = int(video.duration)
    
    # Para garantir que cada sugestão gere um único vídeo
    trechos_unicos = list(dict.fromkeys(trechos_relevantes))  # Remove duplicatas

    for inicio, fim in trechos_unicos:
        try:
            inicio_seg = converter_tempo(inicio)
            fim_seg = converter_tempo(fim) if fim is not None else duracao_total
            
            # Calcula a duração do corte
            duracao_corte = fim_seg - inicio_seg
            if duracao_corte < 10:
                log_message(f"Corte de {inicio} a {fim} é menor que 10 segundos e será ignorado.", level="WARNING")
                continue
 
            output_video = os.path.join(TEMP_DIR, f'corte_{len(cortes) + 1}.mp4')
            ffmpeg_extract_subclip(video_path, inicio_seg, fim_seg, targetname=output_video)

            if os.path.exists(output_video) and os.path.getsize(output_video) > 0:
                cortes.append(output_video)
            else:
                log_message(f"Arquivo de corte {output_video} não foi gerado corretamente.", level="ERROR")
        except Exception as e:
            log_message(f"Erro ao processar o trecho {inicio} a {fim}: {e}", level="ERROR")
            continue

    video.close()  # Fecha o vídeo após o processamento

    if not cortes:
        log_message("Nenhum corte para retornar.", level="ERROR")
        return []

    log_message(f"Lista de caminhos dos cortes: {cortes}", level="INFO")
    return cortes

# Código principal que usa as funções acima
def processar_video_para_cortes(video_path):
    """Processa o vídeo e gera cortes sugeridos pelo GPT-4, com detalhes de resumo, hashtags e score."""
    log_message("Transcrevendo o vídeo...", level="INFO")
    transcricao = transcrible_audio(video_path)

    log_message("Analisando transcrição para gerar sugestões de cortes...", level="INFO")
    sugestoes = analisar_transcricao(transcricao)

    # Extrair e exibir resumo, hashtags e score para cada corte usar depois
    print("Detalhes de resumo, hashtags e score dos vídeos:")
    for i, corte in enumerate(sugestoes.split("---")[1:], start=1):  # [1:11] Limita a 10 cortes
        resumo = re.search(r"Resumo:\s*(.+)", corte)
        hashtags = re.search(r"Hashtags:\s*(.+)", corte)
        score = re.search(r"Score:\s*(.+)", corte)
        
        if resumo and hashtags and score:
            print(f"\nCorte {i}:")
            print("Resumo:", resumo.group(1).strip())
            print("Hashtags:", hashtags.group(1).strip())
            print("Score:", score.group(1).strip())
    
    log_message("Extraindo cortes com base nas sugestões de trechos relevantes...", level="INFO")
    video_final = extrair_cortes(video_path, sugestoes)

    log_message("Processo completo!", level="INFO")
    return video_final
