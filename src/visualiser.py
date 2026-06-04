import librosa.display
import matplotlib.pyplot as plt


class AudioVisualizer:
    def __init__(self, audio, sample_rate):
        self.audio = audio
        self.sample_rate = sample_rate

    def plot_waveform(self):
        fig, ax = plt.subplots(figsize=(12, 4), dpi=120)

        librosa.display.waveshow(
            self.audio,
            sr=self.sample_rate,
            ax=ax
        )

        ax.set_title("Waveform")
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Amplitude")
        ax.grid(True, alpha=0.3)

        fig.tight_layout()
        return fig

    def plot_spectrogram(self, spectrogram_db):
        fig, ax = plt.subplots(figsize=(12, 5), dpi=120)

        img = librosa.display.specshow(
            spectrogram_db,
            sr=self.sample_rate,
            x_axis="time",
            y_axis="log",
            ax=ax
        )

        ax.set_title("STFT Spectrogram")
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Frequency (Hz, log scale)")

        fig.colorbar(img, ax=ax, format="%+2.0f dB")
        fig.tight_layout()

        return fig

    def plot_loudness(self, times, rms):
        fig, ax = plt.subplots(figsize=(12, 4), dpi=120)

        ax.plot(times, rms)
        ax.set_title("RMS Loudness Over Time")
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("RMS Energy")
        ax.grid(True, alpha=0.3)

        fig.tight_layout()
        return fig