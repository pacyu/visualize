import audio_visual
import sys


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            if len(sys.argv) > 3:
                run = audio_visual.AudioVisualize(sys.argv[2], float(sys.argv[3]))
            else:
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
        print('run.py [options](Input device: 1d | 2d | 3d) |'
              ' (Output device: m1d filename | m2d filename | m3d filename |'
              ' m1d filename 1.2 | m2d filename 1.2 | m3d filename 1.2)')
