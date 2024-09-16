from moviepy.editor import VideoFileClip
import sys
import os
import cv2
import numpy as np

def detect_scene_changes(video_path, threshold=30):
    print(f"Detectando mudanças de cena no vídeo {video_path}...")
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    prev_frame = None
    scene_changes = []
    frame_count = 0

    while True:
        ret, frame = video.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is not None:
            frame_diff = cv2.absdiff(prev_frame, gray_frame)
            diff_mean = np.mean(frame_diff)

            if diff_mean > threshold:
                scene_changes.append(frame_count)
        
        prev_frame = gray_frame
        frame_count += 1

    video.release()

    if 0 not in scene_changes:
        scene_changes.insert(0, 0)
    if total_frames not in scene_changes:
        scene_changes.append(total_frames)

    return scene_changes

def write_scene_changes_to_file(scene_changes_file, scene_changes):
    with open(scene_changes_file, 'w') as file:
        for change in scene_changes:
            file.write(f"{change}\n")

def split_and_resize_clips(video_path, scene_changes_file, output_folder, min_clip_length=21, max_clip_length=34, target_resolution=(1080, 1920)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Verifique se o arquivo de mudanças de cena contém dados válidos
    if not os.path.isfile(scene_changes_file) or os.path.getsize(scene_changes_file) == 0:
        print(f"Arquivo de mudanças de cena vazio ou não encontrado: {scene_changes_file}")
        return

    with open(scene_changes_file, 'r') as file:
        scene_changes = [int(line.strip()) for line in file.readlines()]

    if len(scene_changes) < 2:
        print(f"Não há mudanças de cena suficientes para processar.")
        return

    try:
        video = VideoFileClip(video_path)
    except Exception as e:
        print(f"Erro ao abrir o vídeo: {e}")
        return

    fps = video.fps
    print(f"FPS do vídeo: {fps}")

    for i in range(len(scene_changes) - 1):
        start = scene_changes[i] / fps
        end = scene_changes[i + 1] / fps

        print(f"Processando clipe {i + 1}: Início {start} s, Fim {end} s")

        try:
            clip = video.subclip(start, end)
        except Exception as e:
            print(f"Erro ao criar subclip {i + 1}: {e}")
            continue

        # Redimensionar o clipe
        clip = clip.resize(height=target_resolution[1])

        # Ajustar a largura
        new_width = int(target_resolution[1] * clip.size[0] / clip.size[1])
        if new_width > target_resolution[0]:
            x_offset = (new_width - target_resolution[0]) // 2
            clip = clip.crop(x1=x_offset, x2=x_offset + target_resolution[0])
        else:
            clip = clip.resize(width=target_resolution[0])

        clip_name = os.path.join(output_folder, f"clip_{i + 1}.mp4")
        print(f"Salvando clipe em {clip_name}")
        try:
            clip.write_videofile(clip_name, codec='libx264', audio_codec='aac')
            print(f"Clipe {i + 1} salvo com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar o clipe {i + 1}: {e}")

    print(f"Todos os clipes foram salvos na pasta {output_folder}.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python process_video.py <video_path> <scene_changes_file> <output_folder>")
        sys.exit(1)

    video_path = sys.argv[1]
    scene_changes_file = sys.argv[2]
    output_folder = sys.argv[3]

    # Detecção de mudanças de cena e gravação
    scene_changes = detect_scene_changes(video_path)
    write_scene_changes_to_file(scene_changes_file, scene_changes)

    # Processamento dos clipes
    split_and_resize_clips(video_path, scene_changes_file, output_folder)
