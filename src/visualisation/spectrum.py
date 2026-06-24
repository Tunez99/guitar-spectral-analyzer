import numpy as np
import plotly.graph_objects as go


def create_spectrum_comparison_plot(
    original,
    processed,
    sample_rate,
    max_frequency=None,
    title="Frequency Spectrum Comparison",
):
    original_freqs, original_magnitude = _compute_magnitude_spectrum(
        original,
        sample_rate,
    )

    processed_freqs, processed_magnitude = _compute_magnitude_spectrum(
        processed,
        sample_rate,
    )

    removed_magnitude = np.maximum(
        original_magnitude - processed_magnitude,
        0.0,
    )

    if max_frequency is None:
        max_frequency = sample_rate / 2

    mask = original_freqs <= max_frequency

    fig = go.Figure()

    fig.add_trace(
        go.Scattergl(
            x=original_freqs[mask],
            y=original_magnitude[mask],
            mode="lines",
            name="Original spectrum",
            opacity=0.35,
        )
    )

    fig.add_trace(
        go.Scattergl(
            x=processed_freqs[mask],
            y=processed_magnitude[mask],
            mode="lines",
            name="Filtered spectrum",
        )
    )

    fig.add_trace(
        go.Scattergl(
            x=original_freqs[mask],
            y=removed_magnitude[mask],
            mode="lines",
            name="Removed content",
            opacity=0.75,
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Frequency (Hz)",
        yaxis_title="Magnitude (dB)",
        hovermode="x unified",
        dragmode="zoom",
    )

    fig.update_xaxes(
        range=[0, max_frequency],
        minallowed=0,
        maxallowed=sample_rate / 2,
        fixedrange=False,
    )

    fig.update_yaxes(
        fixedrange=False,
    )

    return fig


def _compute_magnitude_spectrum(samples, sample_rate):
    samples = np.asarray(samples)

    if len(samples) == 0:
        return np.array([]), np.array([])

    window = np.hanning(len(samples))
    windowed = samples * window

    spectrum = np.fft.rfft(windowed)
    frequencies = np.fft.rfftfreq(len(samples), d=1 / sample_rate)

    magnitude = np.abs(spectrum)

    magnitude_db = 20 * np.log10(magnitude + 1e-12)

    magnitude_db = magnitude_db - np.max(magnitude_db)

    return frequencies, magnitude_db