import moviepy.editor as mp

# Lista com os caminhos dos arquivos de vídeo
clip_list = ['corte_1.mp4',
'corte_2.mp4',
'corte_3.mp4',
'corte_4.mp4',
'corte_5.mp4',
'corte_6.mp4',
'corte_7.mp4',
'corte_8.mp4',
'corte_9.mp4',
'corte_10.mp4']

# Carregar os clipes
clips = [mp.VideoFileClip(c) for c in clip_list]

# Concatenar os clipes
final_clip = mp.concatenate_videoclips(clips)

# Exportar o vídeo final
final_clip.write_videofile("output.mp4")