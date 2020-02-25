from mpl_toolkits.mplot3d import Axes3D
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import struct
from scipy.signal import detrend
import wave
from _tkinter import TclError
from matplotlib.animation import FuncAnimation


class AudioVisualize(object):

    def __init__(self, filename: str = None):
        self.channels = 1
        self.rate = 48000
        self.chunk = 1024
        self.fwhm = 20

        p = pyaudio.PyAudio()
        if filename is None:
            self.stream = p.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.rate,
                input=True,
            )
        else:
            self.wf = wave.open(filename)
            self.stream = p.open(
                format=p.get_format_from_width(self.wf.getsampwidth()),
                channels=self.wf.getnchannels(),
                rate=self.wf.getframerate(),
                output=True,
                # frames_per_buffer=chunk
            )

        self.stream.start_stream()

    def audio_visualize_1d(self):
        xf = np.linspace(20, self.rate / 2, self.chunk)
        fig, ax = plt.subplots(figsize=(14, 5))
        lf, = ax.semilogx(xf, np.zeros(self.chunk), lw=1)
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
            ind = np.where(y_vals > (np.max(y_vals) + np.min(y_vals)) / 2)
            y_vals[ind[0]] *= 4

            lf.set_ydata(y_vals)

            try:
                ax.figure.canvas.draw()
                ax.figure.canvas.flush_events()
            except TclError:
                self.stream.stop_stream()
                self.stream.close()
                break

    def audio_visualize_2d(self):
        t = np.linspace(0, 2. * np.pi, self.chunk * 2)
        xf = np.cos(t)
        yf = np.sin(t)
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
            ind = np.where(y_vals > (np.max(y_vals) + np.min(y_vals)) / 2)
            y_vals[ind[0]] *= 4

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
        t = np.linspace(0, 2. * np.pi, self.chunk * 2)
        xf = np.cos(t)
        yf = np.sin(t)
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
            ind = np.where(z_vals > (np.max(z_vals) + np.min(z_vals)) / 2)
            z_vals[ind[0]] *= 4

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

    def music_visualize_1d(self):
        t = np.linspace(20, 20000, self.chunk * 2)
        fig = plt.figure()
        ax = fig.gca()
        ax.set_ylim(0, 1)
        ax.set_axis_off()
        lf, = ax.semilogx(t, np.zeros(self.chunk * 2), lw=1)

        def update(frame):
            if self.stream.is_active():
                data = self.wf.readframes(self.chunk)
                self.stream.write(data)
                data_int = struct.unpack(str(self.chunk * 4) + 'B', data)
                y_detrend = detrend(data_int)
                yft = np.abs(np.fft.fft(y_detrend))
                y_vals = yft[:self.chunk * 2] / (self.chunk ** 2)
                ind = np.where(y_vals > (np.max(y_vals) + np.min(y_vals)) / 2)
                y_vals[ind[0]] *= 4
                lf.set_ydata(y_vals)
            return lf,

        ani = FuncAnimation(fig, update, frames=None, interval=0, blit=True)
        plt.show()

    def music_visualize_2d(self):
        t = np.linspace(0, 2 * np.pi, self.chunk * 2)
        fig = plt.figure()
        ax = fig.gca(projection='polar')
        ax.set_axis_off()
        lf, = ax.plot(t, np.zeros(self.chunk * 2), lw=1)

        def update(frame):
            if self.stream.is_active():
                data = self.wf.readframes(self.chunk)
                self.stream.write(data)
                data_int = struct.unpack(str(self.chunk * 4) + 'B', data)
                y_detrend = detrend(data_int)
                yft = np.abs(np.fft.fft(y_detrend))
                y_vals = yft[:self.chunk * 2] / (self.chunk ** 2 * 8)
                ind = np.where(y_vals > (np.max(y_vals) + np.min(y_vals)) / 2)
                y_vals[ind[0]] *= 2
                lf.set_ydata(y_vals)
            return lf,

        ani = FuncAnimation(fig, update, frames=None, interval=0, blit=True)
        plt.show()

    def music_visualize_3d(self):
        t = np.linspace(0, 2 * np.pi, self.chunk * 2)
        x, y = np.cos(t), np.sin(t)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_axis_off()
        lf, = ax.plot(x, y, np.zeros(self.chunk * 2), lw=1)
        lf2, = ax.plot(x, y, np.zeros(self.chunk * 2), lw=1)

        def update(frame):
            if self.stream.is_active():
                data = self.wf.readframes(self.chunk)
                self.stream.write(data)
                data_int = struct.unpack(str(self.chunk * 4) + 'B', data)
                z_detrend = detrend(data_int)
                zft = np.abs(np.fft.fft(z_detrend))
                z_vals = zft[:self.chunk * 2] / (self.chunk ** 2 * 8)
                ind = np.where(z_vals > (np.max(z_vals) + np.min(z_vals)) / 2)
                z_vals[ind[0]] *= 2
                lf.set_xdata(x)
                lf.set_ydata(y)
                lf.set_3d_properties(z_vals)
                lf2.set_xdata(x)
                lf2.set_ydata(y)
                lf2.set_3d_properties(-z_vals)

            return lf, lf2,

        ani = FuncAnimation(fig, update, frames=None, interval=0, blit=True)
        plt.show()
