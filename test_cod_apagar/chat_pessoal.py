import json
import os

# Inicializa ou carrega a memória
def carregar_memoria():
    """Carrega a memória do arquivo JSON se existir, ou inicializa uma nova memória."""
    if os.path.exists("memoria.json"):
        with open("memoria.json", "r") as file:
            return json.load(file)
    else:
        return {}

def salvar_memoria(memoria):
    """Salva a memória no arquivo JSON."""
    with open("memoria.json", "w") as file:
        json.dump(memoria, file, indent=4)

def atualizar_memoria(memoria, usuario, nova_informacao):
    """Atualiza a memória com novas informações fornecidas pelo usuário."""
    if usuario not in memoria:
        memoria[usuario] = []
    memoria[usuario].append(nova_informacao)
    salvar_memoria(memoria)

def obter_resposta_ia(pergunta, usuario, memoria):
    """Gera uma resposta da IA, usando memória, se aplicável."""
    # A IA verifica se há informações anteriores sobre o usuário na memória
    if usuario in memoria:
        historico = memoria[usuario]
        resposta = f"Lembro que você me disse: {historico[-1]}. Em que mais posso te ajudar?"
    else:
        resposta = "Olá! Parece que é a primeira vez que conversamos. Como posso te ajudar?"

    # Atualiza a memória com a nova interação
    atualizar_memoria(memoria, usuario, pergunta)
    return resposta

# Função principal do diálogo
def dialogo():
    memoria = carregar_memoria()  # Carrega a memória existente

    usuario = input("Qual é o seu nome? ")  # Pede o nome do usuário para identificá-lo
    while True:
        pergunta_usuario = input(f"{usuario}: ")
        if pergunta_usuario.lower() in ["sair", "não"]:
            print("Encerrando o diálogo.")
            break

        resposta = obter_resposta_ia(pergunta_usuario, usuario, memoria)
        print(f"IA: {resposta}")

if __name__ == "__main__":
    dialogo()
