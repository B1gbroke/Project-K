# src/nlp/tts.py
# tts.py
import subprocess
from pathlib import Path

# Path to your Piper voice model
PIPER_MODEL_PATH = (
    Path.home()
    / ".local"
    / "share"
    / "piper-tts"
    / "en"
    / "en_US"
    / "amy"
    / "medium"
    / "en_US-amy-medium.onnx"
)

# Temp WAV file
TMP_WAV = Path("/tmp/assistant_tts.wav")

# ALSA device that you just tested successfully
ALSA_DEVICE = "plughw:2,0"


def speak(text: str) -> None:
    """
    Convert text to speech using Piper and play it through the MAX98357A.
    Blocks until playback is finished.
    """
    text = (text or "").strip()
    if not text:
        return

    # 1) Generate WAV with Piper
    piper_proc = subprocess.Popen(
        [
            "piper",
            "-m",
            str(PIPER_MODEL_PATH),
            "--output_file",
            str(TMP_WAV),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    piper_proc.communicate(input=text.encode("utf-8"))

    if piper_proc.returncode != 0:
        print(f"[TTS] Piper exited with code {piper_proc.returncode}")
        return

    # 2) Play WAV with aplay on the I2S amp
    cmd = ["aplay", "-q", "-D", ALSA_DEVICE, str(TMP_WAV)]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[TTS] aplay error: {e}")

