import numpy as np
import plotly.graph_objects as go


def create_filter_response_plot(
    filter_type,
    sample_rate,
    window_size=None,
    cutoff=None,
    low_cutoff=None,
    high_cutoff=None,
    transition_width=0,
    points=2000,
    samples=None,
):
    nyquist = sample_rate / 2
    frequencies = np.linspace(0, nyquist, points)

    if filter_type == "Moving Average":
        if window_size is None:
            raise ValueError("window_size is required for Moving Average")

        response = _moving_average_response(
            frequencies,
            sample_rate,
            window_size,
        )

        title = f"Moving Average Filter Response ({window_size} samples)"

    elif filter_type == "FFT Low-pass":
        if cutoff is None:
            raise ValueError("cutoff is required for FFT Low-pass")

        response = _low_pass_response(
            frequencies,
            cutoff,
            transition_width,
        )

        title = _make_title(
            "FFT Low-pass Response",
            f"{cutoff} Hz cutoff",
            transition_width,
        )

    elif filter_type == "FFT High-pass":
        if cutoff is None:
            raise ValueError("cutoff is required for FFT High-pass")

        response = _high_pass_response(
            frequencies,
            cutoff,
            transition_width,
        )

        title = _make_title(
            "FFT High-pass Response",
            f"{cutoff} Hz cutoff",
            transition_width,
        )

    elif filter_type == "FFT Band-pass":
        if low_cutoff is None or high_cutoff is None:
            raise ValueError(
                "low_cutoff and high_cutoff are required for FFT Band-pass"
            )

        response = _band_pass_response(
            frequencies,
            low_cutoff,
            high_cutoff,
            transition_width,
        )

        title = _make_title(
            "FFT Band-pass Response",
            f"{low_cutoff} Hz → {high_cutoff} Hz",
            transition_width,
        )

    else:
        raise ValueError(f"Unknown filter type: {filter_type}")

    fig = go.Figure()

    if samples is not None:
        spectrum_frequencies, spectrum_magnitude = _compute_normalized_spectrum(
            samples,
            sample_rate,
            max_points=5000,
        )

        fig.add_trace(
            go.Scattergl(
                x=spectrum_frequencies,
                y=spectrum_magnitude,
                mode="lines",
                name="Audio spectrum",
                opacity=0.3,
            )
        )

    fig.add_trace(
        go.Scattergl(
            x=frequencies,
            y=response,
            mode="lines",
            name="Filter response",
            line=dict(width=3),
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Frequency (Hz)",
        yaxis_title="Magnitude / response",
        hovermode="x unified",
        dragmode="zoom",
    )

    fig.update_xaxes(
        range=[0, nyquist],
        minallowed=0,
        maxallowed=nyquist,
        fixedrange=False,
    )

    fig.update_yaxes(
        range=[-0.05, 1.05],
        fixedrange=True,
    )

    return fig


def _compute_normalized_spectrum(samples, sample_rate, max_points=5000):
    samples = np.asarray(samples)

    if len(samples) == 0:
        return np.array([]), np.array([])

    window = np.hanning(len(samples))
    spectrum = np.fft.rfft(samples * window)
    frequencies = np.fft.rfftfreq(len(samples), d=1 / sample_rate)

    magnitude = np.abs(spectrum)
    magnitude_db = 20 * np.log10(magnitude + 1e-12)

    magnitude_db = magnitude_db - np.max(magnitude_db)

    magnitude_normalized = np.clip((magnitude_db + 80) / 80, 0, 1)

    if len(frequencies) > max_points:
        step = max(1, len(frequencies) // max_points)
        frequencies = frequencies[::step]
        magnitude_normalized = magnitude_normalized[::step]

    return frequencies, magnitude_normalized

def _low_pass_response(frequencies, cutoff, transition_width):
    if transition_width <= 0:
        return np.where(frequencies <= cutoff, 1.0, 0.0)

    response = np.ones_like(frequencies)

    start = cutoff
    end = cutoff + transition_width

    response[frequencies >= end] = 0.0

    transition = (frequencies > start) & (frequencies < end)
    response[transition] = 0.5 * (
        1
        + np.cos(
            np.pi
            * (frequencies[transition] - start)
            / transition_width
        )
    )

    return response


def _high_pass_response(frequencies, cutoff, transition_width):
    if transition_width <= 0:
        return np.where(frequencies >= cutoff, 1.0, 0.0)

    response = np.ones_like(frequencies)

    start = cutoff - transition_width
    end = cutoff

    response[frequencies <= start] = 0.0

    transition = (frequencies > start) & (frequencies < end)
    response[transition] = 0.5 * (
        1
        - np.cos(
            np.pi
            * (frequencies[transition] - start)
            / transition_width
        )
    )

    return response


def _band_pass_response(
    frequencies,
    low_cutoff,
    high_cutoff,
    transition_width,
):
    if transition_width <= 0:
        return np.where(
            (frequencies >= low_cutoff) & (frequencies <= high_cutoff),
            1.0,
            0.0,
        )

    response = np.ones_like(frequencies)

    low_start = low_cutoff - transition_width
    low_end = low_cutoff

    high_start = high_cutoff
    high_end = high_cutoff + transition_width

    response[frequencies <= low_start] = 0.0
    response[frequencies >= high_end] = 0.0

    low_transition = (frequencies > low_start) & (frequencies < low_end)
    response[low_transition] = 0.5 * (
        1
        - np.cos(
            np.pi
            * (frequencies[low_transition] - low_start)
            / transition_width
        )
    )

    high_transition = (frequencies > high_start) & (frequencies < high_end)
    response[high_transition] = 0.5 * (
        1
        + np.cos(
            np.pi
            * (frequencies[high_transition] - high_start)
            / transition_width
        )
    )

    return response


def _moving_average_response(frequencies, sample_rate, window_size):
    normalized_frequency = frequencies / sample_rate

    numerator = np.sin(np.pi * normalized_frequency * window_size)
    denominator = window_size * np.sin(np.pi * normalized_frequency)

    response = np.abs(
        np.divide(
            numerator,
            denominator,
            out=np.ones_like(numerator),
            where=np.abs(denominator) > 1e-12,
        )
    )

    response[0] = 1.0

    return response


def _make_title(base, detail, transition_width):
    if transition_width > 0:
        return f"{base} ({detail}, {transition_width} Hz transition)"

    return f"{base} ({detail})"