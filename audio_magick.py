import pydub
from pydub import AudioSegment
import io


def save_voice(name, data, format='wav', bitrate='16k'):
    audio = AudioSegment.from_file(io.BytesIO(data))
    audio.export(name, format=format, bitrate=bitrate)


def save_voice_to_wav(name, data, frame_rate=16000):
    audio = AudioSegment.from_file(io.BytesIO(data))
    audio = audio.set_frame_rate(frame_rate)
    audio.export(name, format='wav')
