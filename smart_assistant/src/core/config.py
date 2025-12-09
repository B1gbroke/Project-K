# src/core/config.py
from dataclasses import dataclass

@dataclass
class Config:
    # Audio settings
    SAMPLE_RATE: int = 16000
    CHANNELS: int = 1
    RECORD_SECONDS: int = 5

    # Set this to the working USB mic index from sd.query_devices()
    INPUT_DEVICE_INDEX: int = 1  # change if needed

    # Backends
    STT_BACKEND: str = "whisper_local"   # local Whisper
    LLM_BACKEND: str = "ollama"          # use Ollama on this Pi
    TTS_BACKEND: str = "stub"            # we'll swap to real TTS later

    # Ollama settings
    OLLAMA_HOST: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "llama3.2:1b"    # exactly as shown in `ollama list`

config = Config()
