import streamlit as st

from src.audio.conversion import to_mono, normalize
from src.audio.signal import (
    moving_average,
    fft_low_pass,
    fft_high_pass,
    fft_band_pass,
)
from src.visualisation.waveform import create_overlay_waveform
from src.visualisation.filters import create_filter_response_plot


PLOT_CONFIG = {
    "scrollZoom": True,
    "displayModeBar": True,
}


def filters_tab(samples, sample_rate):
    st.subheader("Filter Controls")

    mono = normalize(to_mono(samples))

    filter_type = st.selectbox(
        "Filter type",
        [
            "None",
            "Moving Average",
            "FFT Low-pass",
            "FFT High-pass",
            "FFT Band-pass",
        ],
    )

    if filter_type == "None":
        st.session_state["filtered_audio"] = None
        st.session_state["filter_name"] = "None"
        st.info("No filter selected.")
        return

    if filter_type == "Moving Average":
        window_size = st.slider(
            "Window size",
            min_value=1,
            max_value=5000,
            value=100,
            step=10,
        )

        window_ms = 1000 * window_size / sample_rate
        st.write(f"Window: {window_size} samples ({window_ms:.2f} ms)")

        filtered = moving_average(mono, window_size)

        response_fig = create_filter_response_plot(
            filter_type,
            sample_rate,
            window_size=window_size,
            samples=mono,
        )

    elif filter_type == "FFT Low-pass":
        cutoff = st.slider(
            "Cutoff frequency (Hz)",
            min_value=20,
            max_value=sample_rate // 2,
            value=1000,
            step=10,
        )

        smoothing = st.checkbox("Smooth cutoff", value=False)

        transition = 0

        if smoothing:
            transition = st.slider(
                "Transition width (Hz)",
                min_value=10,
                max_value=5000,
                value=500,
                step=10,
            )

        filtered = fft_low_pass(
            mono,
            sample_rate,
            cutoff,
            transition_width=transition,
        )

        response_fig = create_filter_response_plot(
            filter_type,
            sample_rate,
            cutoff=cutoff,
            transition_width=transition,
            samples=mono,
        )

    elif filter_type == "FFT High-pass":
        cutoff = st.slider(
            "Cutoff frequency (Hz)",
            min_value=20,
            max_value=sample_rate // 2,
            value=200,
            step=10,
        )

        smoothing = st.checkbox("Smooth cutoff", value=False)

        transition = 0

        if smoothing:
            transition = st.slider(
                "Transition width (Hz)",
                min_value=10,
                max_value=5000,
                value=500,
                step=10,
            )

        filtered = fft_high_pass(
            mono,
            sample_rate,
            cutoff,
            transition_width=transition,
        )

        response_fig = create_filter_response_plot(
            filter_type,
            sample_rate,
            cutoff=cutoff,
            transition_width=transition,
            samples=mono,
        )

    else:
        low_cutoff = st.slider(
            "Low cutoff frequency (Hz)",
            min_value=20,
            max_value=sample_rate // 2,
            value=200,
            step=10,
        )

        high_cutoff = st.slider(
            "High cutoff frequency (Hz)",
            min_value=20,
            max_value=sample_rate // 2,
            value=3000,
            step=10,
        )

        if low_cutoff >= high_cutoff:
            st.warning("Low cutoff must be below high cutoff.")
            return

        smoothing = st.checkbox("Smooth cutoff", value=False)

        transition = 0

        if smoothing:
            transition = st.slider(
                "Transition width (Hz)",
                min_value=10,
                max_value=5000,
                value=500,
                step=10,
            )

        filtered = fft_band_pass(
            mono,
            sample_rate,
            low_cutoff,
            high_cutoff,
            transition_width=transition,
        )

        response_fig = create_filter_response_plot(
            filter_type,
            sample_rate,
            low_cutoff=low_cutoff,
            high_cutoff=high_cutoff,
            transition_width=transition,
            samples=mono,
        )

    st.session_state["filtered_audio"] = filtered
    st.session_state["filter_name"] = filter_type

    st.subheader("Original Audio")
    st.audio(mono.astype("float32"), sample_rate=sample_rate)

    st.subheader("Filter Shape")
    st.plotly_chart(
        response_fig,
        width="stretch",
        config=PLOT_CONFIG,
    )

    st.subheader("Waveform Comparison")
    fig = create_overlay_waveform(
        original=mono,
        processed=filtered,
        sample_rate=sample_rate,
        title=f"{filter_type}: Original vs Filtered",
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config=PLOT_CONFIG,
    )

    st.subheader("Filtered Audio")
    st.audio(filtered.astype("float32"), sample_rate=sample_rate)