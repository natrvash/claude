"""AI narration for one entry (piper neural TTS). Usage: python3 tts.py <id>
Writes work/<id>/narration.wav and timings.json: word/pos/def = [start, end] of the phrase that reveals that block, end = last word."""
import subprocess, wave, json, os, sys, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); SR = 48000
MODEL = os.environ.get("PIPER_MODEL", "/tmp/piper/en_US-ryan-medium.onnx")
E = {e["id"]: e for e in json.load(open(f"{D}/entries.json"))["entries"]}[sys.argv[1]]
W = f"{D}/work/{E['id']}"; os.makedirs(f"{W}/tts", exist_ok=True)

def say(text, path):
    subprocess.run(["python3", "-m", "piper", "-m", MODEL, "-f", path, "--length-scale", "1.05"], input=text.encode(), check=True, capture_output=True)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    nz = np.where(np.abs(x) > 0.01)[0]
    return x[max(0, nz[0] - 200):nz[-1] + 1200]

t, parts, tm = 0.5, [np.zeros(int(SR * .5), np.float32)], {"phrases": {}}
for key, text, gap, show in E["ai"]:
    s = say(text, f"{W}/tts/{key}.wav"); span = [t, t + len(s) / SR]
    tm["phrases"][key] = span
    if show: tm[show] = span
    parts += [s, np.zeros(int(SR * gap), np.float32)]; t += len(s) / SR + gap
tm["end"] = max(v[1] for v in tm["phrases"].values())
audio = np.concatenate(parts)
with wave.open(f"{W}/narration.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((audio / max(1e-9, np.abs(audio).max()) * .9 * 32767).astype(np.int16).tobytes())
json.dump(tm, open(f"{W}/timings.json", "w"), indent=1)
print(E["id"], {k: [round(a, 2) for a in v] for k, v in tm.items() if k in ("word", "pos", "def")}, "ai ends", round(tm["end"], 2))
