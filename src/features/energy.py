import numpy as np

def calculate_rms_energy(frames):
    energy = []

    for frame in frames:
        rms = np.sqrt(np.mean(frame ** 2))
        energy.append(rms)

    return np.array(energy)

