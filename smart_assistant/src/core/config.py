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
    LLM_BACKEND: str = "ollama"          # Ollama on this Pi for llama3.2 1b
    TTS_BACKEND: str = "stub"            # swapped for TTS 

    # Ollama settings
    OLLAMA_HOST: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "llama3.2:1b"    # exact ollama model for running llama

config = Config()
