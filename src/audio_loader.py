import librosa


class AudioLoader:
    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file
        self.audio = None
        self.sample_rate = None

    def load(self):
        self.audio, self.sample_rate = librosa.load(
            self.uploaded_file,
            sr=None,
            mono=True
        )
        return self.audio, self.sample_rate

    def get_duration(self):
        if self.audio is None or self.sample_rate is None:
            return 0
        return len(self.audio) / self.sample_rate