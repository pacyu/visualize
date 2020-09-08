import audio_visual
import argparse
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Audio visualization', conflict_handler='resolve')
    parser.add_argument('-e', '--effect',
                        help='visualization effect: 1d or 2d or 3d')
    parser.add_argument('-f', '--filename', type=str,
                        help='play audio file')
    parser.add_argument('-r', '--playback-rate', type=float,
                        help='Specify the playback rate.(e.g. 1.2)', default=1.)
    parser.add_argument('-d', '--delay', type=float,
                        help='Specify the delay time to play the animation.(unit second)', default=4)
    cmd = parser.parse_args(sys.argv[1:])
    parser.print_help()
    run = audio_visual.AudioVisualize(filename=cmd.filename,
                                      rate=cmd.playback_rate,
                                      delay=cmd.delay)
    if cmd.effect == '1' or cmd.effect == '1d' or cmd.effect == '1D':
        if cmd.filename:
            run.music_visualize_1d()
        else:
            run.audio_visualize_1d()
    elif cmd.effect == '2' or cmd.effect == '2d' or cmd.effect == '2D':
        if cmd.filename:
            run.music_visualize_2d()
        else:
            run.audio_visualize_2d()
    elif cmd.effect == '3' or cmd.effect == '3d' or cmd.effect == '3D':
        if cmd.filename:
            run.music_visualize_3d()
        else:
            run.audio_visualize_1d()


