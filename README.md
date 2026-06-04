# Guitar Spectral Analyzer

A Python-based audio analysis tool designed to assist guitarists in understanding and transcribing music through signal processing and spectral analysis.

## Motivation

Many niche or independent songs have no available tabs, chord charts, or tutorials. Learning these songs often requires transcription by ear, which can be difficult and time-consuming.

This project aims to provide visual and analytical tools that help musicians understand what is happening in a recording by analysing its frequency content, dynamics, and musical structure.

Rather than attempting to automatically generate perfect guitar tabs, the goal is to create an interactive analysis platform that assists the transcription process.

## Features

### Current Features

* Audio file loading
* Waveform visualization
* STFT spectrogram generation
* RMS loudness analysis
* Interactive Streamlit interface

### Planned Features

* Spectral centroid (brightness/tone analysis)
* Spectral rolloff analysis
* Chroma feature extraction
* Pitch detection
* Octave/register analysis
* Chord candidate detection
* Onset and transient detection
* Section segmentation
* Guitar-specific transcription assistance

### Future Work

* Machine learning-based chord classification
* Playing style recognition
* Tone comparison between recordings
* Fretboard position suggestions
* Automatic transcription assistance

## Technologies

* Python
* Streamlit
* NumPy
* Librosa
* Matplotlib
* SciPy

## Signal Processing Concepts

This project explores several Digital Signal Processing (DSP) techniques including:

* Fourier Transform (FFT)
* Short-Time Fourier Transform (STFT)
* Constant-Q Transform (CQT)
* Spectrogram Analysis
* Harmonic Analysis
* Time-Frequency Representations
* Spectral Features
* Loudness and Dynamic Analysis

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd guitar-spectral-analyzer
```

Run the startup script:

```bash
./run.sh
```

The script will:

1. Create a Python virtual environment if required
2. Install all dependencies
3. Launch the Streamlit application

## Usage

Launch the application and upload an audio file.

The analyzer will generate:

* Audio waveform
* Frequency spectrogram
* Loudness profile
* Additional analysis metrics as features are added

## Project Structure

```text
guitar-spectral-analyzer/
│
├── app.py
├── requirements.txt
├── run.sh
├── README.md
└── .gitignore
```

## Limitations

Music transcription is a difficult problem due to:

* Multiple instruments occupying similar frequency ranges
* Guitar harmonics and overtones
* Distortion effects
* Alternate tunings
* Ambiguous fretboard positions
* Recording and mixing variations

As a result, this project is intended as a transcription aid rather than a complete automatic tab generation system.

## Author

Created as a personal exploration of signal processing, music analysis, and software engineering.
