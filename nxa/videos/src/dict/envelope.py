"""Per-frame levels of the AI voice in 7 bands (0..1) for the line meter. Usage: python3 envelope.py <id>"""
import numpy as np, wave, json, os, sys
D = os.path.dirname(os.path.abspath(__file__)); W = f"{D}/work/{sys.argv[1]}"; FPS = 30; BANDS = 7
w = wave.open(f"{W}/narration.wav"); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
hop = sr // FPS; win = 2048; edges = np.geomspace(120, 5000, BANDS + 1); f = np.fft.rfftfreq(win, 1 / sr); out = []
for i in range(0, len(x), hop):
    seg = x[i:i + win]; seg = np.pad(seg, (0, win - len(seg))) * np.hanning(win); mag = np.abs(np.fft.rfft(seg))
    out.append([float(np.sqrt(np.mean(mag[(f >= edges[b]) & (f < edges[b + 1])] ** 2))) for b in range(BANDS)])
a = np.clip(np.array(out) / (np.percentile(out, 98, axis=0) + 1e-9), 0, 1) ** .7
for t in range(1, len(a)): a[t] = np.maximum(a[t], a[t - 1] * .72)
json.dump(np.round(a, 3).tolist(), open(f"{W}/envelope.json", "w"))
