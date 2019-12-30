import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import struct
from scipy.signal import detrend
from _tkinter import TclError


class AudioVisualize(object):

    def __init__(self):
        self.channels = 1
        self.rate = 48000
        self.chunk = 1024 * 2
        self.fwhm = 20

        p = pyaudio.PyAudio()
        self.stream = p.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.rate,
            input=True,
            # output=True,
        )

        self.stream.start_stream()

    def audio_visualize_1d(self):
        xf = np.linspace(0, self.rate, self.chunk)
        fig, ax = plt.subplots(figsize=(14, 5))
        lf, = ax.semilogx(xf, np.zeros(self.chunk), lw=1)
        ax.set_xlim(20, self.rate / 2)
        ax.set_ylim(-0.5, 1.5)
        ax.set_axis_off()
        plt.show(block=False)

        while self.stream.is_active():
            data = self.stream.read(self.chunk)
            data_int = struct.unpack(str(self.chunk * 2) + 'B', data)
            y_detrend = detrend(data_int)
            box = np.ones(self.fwhm) / self.fwhm
            y_smooth = np.convolve(y_detrend, box, mode='same')
            yft = np.abs(np.fft.fft(y_smooth))
            y_vals = yft[:self.chunk] / (64 * self.chunk)
            # ind = np.where(y_vals > np.mean(y_vals))
            # y_vals[ind[0]] *= 4
            lf.set_ydata(y_vals)

            try:
                ax.figure.canvas.draw()
                ax.figure.canvas.flush_events()
            except TclError:
                self.stream.stop_stream()
                self.stream.close()
                break

    def audio_visualize_2d(self):
        r = 2.
        t = np.linspace(0, 2. * np.pi, self.chunk * 2)
        xf = r * np.cos(t)
        yf = r * np.sin(t)
        fig, ax = plt.subplots(figsize=(7, 7))
        lf, = ax.plot(xf, yf, lw=1)
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_axis_off()
        plt.show(block=False)

        while self.stream.is_active():
            data = self.stream.read(self.chunk)
            data_int = struct.unpack(str(self.chunk * 2) + 'B', data)
            y_detrend = detrend(data_int)
            yft = np.abs(np.fft.fft(y_detrend))
            y_vals = yft / (64 * self.chunk)
            # ind = np.where(y_vals > np.mean(y_vals))
            # y_vals[ind[0]] *= 4
            lf.set_xdata(xf + y_vals * np.cos(t))
            lf.set_ydata(yf + y_vals * np.sin(t))

            try:
                ax.figure.canvas.draw()
                ax.figure.canvas.flush_events()
            except TclError:
                self.stream.stop_stream()
                self.stream.close()
                break

    def audio_visualize_3d(self):
        r = 20.
        t = np.linspace(0, 2. * np.pi, self.chunk * 2)
        xf = r * np.cos(t)
        yf = r * np.sin(t)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        lf, = ax.plot(xf, yf, np.zeros(self.chunk * 2), lw=1)
        ax.set_zlim(-0.2, 1.2)
        ax.set_axis_off()
        plt.show(block=False)

        while self.stream.is_active():
            data = self.stream.read(self.chunk)
            data_int = struct.unpack(str(self.chunk * 2) + 'B', data)
            z_detrend = detrend(data_int)
            zf = np.abs(np.fft.fft(z_detrend))
            z_vals = zf / (64 * self.chunk)
            # ind = np.where(z_vals > np.mean(z_vals))
            # z_vals[ind[0]] *= 4
            lf.set_xdata(xf)
            lf.set_ydata(yf)
            lf.set_3d_properties(z_vals)

            try:
                ax.figure.canvas.draw()
                ax.figure.canvas.flush_events()
            except TclError:
                self.stream.stop_stream()
                self.stream.close()
                break

    def audio_visualize_2d_rainbow(self):
        theta = np.linspace(0.0, 2. * np.pi, self.chunk, endpoint=False)
        radii = np.zeros(self.chunk)
        fig = plt.figure()
        ax = fig.gca(projection='polar')
        lf = ax.bar(x=theta, height=radii, width=0.02, bottom=-2.0, alpha=0.5)
        ax.set_axis_off()
        plt.show(block=False)

        while self.stream.is_active():
            data = self.stream.read(self.chunk)
            data_int = struct.unpack(str(self.chunk * 2) + 'B', data)
            y_detrend = detrend(data_int)

            yft = np.abs(np.fft.fft(y_detrend))
            y_vals = yft[:self.chunk] / (128 * self.chunk)

            for rect, y_val, color in zip(lf.patches, y_vals, plt.cm.Spectral(y_vals * 8)):
                rect.set_height(y_val)
                rect.set_facecolor(color)

            try:
                ax.figure.canvas.draw()
                ax.figure.canvas.flush_events()
            except TclError:
                self.stream.stop_stream()
                self.stream.close()
                break
