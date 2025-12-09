# src/core/pipeline.py
from typing import List, Dict
from pathlib import Path

from src.audio.input import record_to_file
from src.audio.output import play_audio_file
from src.nlp.stt import transcribe_audio_file
from src.nlp.llm import generate_reply
#from src.nlp.tts import synthesize_speech
from src.nlp.tts import speak

Conversation = List[Dict[str, str]]

class AssistantPipeline:
    def __init__(self):
        self.history: Conversation = []

    def capture_user_audio(self, path: str):
        record_to_file(path)

    def understand_user(self, audio_path: str) -> str:
        text = transcribe_audio_file(audio_path)
        self.history.append({"role": "user", "content": text})
        return text

    def think_and_reply(self, user_text: str) -> str:
        reply = generate_reply(user_text, self.history)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def speak_reply(self, reply_text: str, audio_path: str):
        output_file = synthesize_speech(reply_text, audio_path)
        if Path(output_file).exists() and Path(output_file).stat().st_size > 0:
            play_audio_file(output_file)
        else:
            print("[WARN] No audio generated (stub TTS).")

    def run_one_turn(self):
        raw_audio = "data/user_input.wav"
        reply_audio = "data/assistant_reply.wav"

        self.capture_user_audio(raw_audio)
        user_text = self.understand_user(raw_audio)
        print(f"\n[STT OUTPUT] {user_text}\n")

        reply = self.think_and_reply(user_text)
        print(f"[ASSISTANT] {reply}\n")
        speak(reply)

       # self.speak_reply(reply, reply_audio) #uncomment if its not working(old tts)
