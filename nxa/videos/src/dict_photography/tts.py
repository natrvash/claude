"""AI narration (piper, neural TTS — smooth but clearly synthetic). Three phrases: word, part of speech, definition.
Writes narration.wav + timings.json. Voice model path: $PIPER_MODEL (default /tmp/piper/en_US-ryan-medium.onnx)."""
import subprocess, wave, json, os, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); SR = 48000
MODEL = os.environ.get("PIPER_MODEL", "/tmp/piper/en_US-ryan-medium.onnx")
# The assistant talks a little: introduces itself, looks the word up, reads the entry. Text on screen stays the same.
PHRASES = [
    ("intro", "Hi, I'm your AI assistant."),
    ("lookup", "I looked up"),
    ("word", "photography"),
    ("dict", "in the dictionary."),
    ("pos", "It's a noun,"),
    ("means", "and it means:"),
    ("def", "the practice of taking pictures with a camera."),
]
GAPS = {"intro": .35, "lookup": .05, "word": .05, "dict": .35, "pos": .08, "means": .18, "def": 0}

def say(text, path):
    subprocess.run(["python3", "-m", "piper", "-m", MODEL, "-f", path, "--length-scale", "1.08"],
                   input=text.encode(), check=True, capture_output=True)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    nz = np.where(np.abs(x) > 0.01)[0]
    return x[max(0, nz[0]-200):nz[-1] + 1200]

os.makedirs(f"{D}/tts", exist_ok=True)
t, parts, tm = 0.5, [np.zeros(int(SR * .5), np.float32)], {}
for key, text in PHRASES:
    s = say(text, f"{D}/tts/{key}.wav"); tm[key] = [t, t + len(s) / SR]; parts.append(s); t += len(s) / SR
    parts.append(np.zeros(int(SR * GAPS[key]), np.float32)); t += GAPS[key]
audio = np.concatenate(parts)
with wave.open(f"{D}/narration.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((audio / max(1e-9, np.abs(audio).max()) * .9 * 32767).astype(np.int16).tobytes())
json.dump(tm, open(f"{D}/timings.json", "w"), indent=1); print(tm)
