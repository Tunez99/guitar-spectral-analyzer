import librosa.display
import matplotlib.pyplot as plt


class AudioVisualizer:
    def __init__(self, audio, sample_rate):
        self.audio = audio
        self.sample_rate = sample_rate

    def plot_waveform(self):
        fig, ax = plt.subplots()
        librosa.display.waveshow(
            self.audio,
            sr=self.sample_rate,
            ax=ax
        )
        ax.set_title("Waveform")
        ax.set_xlabel("Time")
        ax.set_ylabel("Amplitude")
        return fig

    def plot_spectrogram(self, spectrogram_db):
        fig, ax = plt.subplots()
        img = librosa.display.specshow(
            spectrogram_db,
            sr=self.sample_rate,
            x_axis="time",
            y_axis="hz",
            ax=ax
        )
        ax.set_title("STFT Spectrogram")
        fig.colorbar(img, ax=ax, format="%+2.0f dB")
        return fig

    def plot_loudness(self, times, rms):
        fig, ax = plt.subplots()
        ax.plot(times, rms)
        ax.set_title("RMS Loudness")
        ax.set_xlabel("Time")
        ax.set_ylabel("RMS Energy")
        return fig