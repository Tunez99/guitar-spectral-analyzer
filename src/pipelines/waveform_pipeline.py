# src/pipelines/waveform_pipeline.py

from src.audio.conversion import to_mono, normalize
from src.visualisation.waveform import create_waveform_plot


class Waveform:
    def __init__(self):
        pass
    def create_waveform_figure(
        samples,
        sample_rate,
    ):
        samples = normalize(to_mono(samples))

        plot = create_waveform_plot()


        plot.add_waveform(
            samples=samples,
            sample_rate=sample_rate,
            name="Original",
        )

        return plot.get_figure()