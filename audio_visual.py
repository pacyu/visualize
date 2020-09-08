from mpl_toolkits.mplot3d import Axes3D
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import struct
from scipy.signal import detrend
from _tkinter import TclError
from matplotlib.animation import FuncAnimation
from pydub import AudioSegment
from matplotlib.collections import LineCollection


class AudioVisualize(object):

    def __init__(self, filename: str = None, rate=1., delay=4.):
        p = pyaudio.PyAudio()
        self.record_delay = delay
        if filename is None:
            self.channels = 1
            self.rate = 48000
            self.window = int(self.rate * 0.02)
            self.fwhm = 20
            self.stream = p.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.rate,
                input=True,
            )
        else:
            sound = AudioSegment.from_file(filename)
            self.left = sound.split_to_mono()[0]
            self.size = len(self.left.get_array_of_samples())
            self.rate = self.left.frame_rate
            self.window = int(self.rate * 0.02)
            self.stream = p.open(
                format=p.get_format_from_width(self.left.sample_width),
                channels=self.left.channels,
                rate=int(self.rate * rate),
                output=True,
            )

        self.stream.start_stream()

    def audio_visualize_1d(self):
        xf = np.linspace(20, self.rate / 2, self.window)
        fig, ax = plt.subplots(figsize=(14, 5))
        lf, = ax.semilogx(xf, np.zeros(self.window), lw=1, color='lightblue')
        ax.set_ylim(-0.5, 1.5)
        ax.set_axis_off()
        plt.show(block=False)
        plt.pause(self.record_delay)

        while self.stream.is_active():
            data = self.stream.read(self.window)
            data_int = struct.unpack(str(self.window * 2) + 'B', data)
            y_detrend = detrend(data_int)
            box = np.ones(self.fwhm) / self.fwhm
            y_smooth = np.convolve(y_detrend, box, mode='same')
            yft = np.abs(np.fft.fft(y_smooth))
            y_vals = yft[:self.window] / (64 * self.window)
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
        t = np.linspace(0, 2. * np.pi, self.window * 2)
        xf = np.cos(t)
        yf = np.sin(t)
        fig, ax = plt.subplots(figsize=(7, 7))
        lf, = ax.plot(xf, yf, lw=1, color='lightblue')
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_axis_off()
        plt.show(block=False)
        plt.pause(self.record_delay)

        while self.stream.is_active():
            data = self.stream.read(self.window)
            data_int = struct.unpack(str(self.window * 2) + 'B', data)
            y_detrend = detrend(data_int)
            yft = np.abs(np.fft.fft(y_detrend))
            y_vals = yft / (64 * self.window)
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
        t = np.linspace(0, 2. * np.pi, self.window * 2)
        xf = np.cos(t)
        yf = np.sin(t)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        lf, = ax.plot(xf, yf, np.zeros(self.window * 2), lw=1, color='lightblue')
        ax.set_zlim(-0.2, 1.2)
        ax.set_axis_off()
        plt.show(block=False)
        plt.pause(self.record_delay)

        while self.stream.is_active():
            data = self.stream.read(self.window)
            data_int = struct.unpack(str(self.window * 2) + 'B', data)
            z_detrend = detrend(data_int)
            zf = np.abs(np.fft.fft(z_detrend))
            z_vals = zf / (64 * self.window)
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
        fig = plt.figure(facecolor='black')
        ax = fig.gca()
        norm = plt.Normalize(-1., 1.)
        lc = LineCollection([], cmap='cool', norm=norm)
        ax.set_ylim(-1.5, 1.5)
        ax.set_axis_off()
        time = np.linspace(0, 2 * np.pi, self.window)
        ax.add_collection(lc)
        plt.pause(self.record_delay)

        def update(frames):
            if self.stream.is_active():
                slice = self.left.get_sample_slice(frames, frames + self.window)
                self.stream.write(slice.raw_data)
                y = np.array(slice.get_array_of_samples()) / 30000
                points = np.array([np.cos(time), y]).T.reshape((-1, 1, 2))  # 控制曲线精细程度和振幅
                segments = np.concatenate([points[:-1], points[1:]], axis=1)
                lc.set_segments(segments)
                lc.set_array(y)  # 控制颜色
            return lc,

        ani = FuncAnimation(fig, update, frames=range(0, self.size, self.window), interval=0, blit=True)
        plt.show()

    def music_visualize_2d(self):
        t = np.linspace(0, 2 * np.pi, self.window)
        fig = plt.figure(facecolor='black')
        ax = fig.gca(projection='polar')
        ax.set_axis_off()
        lf, = ax.plot(t, np.zeros(self.window), lw=1, color='lightblue')
        plt.pause(self.record_delay)

        def update(frames):
            if self.stream.is_active():
                slice = self.left.get_sample_slice(frames, frames + self.window)
                self.stream.write(slice.raw_data)
                y = np.array(slice.get_array_of_samples()) / 1000000
                # yft = np.abs(np.fft.fft(y)) / self.window
                lf.set_ydata(y)
            return lf,

        ani = FuncAnimation(fig, update, frames=range(0, self.size, self.window), interval=0, blit=True)
        plt.show()

    def music_visualize_3d(self):
        t = np.linspace(0, 2 * np.pi, self.window)
        x, y = np.cos(t), np.sin(t)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_axis_off()
        lf, = ax.plot(x, y, np.zeros(self.window), lw=1, color='lightblue')
        lf2, = ax.plot(x, y, np.zeros(self.window), lw=1, color='orange')
        plt.pause(self.record_delay)

        def update(frames):
            if self.stream.is_active():
                slice = self.left.get_sample_slice(frames, frames + self.window)
                self.stream.write(slice.raw_data)
                z = np.array(slice.get_array_of_samples())
                zft = np.abs(np.fft.fft(z / max(z))) / (self.window * 4)
                lf.set_xdata(x)
                lf.set_ydata(y)
                lf.set_3d_properties(zft)
                lf2.set_xdata(x)
                lf2.set_ydata(y)
                lf2.set_3d_properties(z / 1000000)

            return lf, lf2,

        ani = FuncAnimation(fig, update, frames=range(0, self.size, self.window), interval=0, blit=True)
        plt.show()
