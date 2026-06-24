import librosa
import numpy as np


def estimate_bpm_librosa(samples, sample_rate):
    tempo, beat_frames = librosa.beat.beat_track(
        y=samples,
        sr=sample_rate,
    )

    tempo = np.asarray(tempo).item()

    return tempo, beat_frames