"""Minimal sound for NxA 01 — FRAME (v2). Loop-exact: every pad frequency completes whole cycles in TOTAL seconds."""
import numpy as np, wave, json, os
D = os.path.dirname(os.path.abspath(__file__))
SR, TOTAL = 48000, 6.0
N = int(SR * TOTAL)
t = np.arange(N) / SR
out = np.zeros((N, 2))
rng = np.random.default_rng(11)
SPAWN = json.load(open(f"{D}/spawn.json"))

def place(sig, at, pan=0.0, gain=1.0):
    i = int(at * SR) % N
    n = len(sig)
    idx = (np.arange(n) + i) % N                     # wrap around: sounds near the end spill into the start (loop-safe)
    l, r = np.sqrt((1 - pan) / 2), np.sqrt((1 + pan) / 2)
    np.add.at(out[:, 0], idx, sig * gain * l * 1.41)
    np.add.at(out[:, 1], idx, sig * gain * r * 1.41)

def env(n, a=0.0006, d=0.03):
    x = np.arange(n) / SR
    return np.minimum(x / a, 1) * np.exp(-x / d)

def tick(f=2600, d=0.010, noise=.3, length=0.08):
    n = int(SR * length); x = np.arange(n) / SR
    return (np.sin(2*np.pi*f*x) * (1-noise) + rng.standard_normal(n) * noise) * env(n, d=d)

def pluck(f, d=0.5, length=1.4):
    n = int(SR * length); x = np.arange(n) / SR
    s = np.sin(2*np.pi*f*x) + .3*np.sin(2*np.pi*2*f*x)*np.exp(-x/0.15) + .08*np.sin(2*np.pi*3*f*x)*np.exp(-x/0.08)
    return s * env(n, a=0.003, d=d)

def air(length, rise=False):
    n = int(SR * length); x = np.linspace(0, 1, n)
    noise = rng.standard_normal(n)
    k = np.ones(64) / 64; noise = np.convolve(noise, k, "same")      # soft low-passed air
    shape = (x if rise else 1 - x) ** 2 * np.sin(np.pi * x) ** .5
    return noise * shape

# --- pad: A2 · E3 · B3 · E4 (sus, airy). f*TOTAL is an integer for each → seamless loop
pad = np.zeros(N)
for f, g in ((110, 1.0), (165, .7), (247.5, .45), (330, .25)):
    assert abs(f * TOTAL - round(f * TOTAL)) < 1e-9
    pad += g * np.sin(2*np.pi*f*t)
lfo = 0.75 + 0.25 * np.cos(2*np.pi*t/TOTAL)                      # breathes once per loop
pad *= lfo * 0.035
out[:, 0] += pad; out[:, 1] += pad * 0.96

# --- events (seconds), synced to anim.html
place(tick(3200, .006, .2), 0.30, .3, .35)                    # × turns into +
place(tick(2400, .010), 0.90, .2, .45)                       # arms reach
place(tick(2000, .014, .25), 1.05, 0, .6)                    # first rectangle closes
for i, s in enumerate(SPAWN[:-1]):                           # each rectangle slides out of the last
    g = .32 * (1 - i / len(SPAWN)) + .08
    place(tick(2200 + 900 * rng.random(), .005, .45), s + 0.24, rng.uniform(-.6, .6), g)
place(air(0.55), 2.55, 0, .10)                               # the crowd fades away
for i, f in enumerate((659.25, 739.99, 830.61, 987.77)):      # four Rose edges: E5 F#5 G#5 B5
    place(pluck(f, .25, .6), 3.12 + i * 0.12, (i - 1.5) * .25, .16)
place(pluck(440, .7), 3.50, 0, .12)                          # the title rises
place(air(0.45, rise=True), 4.95, 0, .07)                    # fold
place(tick(2600, .008, .2), 5.47, .2, .35)                   # frame becomes +
place(pluck(880, .45, 1.0), 5.80, .3, .12)                   # × lands (rings into the loop start)

out /= np.max(np.abs(out)) * 1.12
with wave.open(f"{D}/sfx.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("ok")
