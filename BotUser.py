from audio_magick import save_voice_to_wav


class BotUser:
    def __init__(self, id):
        self.id = str(id)
        self.records = []
        self.record_id = 0

    def _audio_name(self, id):
        return f'audio_message_{id}.wav'

    def _audio_path(self, id):
        return fr'.\{self.id}\{self._audio_name(id)}'

    def get_audio(self, id):
        return open(self._audio_path(id), 'rb')

    def add_voice(self, voice):
        save_voice_to_wav(self._audio_path(self.record_id), voice)
        self.records.append(self._audio_name(self.record_id))
        self.record_id += 1

    def add_image(self, image):
        pass
