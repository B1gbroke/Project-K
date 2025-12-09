# src/nlp/stt.py
from src.core.config import config

# Lazy-load the model so startup is faster
_whisper_model = None

def _get_model():
    global _whisper_model
    if _whisper_model is None:
        import whisper
        # "tiny" is fastest on a Pi; you can try "base" later
        print("[STT] Loading Whisper model 'tiny'...")
        _whisper_model = whisper.load_model("tiny")
    return _whisper_model

def transcribe_audio_file(path: str) -> str:
    """
    Turn an audio file into text using local Whisper.
    No API key required; runs on the Pi.
    """
    if config.STT_BACKEND != "whisper_local":
        print(f"[STT] Unknown backend {config.STT_BACKEND}, returning stub text.")
        return "STT backend not configured."

    model = _get_model()
    print(f"[STT] Transcribing {path} ...")
    result = model.transcribe(path)
    text = result.get("text", "").strip()
    print(f"[STT] Text: {text!r}")
    return text or "(no speech detected)"
