"""Per-frame levels of the AI voice in 7 frequency bands (0..1), for the 'AI is speaking' line meter."""
import numpy as np, wave, json, os
D = os.path.dirname(os.path.abspath(__file__)); FPS = 30; BANDS = 7
w = wave.open(f"{D}/narration.wav"); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
hop = sr // FPS; win = 2048; edges = np.geomspace(120, 5000, BANDS + 1)
f = np.fft.rfftfreq(win, 1 / sr); out = []
for i in range(0, len(x), hop):
    seg = x[i:i + win]; seg = np.pad(seg, (0, win - len(seg))) * np.hanning(win)
    mag = np.abs(np.fft.rfft(seg))
    out.append([float(np.sqrt(np.mean(mag[(f >= edges[b]) & (f < edges[b + 1])] ** 2))) for b in range(BANDS)])
a = np.array(out); a = a / (np.percentile(a, 98, axis=0) + 1e-9); a = np.clip(a, 0, 1) ** .7
# smooth: fast attack, slower release
for t in range(1, len(a)): a[t] = np.maximum(a[t], a[t - 1] * .72)
json.dump(np.round(a, 3).tolist(), open(f"{D}/envelope.json", "w")); print("frames", len(a))
