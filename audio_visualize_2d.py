from _tkinter import TclError
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import struct
from scipy.signal import savgol_filter, detrend, lfilter


channels = 1
rate = 48000
chunk = 1024 * 2

p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=channels,
    rate=rate,
    input=True,
    # output=True,
    frames_per_buffer=chunk
)

stream.start_stream()

R = 2
t = np.linspace(0, 2*np.pi, chunk * 2)
xf = R*np.cos(t)
yf = R*np.sin(t)
fig, ax = plt.subplots(figsize=(7, 7))
lf, = ax.plot(xf, yf, lw=1)
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_axis_off()
plt.show(block=False)

while stream.is_active():
    data = stream.read(chunk)
    data_int = struct.unpack(str(chunk * 2) + 'B', data)
    y_detrend = detrend(data_int)
    yft = np.abs(np.fft.fft(y_detrend))
    y_vals = yft / (256 * chunk)
    ind = np.where(y_vals > np.mean(y_vals))
    y_vals[ind[0]] *= 4
    lf.set_xdata(xf + y_vals * np.cos(t))
    lf.set_ydata(yf + y_vals * np.sin(t))

    try:
        ax.figure.canvas.draw()
        ax.figure.canvas.flush_events()
    except TclError:
        stream.stop_stream()
        stream.close()
        break
