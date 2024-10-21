import subprocess

def add_subtitle(input_video, output_video, subtitle_text, font_file, font_size=20, 
                 font_color="16777215", border_color="0", border_width=4, 
                 alignment=2):  # Padrão para central inferior
    try:
        # Comando FFmpeg para adicionar legenda
        command = [
            'ffmpeg',
            '-y',
            '-i', input_video,  # Arquivo de vídeo de entrada
            '-vf', (f"subtitles={ass_filename}:"
                     f"force_style='FontName=Comic Sans MS,"
                     f"FontSize={font_size},"
                     f"PrimaryColour={font_color},"
                     f"BorderStyle=1,"
                     f"Outline={border_width},"
                     f"OutlineColour={border_color},"
                     f"Alignment={alignment}'"),
            '-codec:a', 'copy',  # Copiar o áudio original
            output_video  # Arquivo de saída com a legenda
        ]
        
        # Executa o comando
        subprocess.run(command, check=True)
        print(f"Legenda '{subtitle_text}' adicionada com sucesso no vídeo '{input_video}'. Arquivo de saída: '{output_video}'")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao adicionar legenda: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Exemplo de uso
if __name__ == "__main__":
    # Caminho do vídeo de entrada
    input_video = 'teste.mp4'
    
    # Caminho do vídeo de saída
    output_video = 'output_video_com_legenda.mp4'
    
    # Texto da legenda
    subtitle_text = 'teste.srt'

    ass_filename = 'exemplo.ass'
    
    # Caminho para o arquivo de fonte (certifique-se de usar o caminho correto)
    font_file = 'ariali.ttf'  # Certifique-se de que o caminho da fonte está correto
    
    # Chamar a função para adicionar legenda
    add_subtitle(input_video, output_video, subtitle_text, font_file)
