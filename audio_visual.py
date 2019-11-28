import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import struct
from matplotlib.animation import FuncAnimation


channels = 1
rate = 48000
chunk = 1024 * 2
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=channels,
    rate=rate,
    input=True,
    output=True,
)

stream.start_stream()
x = np.arange(0, 2*chunk, 2)
xf = np.linspace(0, rate, chunk)
fig, (ax1, ax2) = plt.subplots(2)
l, = ax1.plot(x, np.zeros(chunk), '-', lw=1)
lf, = ax2.semilogx(xf, np.zeros(chunk), '-', lw=1)
ax1.set_xlim(0, 2*chunk)
ax1.set_ylim(0, 256)
ax2.set_xlim(20, rate / 2)
ax2.set_ylim(0, 1)
plt.setp(ax1, xticks=[0, chunk, 2 * chunk], yticks=[0, 128, 256])
fwhm = 20


def gen():
    while stream.is_active():
        data = stream.read(chunk)
        data_int = struct.unpack(str(chunk*2) + 'B', data)
        box = np.ones(fwhm) / fwhm
        y_smooth = np.convolve(data_int, box, mode='same')
        data_np = np.array(y_smooth, dtype='b')[::2] + 128
        yf = np.fft.fft(y_smooth)
        yield data_np, yf


def init():
    lf.set_ydata(np.zeros(chunk))
    return lf,


def update(data):
    ax1.figure.canvas.draw()
    ax2.figure.canvas.draw()
    l.set_ydata(data[0])
    lf.set_ydata(np.abs(data[1][:chunk]) / (128 * chunk))
    return lf,


animate = FuncAnimation(fig, update, gen, blit=True, interval=0.1, repeat=False, init_func=init)
plt.show()
stream.stop_stream()
stream.close()
