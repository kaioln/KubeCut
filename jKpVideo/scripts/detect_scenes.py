import subprocess
import sys

def detect_scene_changes(video_path, output_file):
    command = [
        'ffprobe', 
        '-f', 'lavfi', 
        '-i', f'select=scene=1',
        '-vsync', 'vfr',
        '-an', 
        '-f', 'null', 
        '-',
        '-loglevel', 'error'
    ]
    
    with open(output_file, 'w') as f:
        subprocess.run(command, stdout=f, stderr=subprocess.PIPE)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python detect_scenes.py <video_path> <output_file>")
        sys.exit(1)

    video_path = sys.argv[1]
    output_file = sys.argv[2]
    detect_scene_changes(video_path, output_file)
