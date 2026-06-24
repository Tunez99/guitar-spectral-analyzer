import numpy as np


MIN_BPM = 80
MAX_BPM = 180

TEMPO_MULTIPLIERS = [
    1,
    2,
    0.5,
    1.5,
    2 / 3,
]

def bpm_to_lag(bpm, sample_rate, hop_size):
    seconds_per_beat = 60 / bpm
    return round(seconds_per_beat * sample_rate / hop_size)


def get_correlation_at_bpm(correlation, bpm, sample_rate, hop_size):
    lag = bpm_to_lag(bpm, sample_rate, hop_size)

    return {
        "bpm": bpm,
        "lag": lag,
        "strength": correlation[lag],
    }
    
def estimate_bpm(
    onset_envelope,
    sample_rate,
    hop_size,
    min_bpm=MIN_BPM,
    max_bpm=MAX_BPM,
):
    onset_centered = onset_envelope - np.mean(onset_envelope)

    correlation = np.correlate(
        onset_centered,
        onset_centered,
        mode="full",
    )

    correlation = correlation[len(correlation) // 2:]

    min_lag, max_lag = bpm_range_to_lag_range(
        sample_rate,
        hop_size,
        min_bpm,
        max_bpm,
    )

    search_area = correlation[min_lag:max_lag]

    best_lag = np.argmax(search_area) + min_lag

    bpm = lag_to_bpm(best_lag, sample_rate, hop_size)

    return bpm, correlation, best_lag


def get_bpm_candidates(
    correlation,
    sample_rate,
    hop_size,
    min_bpm=MIN_BPM,
    max_bpm=MAX_BPM,
    count=5,
):
    min_lag, max_lag = bpm_range_to_lag_range(
        sample_rate,
        hop_size,
        min_bpm,
        max_bpm,
    )

    search_area = correlation[min_lag:max_lag]
    max_strength = np.max(search_area)
    top_indices = np.argsort(search_area)[-count:][::-1]

    candidates = []

    for index in top_indices:
        lag = index + min_lag

        candidates.append({
            "bpm": lag_to_bpm(lag, sample_rate, hop_size),
            "lag": lag,
            "strength": correlation[lag] / max_strength,
        })

    return candidates


def bpm_range_to_lag_range(sample_rate, hop_size, min_bpm, max_bpm):
    min_lag = int((60 / max_bpm) * sample_rate / hop_size)
    max_lag = int((60 / min_bpm) * sample_rate / hop_size)

    return min_lag, max_lag


def lag_to_bpm(lag, sample_rate, hop_size):
    seconds_per_beat = lag * hop_size / sample_rate
    return 60 / seconds_per_beat


# ------------------------------------------------------------
# Benchmark / comparison helpers
# ------------------------------------------------------------

def best_tempo_match(estimated_bpm, known_bpm):
    adjusted_candidates = []

    for multiplier in TEMPO_MULTIPLIERS:
        adjusted_candidates.append(estimated_bpm * multiplier)

    best_bpm = min(
        adjusted_candidates,
        key=lambda bpm: abs(bpm - known_bpm),
    )

    error = abs(best_bpm - known_bpm)

    return best_bpm, error


def best_candidate_tempo_match(candidates, known_bpm):
    best_match = None

    for candidate in candidates:
        adjusted_bpm, adjusted_error = best_tempo_match(
            candidate["bpm"],
            known_bpm,
        )

        match = {
            "raw_bpm": candidate["bpm"],
            "adjusted_bpm": adjusted_bpm,
            "adjusted_error": adjusted_error,
            "lag": candidate["lag"],
            "strength": candidate["strength"],
        }

        if best_match is None:
            best_match = match
        elif match["adjusted_error"] < best_match["adjusted_error"]:
            best_match = match

    return best_match