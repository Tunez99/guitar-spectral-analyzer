import streamlit as st

from src.audio.loader import load_audio

from app.tabs.audio_input import audio_input_tab
from app.tabs.waveform import waveform_tab
from app.tabs.transforms import transforms_tab
from app.tabs.filters import filters_tab
from app.tabs.bpm import bpm_tab


def main():
    st.title("DSP Audio Workbench")

    uploaded_file = st.file_uploader(
        "Upload an audio file",
        type=["wav", "flac", "ogg", "mp3"],
    )

    if uploaded_file is None:
        st.info("Upload an audio file to begin.")
        return

    samples, sample_rate = load_audio(uploaded_file)

    audio_tab, waveform_tab_view, transforms_tab_view, filters_tab_view, bpm_tab_view = st.tabs(
        [
            "Audio Input",
            "Waveform",
            "Transforms",
            "Filters",
            "BPM",
        ]
    )

    with audio_tab:
        audio_input_tab(uploaded_file, samples, sample_rate)

    with waveform_tab_view:
        waveform_tab(samples, sample_rate)

    with transforms_tab_view:
        transforms_tab(samples, sample_rate)

    with filters_tab_view:
        filters_tab(samples, sample_rate)

    with bpm_tab_view:
        bpm_tab(samples, sample_rate)


if __name__ == "__main__":
    main()