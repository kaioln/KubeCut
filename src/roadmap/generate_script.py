from common.models.prompt_ai import generate_response

def create_script(prompt):
    system_prompt = "Você é um roteirista profissional especializado em vídeos educativos voltados para redes sociais como TikTok, Instagram e YouTube. Seu objetivo é criar roteiros claros, cativantes e organizados para a audiência jovem e adulta."
    response_ai = generate_response(prompt, system_prompt)
    segments = response_ai.split("\n\n") 
    return response_ai, segments