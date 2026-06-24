import numpy as np


def calculate_spectral_flux(frames):
    """
    Calculate spectral flux from framed audio.

    Spectral flux measures how much the frequency content changes
    from one frame to the next.

    This is often better for beat/onset detection than RMS energy alone.
    """

    flux = []

    previous_spectrum = None

    for frame in frames:
        spectrum = np.abs(np.fft.rfft(frame))

        if previous_spectrum is None:
            flux.append(0)
        else:
            change = spectrum - previous_spectrum
            positive_change = np.maximum(change, 0)
            flux.append(np.sum(positive_change))

        previous_spectrum = spectrum

    return np.array(flux)