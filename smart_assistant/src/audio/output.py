# src/audio/output.py
import sounddevice as sd
import soundfile as sf
from pathlib import Path

def play_audio_file(path: str):
    """Play a WAV file through the default output device."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")
    data, samplerate = sf.read(str(path), dtype="float32")
    print(f"Playing audio: {path}")
    sd.play(data, samplerate)
    sd.wait()
