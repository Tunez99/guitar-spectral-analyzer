from src.audio.conversion import to_mono, normalize
from src.audio.framing import frame_signal

from src.features.energy import calculate_rms_energy
from src.features.onset import (
    smooth_signal,
    calculate_onset_envelope,
    pick_onset_peaks,
)
from src.features.spectral_flux import calculate_spectral_flux

from src.analysis.bpm import (
    estimate_bpm,
    get_bpm_candidates,
    MIN_BPM,
    MAX_BPM,
)


def run_bpm_pipeline(
    samples,
    sample_rate,
    frame_size=2048,
    hop_size=512,
    min_bpm=MIN_BPM,
    max_bpm=MAX_BPM,
    smoothing_window=5,
    peak_threshold=1.5,
    candidate_count=5,
    onset_method="rms",
):
    mono = to_mono(samples)
    mono = normalize(mono)

    frames = frame_signal(mono, frame_size, hop_size)

    energy = calculate_rms_energy(frames)

    if onset_method == "rms":
        smoothed_energy = smooth_signal(
            energy,
            window_size=smoothing_window,
        )

        onset = calculate_onset_envelope(smoothed_energy)

    elif onset_method == "spectral_flux":
        spectral_flux = calculate_spectral_flux(frames)

        onset = smooth_signal(
            spectral_flux,
            window_size=smoothing_window,
        )

        smoothed_energy = None

    else:
        raise ValueError(f"Unknown onset method: {onset_method}")

    max_onset = max(abs(onset))

    if max_onset > 0:
        onset = onset / max_onset

    onset_peaks = pick_onset_peaks(
        onset,
        threshold_multiplier=peak_threshold,
    )

    bpm, correlation, best_lag = estimate_bpm(
        onset_peaks,
        sample_rate,
        hop_size,
        min_bpm,
        max_bpm,
    )

    candidates = get_bpm_candidates(
        correlation,
        sample_rate,
        hop_size,
        min_bpm,
        max_bpm,
        count=candidate_count,
    )

    return {
        "mono": mono,
        "frames": frames,
        "energy": energy,
        "smoothed_energy": smoothed_energy,
        "onset": onset,
        "onset_peaks": onset_peaks,
        "bpm": bpm,
        "correlation": correlation,
        "best_lag": best_lag,
        "candidates": candidates,
        "settings": {
            "frame_size": frame_size,
            "hop_size": hop_size,
            "min_bpm": min_bpm,
            "max_bpm": max_bpm,
            "smoothing_window": smoothing_window,
            "peak_threshold": peak_threshold,
            "candidate_count": candidate_count,
            "onset_method": onset_method,
        },
    }