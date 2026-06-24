import numpy as np


def moving_average(samples, window_size):
    if window_size <= 1:
        return samples

    kernel = np.ones(window_size) / window_size
    return np.convolve(samples, kernel, mode="same")


def fft_low_pass(samples, sample_rate, cutoff_hz, transition_width=0):
    spectrum = np.fft.rfft(samples)
    frequencies = np.fft.rfftfreq(len(samples), d=1 / sample_rate)

    response = np.ones_like(frequencies)

    if transition_width <= 0:
        response[frequencies > cutoff_hz] = 0.0
    else:
        start = cutoff_hz
        end = cutoff_hz + transition_width

        response[frequencies >= end] = 0.0

        transition = (frequencies > start) & (frequencies < end)
        response[transition] = 0.5 * (
            1 + np.cos(
                np.pi * (frequencies[transition] - start) / transition_width
            )
        )

    return np.fft.irfft(spectrum * response, n=len(samples))


def fft_high_pass(samples, sample_rate, cutoff_hz, transition_width=0):
    spectrum = np.fft.rfft(samples)
    frequencies = np.fft.rfftfreq(len(samples), d=1 / sample_rate)

    response = np.ones_like(frequencies)

    if transition_width <= 0:
        response[frequencies < cutoff_hz] = 0.0
    else:
        start = cutoff_hz - transition_width
        end = cutoff_hz

        response[frequencies <= start] = 0.0

        transition = (frequencies > start) & (frequencies < end)
        response[transition] = 0.5 * (
            1 - np.cos(
                np.pi * (frequencies[transition] - start) / transition_width
            )
        )

    return np.fft.irfft(spectrum * response, n=len(samples))


def fft_band_pass(
    samples,
    sample_rate,
    low_cutoff_hz,
    high_cutoff_hz,
    transition_width=0,
):
    spectrum = np.fft.rfft(samples)
    frequencies = np.fft.rfftfreq(len(samples), d=1 / sample_rate)

    response = np.ones_like(frequencies)

    if transition_width <= 0:
        response[frequencies < low_cutoff_hz] = 0.0
        response[frequencies > high_cutoff_hz] = 0.0
    else:
        low_start = low_cutoff_hz - transition_width
        low_end = low_cutoff_hz

        high_start = high_cutoff_hz
        high_end = high_cutoff_hz + transition_width

        response[frequencies <= low_start] = 0.0
        response[frequencies >= high_end] = 0.0

        low_transition = (frequencies > low_start) & (frequencies < low_end)
        response[low_transition] = 0.5 * (
            1 - np.cos(
                np.pi
                * (frequencies[low_transition] - low_start)
                / transition_width
            )
        )

        high_transition = (frequencies > high_start) & (frequencies < high_end)
        response[high_transition] = 0.5 * (
            1 + np.cos(
                np.pi
                * (frequencies[high_transition] - high_start)
                / transition_width
            )
        )

    return np.fft.irfft(spectrum * response, n=len(samples))