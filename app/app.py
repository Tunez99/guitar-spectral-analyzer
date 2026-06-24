import streamlit as st
import numpy as np

from src.audio.loader import load_audio
from src.audio.conversion import to_mono, normalize
from src.audio.framing import frame_signal

from src.pipelines.bpm_pipeline import run_bpm_pipeline

from src.visualisation.plots import (
    plot_waveform,
    plot_energy,
    plot_onset_envelope,
    plot_autocorrelation,
)


def display_audio_info(uploaded_file, samples, sample_rate):
    st.subheader("Audio Playback")
    st.audio(uploaded_file)

    st.subheader("File Information")
    st.write("Sample rate:", sample_rate)
    st.write("Sample array shape:", samples.shape)
    st.write("Sample data type:", samples.dtype)

    if samples.ndim == 1:
        number_of_samples = samples.shape[0]
        st.write("Channels: mono")

    elif samples.ndim == 2:
        number_of_samples = samples.shape[1]
        st.write("Channels:", samples.shape[0])

    else:
        st.error("Unsupported audio shape.")
        return

    duration_seconds = number_of_samples / sample_rate

    st.write("Number of samples:", number_of_samples)
    st.write("Duration:", round(duration_seconds, 2), "seconds")


def get_bpm_settings():
    st.subheader("BPM Settings")

    frame_size = st.slider("Frame size", 256, 8192, 2048, step=256)
    hop_size = st.slider("Hop size", 128, 4096, 512, step=128)

    min_bpm = st.slider("Minimum BPM", 40, 140, 80)
    max_bpm = st.slider("Maximum BPM", 120, 260, 180)

    onset_method = st.selectbox(
        "Onset Method",
        ["rms", "spectral_flux"]
    )

    return (
        frame_size,
        hop_size,
        min_bpm,
        max_bpm,
        onset_method,
    )
    
def display_bpm_results(results):
    st.subheader("BPM Estimation")

    st.metric("Estimated BPM", round(results["bpm"], 2))
    st.write("Best lag:", results["best_lag"])

def display_bpm_candidates(results):
    st.subheader("Potential BPMs")

    candidate_rows = []

    for index, candidate in enumerate(results["candidates"], start=1):
        candidate_rows.append({
            "Rank": index,
            "BPM": round(candidate["bpm"], 2),
            "Lag": candidate["lag"],
            "Strength": round(candidate["strength"], 4),
        })

    st.dataframe(candidate_rows, hide_index=True)

def display_plots(results, sample_rate, hop_size):
    st.subheader("Plots")

    mono = results["mono"]
    energy = results["energy"]
    onset = results["onset"]
    onset_peaks = results["onset_peaks"]
    correlation = results["correlation"]
    best_lag = results["best_lag"]

    time_waveform = np.arange(len(mono)) / sample_rate
    time_frames = np.arange(len(energy)) * hop_size / sample_rate

    st.pyplot(plot_waveform(time_waveform, mono))
    st.pyplot(plot_energy(time_frames, energy))
    st.pyplot(plot_onset_envelope(time_frames, onset))
    st.pyplot(plot_onset_envelope(time_frames, onset_peaks))
    st.pyplot(plot_autocorrelation(correlation, best_lag))


def main():
    st.title("DSP Audio Analysis")

    uploaded_file = st.file_uploader(
        "Upload an audio file",
        type=["wav", "flac", "ogg", "mp3"],
    )

    if uploaded_file is None:
        st.info("Upload an audio file to begin.")
        return

    samples, sample_rate = load_audio(uploaded_file)

    display_audio_info(uploaded_file, samples, sample_rate)

    frame_size, hop_size, min_bpm, max_bpm, onset_method = get_bpm_settings()

    results = run_bpm_pipeline(
        samples,
        sample_rate,
        frame_size,
        hop_size,
        min_bpm,
        max_bpm,
        onset_method=onset_method,
    )

    display_bpm_results(results)
    display_bpm_candidates(results)
    display_plots(results, sample_rate, hop_size)


if __name__ == "__main__":
    main()