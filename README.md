# visualize
Get stream from sound card and draw waveform with matplotlib on python.

# Usage


```bash
$ git clone https://github.com/darkchii/visualize.git
$ cd visualize
```
then
```bash
$ py run.py -h
```

output:
```bash
usage: Audio visualization [-h] [-e EFFECT] [-f FILENAME] [-r PLAYBACK_RATE]
                           [-p PAUSE]

optional arguments:
  -h, --help            show this help message and exit
  -e EFFECT, --effect EFFECT
                        visualization effect: 1d or 2d or 3d
  -f FILENAME, --filename FILENAME
                        play audio file
  -r PLAYBACK_RATE, --playback-rate PLAYBACK_RATE
                        Specify the playback rate.(e.g. 1.2)
  -p PAUSE, --pause PAUSE
                        Specify the delay time to play the animation.(unit
                        second)
```

e.g.
```bash
$ py run.py -e 1d
```
or
```bash
$ py run.py -e 2d
```
or
```bash
$ py run.py -e 3d
```
or
```bash
$ py run.py -e 1d -f "/path/xxx.mp3" -r 1.2
```
or
```bash
$ py run.py -e 2d -f "/path/xxx.mp3" -r 1.2
```
or
```bash
$ py run.py -e 3d -f "/path/xxx.mp3" -r 1.2
```

Parameters Description: 

  1. Select visualization style.
  2. Audio file path.(output device mode only)
  3. Playback rate.(output device mode only)
  4. Delay time to play the animation.

# Demo
[bilibili](https://www.bilibili.com/video/av77372866)

# Screenshot
![demo1](demo/audio_visualize_1d.png)
![demo2](demo/audio_visualize_2d.png)
![demo3](demo/audio_visualize_3d.png)
