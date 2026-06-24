import librosa
import numpy as np


def load_audio(file):
    """
    Load an audio file and return signal data

    Uses soundfile library to return information
    
    Parameters:
        file: The uploaded file from Streamlit, or file path
        
    Returns:
        samples: 
            A NumPy arrary containing the audio waveform
            
            Shape depends on audio
            - Mono audio (num_samples,)
            - Stereo audio: (num_samples, num_channels)
        Sample_rate:
            The number of audio samples per second
    """

    # Read the sound file and return into
    samples, sample_rate = librosa.load(
        file,
        sr=None,
        mono=False
    )

    # Make sure samples are float values
    # Use 32 for now as we will investigate accuracy later
    samples = samples.astype(np.float32)

    # Return the waveform and sample rate
    return samples, sample_rate