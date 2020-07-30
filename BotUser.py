from audio_magick import save_voice_to_wav
from image_magick import save_img


class BotUser:
    """
    User class and database record
    Stored in shelve database
    """
    def __init__(self, id):
        self.id = str(id)
        self.records = []
        self.imgs = []
        self.record_id = 0
        self.img_id = 0

    @staticmethod
    def _audio_name(audio_id):
        """
        Convenience function to generate name from id
        """
        return f'audio_message_{audio_id}.wav'

    def _audio_path(self, audio_id):
        """
        Convenience function to generate path from id
        """
        return fr'.\{self.id}\{self._audio_name(audio_id)}'

    @staticmethod
    def _img_name(img_id):
        """
        Convenience function to generate name from id
        """
        return f'face_img_{img_id}.png'

    def _image_path(self, img_id):
        """
        Convenience function to generate path from id
        """
        return fr'.\{self.id}\{self._img_name(img_id)}'

    def get_audio(self, audio_id):
        """
        Get audio file by id
        """
        return open(self._audio_path(audio_id), 'rb')

    def add_voice(self, voice):
        """
        Save audio file
        """
        save_voice_to_wav(self._audio_path(self.record_id), voice)
        self.records.append(self._audio_name(self.record_id))
        self.record_id += 1

    def add_image(self, img):
        """
        Save image
        """
        save_img(self._image_path(self.img_id), img)
        self.imgs.append(self._img_name(self.img_id))
        self.img_id += 1
