import streamlit as st

from src.audio.conversion import to_mono, normalize
from src.audio.selection import (
    get_audio_duration,
    select_audio_segment,
)
from src.visualisation.waveform import (
    create_interactive_waveform,
    create_overlay_waveform,
)


PLOT_CONFIG = {
    "scrollZoom": True,
    "displayModeBar": True,
}


def display_plot(fig):
    st.plotly_chart(
        fig,
        width="stretch",
        config=PLOT_CONFIG,
    )


def waveform_tab(samples, sample_rate):
    st.subheader("Waveform Explorer")

    mono = normalize(to_mono(samples))
    duration = get_audio_duration(mono, sample_rate)

    filtered = st.session_state.get("filtered_audio")
    filter_name = st.session_state.get("filter_name", "None")
    st.write("Filter active:", filtered is not None, filter_name)
    
    st.write("Drag horizontally to zoom on the time axis. Double-click to reset.")

    st.subheader("Full Track")

    max_points = st.slider(
        "Display resolution",
        min_value=5_000,
        max_value=200_000,
        value=50_000,
        step=5_000,
    )

    if filtered is not None:
        full_fig = create_overlay_waveform(
            original=mono,
            processed=filtered,
            sample_rate=sample_rate,
            max_points=max_points,
            title=f"Full Waveform: Original vs {filter_name}",
        )
    else:
        full_fig = create_interactive_waveform(
            mono,
            sample_rate,
            max_points=max_points,
            title="Full Waveform",
        )

    display_plot(full_fig)

    st.subheader("Selected Window")

    zoom_preset = st.selectbox(
        "Window size",
        ["1 second", "5 seconds", "10 seconds", "30 seconds", "Custom"],
        index=2,
    )

    if zoom_preset == "1 second":
        window_size = 1.0
    elif zoom_preset == "5 seconds":
        window_size = 5.0
    elif zoom_preset == "10 seconds":
        window_size = 10.0
    elif zoom_preset == "30 seconds":
        window_size = 30.0
    else:
        window_size = st.number_input(
            "Custom window size in seconds",
            min_value=0.1,
            max_value=float(duration),
            value=min(10.0, float(duration)),
            step=0.1,
        )

    window_size = min(window_size, duration)
    max_start = max(0.0, duration - window_size)

    start_mode = st.selectbox(
        "Start time mode",
        ["Audio Start", "Slider", "Manual Input"],
        index=0,
    )

    if start_mode == "Audio Start":
        start_time = 0.0

    elif start_mode == "Slider":
        start_time = st.slider(
            "Start time in seconds",
            min_value=0.0,
            max_value=float(max_start),
            value=0.0,
            step=0.1,
        )

    else:
        start_time = st.number_input(
            "Start time in seconds",
            min_value=0.0,
            max_value=float(max_start),
            value=0.0,
            step=0.1,
        )

    end_time = min(start_time + window_size, duration)

    st.write(f"Selected range: {start_time:.2f}s → {end_time:.2f}s")

    segment = select_audio_segment(
        mono,
        sample_rate,
        start_time,
        end_time,
    )

    filtered_segment = None

    if filtered is not None:
        filtered_segment = select_audio_segment(
            filtered,
            sample_rate,
            start_time,
            end_time,
        )

    if filtered_segment is not None:
        segment_fig = create_overlay_waveform(
            original=segment,
            processed=filtered_segment,
            sample_rate=sample_rate,
            max_points=max_points,
            title=f"Selected Window: Original vs {filter_name}",
        )
    else:
        segment_fig = create_interactive_waveform(
            segment,
            sample_rate,
            max_points=max_points,
            title="Selected Waveform Window",
        )

    display_plot(segment_fig)

    st.subheader("Selected Audio Playback")

    if filtered_segment is not None:
        playback_mode = st.radio(
            "Playback",
            ["Original", "Filtered"],
            horizontal=True,
        )

        if playback_mode == "Filtered":
            st.audio(filtered_segment.astype("float32"), sample_rate=sample_rate)
        else:
            st.audio(segment.astype("float32"), sample_rate=sample_rate)
    else:
        st.audio(segment.astype("float32"), sample_rate=sample_rate)