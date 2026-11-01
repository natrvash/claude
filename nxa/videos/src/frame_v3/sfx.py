"""Sound for NxA 01 — FRAME v3: NA Post 01's own sound under the footage, its ticks reused for the intro/outro,
and a camera shutter when the frame is taken. Usage: python3 sfx.py <NA_Post_01.mp4>"""
import numpy as np, wave, os, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__))
SR, TOTAL = 48000, 8.2
REF0, REF_LEN = 1.05, 4.0
N = int(SR * TOTAL)
out = np.zeros((N, 2))
rng = np.random.default_rng(3)

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-f", "s16le", "-ac", "2", "-ar", str(SR), "-"],
                     capture_output=True, check=True).stdout
ref = np.frombuffer(raw, np.int16).reshape(-1, 2) / 32768.0

def place(sig, at, gain=1.0):
    if sig.ndim == 1: sig = np.stack([sig, sig], 1)
    i = int(at * SR); n = min(len(sig), N - i)
    out[i:i+n] += sig[:n] * gain

def cut(a, b, fade=0.004):
    s = ref[int(a*SR):int(b*SR)].copy(); f = int(fade*SR)
    s[:f] *= np.linspace(0, 1, f)[:, None]; s[-f:] *= np.linspace(1, 0, f)[:, None]
    return s

def env(n, a=0.0005, d=0.02):
    x = np.arange(n) / SR
    return np.minimum(x / a, 1) * np.exp(-x / d)

def bandnoise(n, k):
    x = rng.standard_normal(n + k)
    return (np.convolve(x, np.ones(k) / k, "same") - np.convolve(x, np.ones(k*4) / (k*4), "same"))[:n]

def shutter(scale=1.0):
    """Mechanical SLR-style shutter: first curtain click, mirror slap body, second curtain click."""
    L = int(SR * 0.22); s = np.zeros(L)
    def click(at, f, g, d=0.004):
        n = int(SR * 0.03); x = np.arange(n) / SR
        c = (np.sin(2*np.pi*f*x) * .4 + bandnoise(n, 3) * .9) * env(n, d=d) * g
        i = int(at * SR); s[i:i+n] += c
    click(0.000, 3800, 1.0)
    n = int(SR * 0.07); s[int(.004*SR):int(.004*SR)+n] += bandnoise(n, 10) * env(n, a=.002, d=.018) * .55   # mirror slap
    click(0.062, 2900, .8)
    click(0.071, 5200, .35, .002)
    return s * scale

# NA Post 01 sound under its footage
seg = cut(0.0, REF_LEN)
fo = int(0.3 * SR); seg[-fo:] *= np.linspace(1, 0, fo)[:, None]
place(seg, REF0)
# its ticks, reused around it
tickA = cut(1.08, 1.30); tickB = cut(2.50, 2.72)
place(tickA, 0.30, .8)          # × turns into +
place(tickB, 0.98, .9)          # first rectangle closes
place(shutter(), 5.58, .9)      # 4th Rose edge: the frame is taken
place(tickA, 7.55, .8)          # edges retract (reverse of 0.98)
place(tickB, 7.85, .6)          # arms back to +
place(shutter(.55), 8.04, .7)   # + becomes ×

out /= max(1e-9, np.max(np.abs(out))) * 1.12
with wave.open(f"{D}/sfx.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("ok")
