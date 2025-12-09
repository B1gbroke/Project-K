# src/audio/input.py
import sounddevice as sd
import soundfile as sf
from pathlib import Path
from src.core.config import config

def record_to_file(output_path: str):
    """Record a short clip from the selected input device and save as WAV."""
    duration = config.RECORD_SECONDS
    sample_rate = config.SAMPLE_RATE
    channels = config.CHANNELS
    
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Recording {duration} seconds of audio...")
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=channels,
        dtype="float32",
        device=config.INPUT_DEVICE_INDEX,  # <-- NEW
    )
    sd.wait()
    sf.write(output_path, audio, sample_rate)
    print(f"Saved recording to {output_path}")
