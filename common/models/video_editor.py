import cv2
from common.models.configs import config

platform_post = config['platform_post']

def adjust_focus(clip):
    """Ajusta o foco e realiza o crop do vídeo mantendo as proporções e com foco em rostos."""

    target_width, target_height = platform_size(platform=platform_post)

    # Dimensões do vídeo original
    original_width, original_height = clip.size
    
    # Calcular a proporção do vídeo original e do destino
    original_ratio = original_width / original_height
    target_ratio = target_width / target_height

    # Detectar a face no primeiro frame
    frame = clip.get_frame(0)
    frame_cv = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Carregar o classificador de faces pré-treinado do OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detectar faces no frame
    gray = cv2.cvtColor(frame_cv, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        # Supondo que a primeira face detectada é a principal
        (x, y, w, h) = faces[0]
        center_x = x + w // 2
        center_y = y + h // 2
    else:
        # Se nenhuma face for detectada, manter o foco central
        center_x = original_width // 2
        center_y = original_height // 2

    # Aplicar o corte proporcional baseado na detecção de rosto
    if original_ratio > target_ratio:
        # Cortar horizontalmente (mais largo que o necessário)
        new_width = int(target_ratio * original_height)
        x1 = max(center_x - new_width // 2, 0)
        x2 = min(x1 + new_width, original_width)
        y1, y2 = 0, original_height
    else:
        # Cortar verticalmente (mais alto que o necessário)
        new_height = int(original_width / target_ratio)
        y1 = max(center_y - new_height // 2, 0)
        y2 = min(y1 + new_height, original_height)
        x1, x2 = 0, original_width

    # Aplicar o crop ao clipe
    cropped_clip = clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)

    # Redimensionar para as dimensões de destino
    resized_clip = cropped_clip.resize(newsize=(target_width, target_height))

    return resized_clip

def platform_size(platform):
    # Dimensões da plataforma de destino
    platform_dimensions = {
        'instagram_feed': (1080, 1080),
        'instagram_reels': (1080, 1920),
        'tiktok': (1080, 1920),
        'youtube': (1920, 1080)
    }
    
    if platform not in platform_dimensions:
        raise ValueError(f"Plataforma {platform} não suportada. Escolha entre: {list(platform_dimensions.keys())}")
    
    return platform_dimensions[platform]