import numpy as np
import plotly.graph_objects as go


def _downsample(samples, sample_rate, max_points):
    samples = np.asarray(samples)
    length = len(samples)

    if length == 0:
        return np.array([]), np.array([])

    if length > max_points:
        step = max(1, length // max_points)
        samples = samples[::step]
        time = np.arange(0, length, step)[: len(samples)] / sample_rate
    else:
        time = np.arange(length) / sample_rate

    return time, samples


def _downsample_pair(original, processed, sample_rate, max_points):
    original = np.asarray(original)
    processed = np.asarray(processed)

    length = min(len(original), len(processed))

    if length == 0:
        return np.array([]), np.array([]), np.array([]), 0.0

    original = original[:length]
    processed = processed[:length]

    if length > max_points:
        step = max(1, length // max_points)
        original = original[::step]
        processed = processed[::step]
        time = np.arange(0, length, step)[: len(original)] / sample_rate
    else:
        time = np.arange(length) / sample_rate

    duration = length / sample_rate

    return time, original, processed, duration


def _apply_waveform_layout(fig, title, duration):
    fig.update_layout(
        title=title,
        xaxis_title="Time (seconds)",
        yaxis_title="Amplitude",
        hovermode="x unified",
        dragmode="zoom",
    )

    fig.update_xaxes(
        range=[0, duration],
        minallowed=0,
        maxallowed=duration,
        rangeslider=dict(
            visible=True,
            range=[0, duration],
        ),
        fixedrange=False,
        type="linear",
    )

    fig.update_yaxes(
        fixedrange=True,
    )

    return fig


def create_interactive_waveform(
    samples,
    sample_rate,
    max_points=50_000,
    title="Waveform",
):
    samples = np.asarray(samples)
    time, display_samples = _downsample(samples, sample_rate, max_points)

    duration = len(samples) / sample_rate if sample_rate > 0 else 0.0

    fig = go.Figure()

    fig.add_trace(
        go.Scattergl(
            x=time,
            y=display_samples,
            mode="lines",
            name="Waveform",
        )
    )

    return _apply_waveform_layout(fig, title, duration)


def create_overlay_waveform(
    original,
    processed,
    sample_rate,
    max_points=50_000,
    title="Waveform Comparison",
):
    time, display_original, display_processed, duration = _downsample_pair(
        original,
        processed,
        sample_rate,
        max_points,
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scattergl(
            x=time,
            y=display_original,
            mode="lines",
            name="Original",
            opacity=0.35,
            line=dict(width=1),
        )
    )

    fig.add_trace(
        go.Scattergl(
            x=time,
            y=display_processed,
            mode="lines",
            name="Filtered Audio",
            opacity=0.95,
            line=dict(width=2),
        )
    )

    return _apply_waveform_layout(fig, title, duration)