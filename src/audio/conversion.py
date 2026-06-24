import numpy as np


def to_mono(samples):
    """
    Convert audio to mono.

    For stereo, we average left and right channels.
    """

    if samples.ndim == 1:
        return samples

    return np.mean(samples, axis=0)


def normalize(samples):
    """
    Scale audio so the largest absolute value becomes 1.

    This makes loud and quiet files easier to compare.
    """

    max_value = np.max(np.abs(samples))

    if max_value == 0:
        return samples

    return samples / max_value