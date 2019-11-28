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

R = 20
t = np.linspace(0, 2*np.pi, chunk * 2)
xf = R*np.cos(t)
yf = R*np.sin(t)
fig = plt.figure()
ax = fig.gca(projection='3d')
lf, = ax.plot(xf, yf, np.zeros(chunk * 2), lw=1)
ax.set_zlim(-0.2, 1.2)
ax.set_axis_off()
plt.show(block=False)

while stream.is_active():
    data = stream.read(chunk)
    data_int = struct.unpack(str(chunk * 2) + 'B', data)
    z_detrend = detrend(data_int)
    zf = np.abs(np.fft.fft(z_detrend))
    z_vals = zf / (256 * chunk)
    ind = np.where(z_vals > np.mean(z_vals))
    z_vals[ind[0]] *= 4
    lf.set_xdata(xf)
    lf.set_ydata(yf)
    lf.set_3d_properties(z_vals)

    try:
        ax.figure.canvas.draw()
        ax.figure.canvas.flush_events()
    except TclError:
        stream.stop_stream()
        stream.close()
        break
