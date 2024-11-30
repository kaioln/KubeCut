from common.models.client_api import client
from common.models.configs import config
from common.models.platform_size import platform_size

platform_post = config['platform_post']

def generate_images(prompt, num_images=2):
    target_width, target_height = platform_size(platform=platform_post)
    # Reduza as dimensões para melhorar a performance
    # target_width = max(512, target_width // 2)
    # target_height = max(512, target_height // 2)
    size = f"{target_width}x{target_height}"
    images = []
    for _ in range(num_images):
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size=size
            )
            image_url = response.data[0].url
            print(f"Imagem gerada: {image_url}")
            images.append(image_url)
        except Exception as e:
            print(f"Erro ao gerar imagem: {e}")
    return images
