import numpy as np


def frame_signal(samples, frame_size, hop_size):
    """
    Split the audio signal into small overlapping frames.

    frame_size:
        Number of samples per frame.

    hop_size:
        Number of samples we move forward each time.
    """

    frames = []

    for start in range(0, len(samples) - frame_size, hop_size):
        frame = samples[start:start + frame_size]
        frames.append(frame)

    return np.array(frames)