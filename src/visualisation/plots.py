import matplotlib.pyplot as plt


def plot_waveform(times, samples):
    """
    Plot the audio waveform.

    x-axis:
        time in seconds

    y-axis:
        amplitude
    """

    fig, ax = plt.subplots()

    ax.plot(times, samples)
    ax.set_title("Mono Normalized Waveform")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Amplitude")

    return fig


def plot_energy(times, energy):
    """
    Plot RMS energy over time.
    """

    fig, ax = plt.subplots()

    ax.plot(times, energy)
    ax.set_title("RMS Energy")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Energy")

    return fig


def plot_onset_envelope(times, onset):
    """
    Plot positive energy changes over time.
    """

    fig, ax = plt.subplots()

    ax.plot(times, onset)
    ax.set_title("Onset Envelope")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Positive energy change")

    return fig


def plot_autocorrelation(correlation, best_lag):
    """
    Plot autocorrelation and mark the selected lag.

    best_lag:
        The lag chosen as the most likely beat period.
    """

    fig, ax = plt.subplots()

    ax.plot(correlation)
    ax.axvline(best_lag, linestyle="--")
    ax.set_title("Autocorrelation")
    ax.set_xlabel("Lag in frames")
    ax.set_ylabel("Similarity")

    return fig