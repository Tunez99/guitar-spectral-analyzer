# Change Log
This is not intended to be a traditional change log. Instead, it serves as a record of development decisions, observations, discoveries, and the thought process behind the project. As the application matures, both the project structure and documentation will be refined.

# 23/06/2026
Today was the first day exploring the project and the broader problem of BPM detection. AI was used heavily as a learning and research tool to explore possible approaches, DSP concepts, and implementation strategies.

The current implementation performs reasonably well across most benchmark tracks; however, one test case consistently produces an incorrect BPM estimate. Comparisons between RMS-based onset detection, spectral flux, and Librosa's built-in beat tracking all produced similar incorrect results. This suggests that the issue is not simply a bug in the implementation, but may instead relate to how rhythmic information is being represented and extracted from the signal.

Investigating this problem has highlighted a significant gap in my understanding of Digital Signal Processing. Rather than continuing to iterate blindly on BPM algorithms, the project has shifted toward a research-focused approach. The goal is now to understand the underlying DSP concepts that influence tempo detection before attempting further improvements.

Topics identified for further study include:

Time-domain vs frequency-domain analysis
Convolution
Digital filtering
Envelope detection
Spectral analysis
Z-transforms
Onset detection techniques
Beat tracking methodologies

A key observation from today's work is that BPM detection is not a single problem but a collection of smaller signal-processing problems. Future development will focus on understanding and visualising intermediate processing stages rather than solely pursuing a final BPM estimate.

Short-term goals:

Improve visualisation of intermediate signal transformations.
Display and compare feature extraction methods more clearly.
Visualise onset detection and peak selection.
Develop a stronger understanding of time-domain and frequency-domain representations.
Explore why different onset detection methods converge on similar BPM estimates for problematic tracks.

The immediate focus will be building intuition around DSP fundamentals before expanding the BPM detection system further.

# 24/06/2026
Today was very big, focused on implementation with some basic DSP ideology behind it, with a focus on UI and plotting, then implementing some basic filters. 

It's abit unintuitive still, but its building. We can take note of how the waveform transforms with applied filters. Due to lack of technical knowledge, we will aim to follow through with the following approach. 

1. Read through the codebase
2. Add comments
3. Update documentation -> Research Specifically
4. Write down what each visualisation should teach
5. Implement spectrum visualisations

I want to improve filtering first and create a ideal workflow, this may involve some refactoring to help modularise the application from this point to allow easier access to changes. We also want to reduce duplicate code and try have plots be callable for various different methods later. I also want to explore sampling, specifically averaging of samples with visualisation and ideology behind these implementations. This should help progress both understanding, modularised code, and future implementation.

# 26/06/2026
Now that i have a better idea of what I want to build, the next few days will be dedicated to learning architecure and reading the streamlit documentation so i can avoid entanglment in code and help streamline my work process. Once we set up a system I imagine continued exploration of DSP will become easier.