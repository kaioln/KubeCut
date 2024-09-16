import cv2
import numpy as np
import sys
import os
from rich.console import Console
from rich.progress import Progress

console = Console()

def detect_scene_changes_and_split(video_path, min_clip_length=21, max_clip_length=34, threshold=30):
    console.log(f"[bold green]Detecção de mudanças de cena no vídeo {video_path}...")
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)  # Obter FPS do vídeo
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # Total de frames
    min_clip_frames = int(fps * min_clip_length)  # Mínimo de frames por corte
    max_clip_frames = int(fps * max_clip_length)  # Máximo de frames por corte
    
    prev_frame = None
    scene_changes = []
    frame_count = 0
    block_count = 0

    console.log(f"[bold cyan]Total de frames: {total_frames}")
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Detectando cenas...", total=total_frames)

        while True:
            ret, frame = video.read()
            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if prev_frame is not None:
                frame_diff = cv2.absdiff(prev_frame, gray_frame)
                diff_mean = np.mean(frame_diff)

                if diff_mean > threshold and (frame_count - block_count >= min_clip_frames):
                    scene_changes.append(frame_count)
                    block_count = frame_count  # Resetar o contador de blocos
            
            if frame_count - block_count >= max_clip_frames:
                scene_changes.append(frame_count)
                block_count = frame_count

            prev_frame = gray_frame
            frame_count += 1
            progress.update(task, advance=1)

    video.release()

    if 0 not in scene_changes:
        scene_changes.insert(0, 0)
    if total_frames not in scene_changes:
        scene_changes.append(total_frames)

    console.log(f"[bold green]Encontrados {len(scene_changes) - 1} pontos de mudança de cena.")
    return scene_changes

def split_and_resize_clips(video_path, scene_changes, output_folder="clips", target_resolution=(1080, 1920)):
    console.log(f"[bold green]Dividindo e redimensionando clipes em {output_folder}...")
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Processando clipes...", total=len(scene_changes) - 1)

        for i in range(len(scene_changes) - 1):
            start_frame = scene_changes[i]
            end_frame = scene_changes[i + 1]

            clip_name = os.path.join(output_folder, f"clip_{i + 1}.mp4")  # Sempre .mp4
            console.log(f"[yellow]Processando clipe {i + 1}: {clip_name}")
            fourcc = cv2.VideoWriter_fourcc(*'H264')  # Usando H264 para MP4
            output = cv2.VideoWriter(clip_name, fourcc, fps, target_resolution)

            video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

            for frame_idx in range(start_frame, end_frame):
                ret, frame = video.read()
                if not ret:
                    console.log(f"[bold red]Erro ao ler o frame {frame_idx}.")
                    break
                
                h, w, _ = frame.shape
                new_w = int(target_resolution[1] * w / h)
                
                if new_w > target_resolution[0]:
                    crop_x = (new_w - target_resolution[0]) // 2
                    frame = cv2.resize(frame, (new_w, target_resolution[1]))
                    frame = frame[:, crop_x:crop_x + target_resolution[0]]
                else:
                    frame = cv2.resize(frame, target_resolution)

                output.write(frame)

            output.release()
            progress.update(task, advance=1)

    video.release()
    console.log(f"[bold green]Todos os clipes foram salvos na pasta {output_folder}.")

if len(sys.argv) != 3:
    console.log("[bold red]Uso: python main.py <caminho_do_video> <pasta_de_saida>")
    sys.exit(1)

video_path = sys.argv[1]
output_folder = sys.argv[2]

scene_changes = detect_scene_changes_and_split(video_path, min_clip_length=21, max_clip_length=34)
split_and_resize_clips(video_path, scene_changes, output_folder)
