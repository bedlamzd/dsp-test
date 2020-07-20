from pydub import AudioSegment
import io
import pathlib


def save_voice_to_wav(path, data, frame_rate=16000):
    """
    Converts audio to wav format
    :param path: where to save
    :param data: audio file
    :param frame_rate: in Hz
    :return:
    """
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    audio = AudioSegment.from_file(io.BytesIO(data))
    audio = audio.set_frame_rate(frame_rate)
    audio.export(path, format='wav')
