import os
import requests
from common.utils.tools import sanitize_prompt
from common.models.generate_img import generate_images
from common.models.configs import IMAGES_DIR

def download_image(url, save_path):
    """Faz o download da imagem de uma URL e salva no caminho especificado."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Verifica se houve erro no download
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):  # Baixa em pedaços
                f.write(chunk)
        print(f"Imagem salva em: {save_path}")
    except requests.RequestException as e:
        print(f"Erro ao baixar imagem de {url}: {e}")
        raise

def create_images(segments):
    """Cria imagens para os segmentos fornecidos."""
    image_paths = []
    for idx, segment in enumerate(segments):
        segment_dir = os.path.join(IMAGES_DIR, f"segment_{idx}")
        os.makedirs(segment_dir, exist_ok=True)

        # Gerar apenas uma imagem por segmento
        existing_images = [img for img in os.listdir(segment_dir) if img.endswith('.jpg')]
        if len(existing_images) >= 1:
            print(f"Imagem já gerada para o segmento {idx}, pulando geração.")
            image_paths.append(os.path.join(segment_dir, existing_images[0]))
            continue

        sanitized_segment = sanitize_prompt(segment)
        prompt = f"Crie uma imagem para o seguinte trecho do roteiro: {sanitized_segment}"

        # Gera uma imagem usando OpenAI
        image_urls = generate_images(prompt, num_images=1)
        for url in image_urls:
            image_path = os.path.join(segment_dir, 'image.jpg')
            try:
                download_image(url, image_path)
                image_paths.append(image_path)
            except Exception as e:
                print(f"Erro ao processar imagem: {e}")

    return image_paths
