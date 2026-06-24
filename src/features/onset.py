import numpy as np


def smooth_signal(signal, window_size=5):
    kernel = np.ones(window_size) / window_size
    return np.convolve(signal, kernel, mode="same")


def calculate_onset_envelope(energy):
    onset = []

    previous_energy = energy[0]

    for current_energy in energy:
        change = current_energy - previous_energy
        onset.append(max(change, 0))
        previous_energy = current_energy

    return np.array(onset)


def pick_onset_peaks(onset, threshold_multiplier=1.5):
    threshold = np.mean(onset) + threshold_multiplier * np.std(onset)

    peaks = np.zeros_like(onset)

    for i in range(1, len(onset) - 1):
        is_local_peak = onset[i] > onset[i - 1] and onset[i] > onset[i + 1]
        is_strong = onset[i] > threshold

        if is_local_peak and is_strong:
            peaks[i] = onset[i]

    return peaks
