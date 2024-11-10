from common.models.client_api import client
from common.models.logginlog import log_message

def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Imprimindo o conteúdo da resposta no terminal
    print("Sugestões do GPT-4:\n", response.choices[0].message.content)
    log_message("Sugestões do GPT-4 geradas!")
    
    return response.choices[0].message.content