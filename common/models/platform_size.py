
def platform_size(platform):
    # Dimensões da plataforma de destino
    platform_dimensions = {
        'instagram_feed': (1080, 1080),
        'instagram_feed2': (1024, 1024),
        'instagram_reels': (1080, 1920),
        'instagram_reels2': (1024, 1792),
        'tiktok': (1080, 1920),
        'tiktok2': (1024, 1792),
        'youtube': (1920, 1080),
        'youtube2': (1792, 1024)
    }
    
    if platform not in platform_dimensions:
        raise ValueError(f"Plataforma {platform} não suportada. Escolha entre: {list(platform_dimensions.keys())}")
    
    return platform_dimensions[platform]