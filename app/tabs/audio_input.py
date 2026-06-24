import streamlit as st


def audio_input_tab(uploaded_file, samples, sample_rate):
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