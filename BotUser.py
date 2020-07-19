from audio_magick import save_voice_to_wav


class BotUser:
    def __init__(self, id):
        self.id = str(id)
        self.records = []
        self.record_id = 0

    def add_voice(self, voice):
        voice_name = f'audio_message_{self.record_id}.wav'
        self.record_id += 1
        save_voice_to_wav(fr'.\{self.id}\{voice_name}', voice)
        self.records.append(voice_name)

    def add_image(self, image):
        pass
