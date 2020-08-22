# visualize
Get stream from sound card and draw waveform with matplotlib on python.

# Usage
```bash
$ git clone https://github.com/darkchii/visualize.git
$ cd visualize
```
then
```bash
$ py run.py 1d
```
or
```bash
$ py run.py 2d
```
or
```bash
$ py run.py 3d
```
or
```bash
$ py run.py m1d "/path/xxx.mp3" 1.2
```
or
```bash
$ py run.py m2d "/path/xxx.mp3" 1.2
```
or
```bash
$ py run.py m3d "/path/xxx.mp3" 1.2
```

Parameters Description: 

  1. Select Input or output device mode and visualization style.
  2. Audio file path.(output device mode only)
  3. Playback rate.(output device mode only)

# Demo
[bilibili](https://www.bilibili.com/video/av77372866)

# Screenshot
![demo1](demo/audio_visualize_1d.png)
![demo2](demo/audio_visualize_2d.png)
![demo3](demo/audio_visualize_3d.png)
