import librosa
import numpy as np


class AudioAnalyzer:
    def __init__(self, audio, sample_rate):
        self.audio = audio
        self.sample_rate = sample_rate

    def get_stft_spectrogram(self):
        stft = librosa.stft(self.audio)
        spectrogram_db = librosa.amplitude_to_db(
            np.abs(stft),
            ref=np.max
        )
        return spectrogram_db

    def get_rms_loudness(self):
        rms = librosa.feature.rms(y=self.audio)[0]
        times = librosa.times_like(rms, sr=self.sample_rate)
        return times, rms