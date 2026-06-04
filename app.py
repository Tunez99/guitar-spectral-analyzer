import streamlit as st
from src import AudioLoader, AudioAnalyzer, AudioVisualizer

st.title("Guitar Spectral Analyzer")

uploaded_file = st.file_uploader(
    "Upload an audio file",
    type=["wav", "mp3", "flac", "ogg"]
)

if uploaded_file:
    st.audio(uploaded_file)

    loader = AudioLoader(uploaded_file)
    audio, sample_rate = loader.load()

    st.write(f"Sample Rate: {sample_rate}")
    st.write(f"Samples: {len(audio)}")
    st.write(f"Duration: {loader.get_duration():.2f} seconds")

    analyzer = AudioAnalyzer(audio, sample_rate)
    visualizer = AudioVisualizer(audio, sample_rate)

    st.subheader("Waveform")
    st.pyplot(visualizer.plot_waveform())

    st.subheader("Spectrogram")
    spectrogram_db = analyzer.get_stft_spectrogram()
    st.pyplot(visualizer.plot_spectrogram(spectrogram_db))

    st.subheader("Loudness Over Time")
    times, rms = analyzer.get_rms_loudness()
    st.pyplot(visualizer.plot_loudness(times, rms))