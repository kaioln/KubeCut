from common.models.text_to_speech import text_to_audio
from common.utils.tools import generate_unique_id
from common.models.generate_bg_music import select_background_music
from src.roadmap import generate_script, video_creator, image_generation

def main():
    tema = "lyudmila pavlichenko"
    base_prompt = f"""
    Você é um roteirista profissional especializado em vídeos educativos voltados para redes sociais como TikTok, Instagram e YouTube. Seu objetivo é criar roteiros claros, cativantes e organizados para a audiência jovem e adulta, interessada em {tema}.

    Instruções para o roteiro:
    Público-alvo: Considere uma audiência que busca aprender de forma rápida, dinâmica e envolvente. Use uma linguagem simples, empática e próxima, mantendo um tom educativo e motivador.

    Tema: Aborde o tema {tema} de forma clara e objetiva. Certifique-se de delimitar bem o escopo, para que o vídeo seja curto, direto e impactante.

    Objetivo: O vídeo deve ensinar um conceito, inspirar, esclarecer dúvidas ou proporcionar informação valiosa.

    Pesquisa e confiabilidade: Garanta que as informações sejam confiáveis, usando dados relevantes e curiosidades que gerem engajamento.

    Estrutura do roteiro:

    Abertura (gancho): Comece com uma frase impactante ou uma pergunta provocativa que chame atenção imediatamente.
    Desenvolvimento: Explique o tema de forma lógica e linear, com exemplos, analogias ou curiosidades. Divida o conteúdo em partes claras.
    Recursos visuais: Sugira momentos para incluir imagens, gráficos ou animações que ajudem na compreensão.
    Encerramento: Finalize com uma mensagem motivadora ou uma chamada para ação, como curtir, comentar, ou compartilhar.
    Duração: Adapte o conteúdo para um vídeo com duração de 3 minuto. Mantenha um ritmo dinâmico e envolvente.

    Com base nas informações acima, gere um roteiro completo com título, introdução, desenvolvimento e fechamento. O texto deve ser otimizado para a plataforma escolhida e garantir que a audiência fique engajada até o final."
    
    Obedeça o formato:

    Tema Trilha Sonora: [UMA PALAVRA ENTRE (CALMO, INSPIRACAO, MELANCOLOSO, SUSPENSE)] 

    [CENA 1]

    [(prompt para imagem da cena)]

    Narrador: [NARRAÇÃO]

    [CENA 2]
    
"""
    
    script, segments = generate_script.create_script(base_prompt)
    
    audio_path = text_to_audio(script, "output_audio")
    
    image_paths = image_generation.create_images(segments)

    unique_id = generate_unique_id()

    background_music_path = select_background_music(script)

    video_creator.create_video(image_paths, audio_path, unique_id, background_music_path)

if __name__ == "__main__":
    main()
