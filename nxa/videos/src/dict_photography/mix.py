"""Mix: machine narration + Post 01 ticks + shutter on the strike + Ava's take (optional).
Usage: python3 mix.py <NA_Post_01.mp4> [ava_take.wav|.m4a]"""
import numpy as np, wave, json, os, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__))
SR = 48000
plan = json.load(open(f"{D}/plan.json"))
N = int(SR * plan["TOTAL"]); out = np.zeros((N, 2)); rng = np.random.default_rng(5)

def load(path, ch=2):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", str(ch), "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).reshape(-1, ch).astype(np.float32) / 32768

def place(sig, at, gain=1.0):
    if sig.ndim == 1: sig = np.stack([sig, sig], 1)
    i = int(at * SR); n = max(0, min(len(sig), N - i)); out[i:i+n] += sig[:n] * gain

def env(n, a=.0005, d=.02):
    x = np.arange(n) / SR; return np.minimum(x / a, 1) * np.exp(-x / d)
def bandnoise(n, k):
    x = rng.standard_normal(n + k); return (np.convolve(x, np.ones(k)/k, "same") - np.convolve(x, np.ones(k*4)/(k*4), "same"))[:n]
def shutter():
    s = np.zeros(int(SR * .22))
    def click(at, f, g, d=.004):
        n = int(SR * .03); x = np.arange(n) / SR; i = int(at * SR)
        s[i:i+n] += (np.sin(2*np.pi*f*x) * .4 + bandnoise(n, 3) * .9) * env(n, d=d) * g
    click(0, 3800, 1); n = int(SR*.07); s[int(.004*SR):int(.004*SR)+n] += bandnoise(n, 10) * env(n, a=.002, d=.018) * .55
    click(.062, 2900, .8); click(.071, 5200, .35, .002); return s

# machine voice, slightly band-limited so it reads as "speaker", centred
voice = load(f"{D}/narration.wav", 1)[:, 0]
place(voice, 0, .9)
# Post 01 tick when the strike starts, shutter when it lands, soft tick for the ×
ref = load(sys.argv[1])
tick = ref[int(1.08*SR):int(1.30*SR)].copy(); f = int(.004*SR); tick[:f] *= np.linspace(0,1,f)[:,None]; tick[-f:] *= np.linspace(1,0,f)[:,None]
place(tick, plan["STRIKE"][0], .9)
place(shutter(), plan["STRIKE"][1] - .05, .8)
place(tick, plan["AVA"][1] + .45, .6)
# music bed, ducked under the AI voice and under Ava's take
import music
tm = json.load(open(f"{D}/timings.json"))
bed = music.bed(plan["TOTAL"])
duck = music.duck_curve(plan["TOTAL"], [(tm["word"][0], tm["def"][1]), (plan["AVA"][0], plan["AVA"][1])], depth=.35)
place(bed * duck[:len(bed), None], 0, .30)
# Ava's take
if len(sys.argv) > 2:
    place(load(sys.argv[2]), plan["AVA"][0], 1.0)

out /= max(1e-9, np.abs(out).max()) * 1.12
with wave.open(f"{D}/mix.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
print("ok", "ava" if len(sys.argv) > 2 else "no ava take (placeholder silence)")
