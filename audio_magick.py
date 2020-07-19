from pydub import AudioSegment
import io
import pathlib
import os


def save_voice_to_wav(path, data, frame_rate=16000):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    print(os.listdir())
    audio = AudioSegment.from_file(io.BytesIO(data))
    audio = audio.set_frame_rate(frame_rate)
    audio.export(path, format='wav')
