from _tkinter import TclError
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import struct
from scipy.signal import detrend


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

xf = np.linspace(0, rate, chunk)
yf = np.zeros(chunk)
fig, ax = plt.subplots(figsize=(14, 5))
lf, = ax.semilogx(xf, yf, lw=1)
ax.set_xlim(20, rate / 2)
ax.set_ylim(0, 1)
ax.set_axis_off()
plt.show(block=False)
fwhm = 20

while stream.is_active():
    data = stream.read(chunk)
    data_int = struct.unpack(str(chunk * 2) + 'B', data)
    y_detrend = detrend(data_int)
    box = np.ones(fwhm) / fwhm
    y_smooth = np.convolve(y_detrend, box, mode='valid')
    yft = np.abs(np.fft.fft(y_smooth))
    y_vals = yft[:chunk] / (256 * chunk)
    ind = np.where(y_vals > np.mean(y_vals))
    y_vals[ind[0]] *= 4
    lf.set_ydata(y_vals)

    try:
        ax.figure.canvas.draw()
        ax.figure.canvas.flush_events()
    except TclError:
        stream.stop_stream()
        stream.close()
        break
