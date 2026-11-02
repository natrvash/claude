"""Machine narration for the dictionary entry: each word spoken separately by espeak-ng and butted together,
so it sounds unmistakably like a computer. Writes narration.wav + timings.json (word start/end in seconds)."""
import subprocess, wave, json, os, numpy as np
D = os.path.dirname(os.path.abspath(__file__))
SR = 48000
VOICE, SPEED = "en-us+m3", 135

ENTRY = {
    "word": "Photography",
    "spoken_word": "Photography.",
    "pos": "noun",
    "definition": "The practice of taking pictures with a camera.",
}

def say(text, path):
    subprocess.run(["espeak-ng", "-v", VOICE, "-s", str(SPEED), "-w", path, text], check=True)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    # trim espeak's leading/trailing silence
    nz = np.where(np.abs(x) > 0.01)[0]
    return x[nz[0]:nz[-1] + 1] if len(nz) else x

def build(t0):
    parts, timings, t = [], {}, t0
    gap = lambda s: np.zeros(int(SR * s), np.float32)
    # 1 · the word, then "noun"
    w = say(ENTRY["spoken_word"], f"{D}/tts/word.wav"); timings["word"] = [t, t + len(w) / SR]; parts += [w]; t += len(w) / SR
    parts += [gap(.25)]; t += .25
    n = say(ENTRY["pos"], f"{D}/tts/pos.wav"); timings["pos"] = [t, t + len(n) / SR]; parts += [n]; t += len(n) / SR
    parts += [gap(.55)]; t += .55
    # 2 · the definition, word by word (tiny gaps = machine cadence)
    timings["def"] = []
    for i, tok in enumerate(ENTRY["definition"].split()):
        s = say(tok.strip(".,"), f"{D}/tts/d{i:02d}.wav")
        timings["def"].append([tok, t, t + len(s) / SR]); parts += [s, gap(.06)]; t += len(s) / SR + .06
    timings["end"] = t
    return np.concatenate([gap(t0)] + parts), timings

audio, timings = build(t0=0.45)
with wave.open(f"{D}/narration.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((audio / max(1e-9, np.abs(audio).max()) * .9 * 32767).astype(np.int16).tobytes())
json.dump(timings, open(f"{D}/timings.json", "w"), indent=1)
print(json.dumps({k: v for k, v in timings.items() if k != "def"}), "def words:", len(timings["def"]), "ends", round(timings["def"][-1][2], 2))
