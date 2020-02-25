import audio_visual
import sys


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            run = audio_visual.AudioVisualize(sys.argv[2])
        else:
            run = audio_visual.AudioVisualize()
        typed = sys.argv[1]
        if typed == '1d':
            run.audio_visualize_1d()
        elif typed == '2d':
            run.audio_visualize_2d()
        elif typed == '3d':
            run.audio_visualize_3d()
        elif typed == 'm1d':
            run.music_visualize_1d()
        elif typed == 'm2d':
            run.music_visualize_2d()
        elif typed == 'm3d':
            run.music_visualize_3d()
    else:
        print('run.py [options](1d | 2d | 3d | m1d filename | m2d filename | m3d filename)')
