def get_audio_duration(samples, sample_rate):
    return len(samples) / sample_rate


def select_audio_segment(samples, sample_rate, start_time, end_time):
    start_sample = int(start_time * sample_rate)
    end_sample = int(end_time * sample_rate)

    start_sample = max(0, start_sample)
    end_sample = min(len(samples), end_sample)

    return samples[start_sample:end_sample]