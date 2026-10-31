"""Synthesise the FRAME sound design: dry ticks on every snap (like NA Post 01), a shutter at the frame snap,
a soft tone when the × lands. Loop-safe: silence at both ends."""
import numpy as np, wave, os
SR, DUR = 48000, 5.5
D = os.path.dirname(os.path.abspath(__file__))
out = np.zeros((int(SR * DUR), 2))
rng = np.random.default_rng(35)

def place(sig, t, pan=0.0, gain=1.0):
    i = int(t * SR); n = min(len(sig), len(out) - i)
    l, r = np.sqrt((1 - pan) / 2), np.sqrt((1 + pan) / 2)
    out[i:i+n, 0] += sig[:n] * gain * l * 1.4
    out[i:i+n, 1] += sig[:n] * gain * r * 1.4

def env(n, a=0.0005, d=0.03):
    t = np.arange(n) / SR
    return np.minimum(t / a, 1) * np.exp(-t / d)

def tick(freq=2600, d=0.012, noise=.35):
    n = int(SR * 0.08); t = np.arange(n) / SR
    s = np.sin(2*np.pi*freq*t) * (1-noise) + rng.standard_normal(n) * noise
    return s * env(n, d=d)

def thump(freq=90, d=0.05):
    n = int(SR * 0.25); t = np.arange(n) / SR
    f = freq * (1 + 1.5*np.exp(-t/0.01))
    return np.sin(2*np.pi*np.cumsum(f)/SR) * env(n, a=0.001, d=d)

def shutter():
    # two mechanical clicks 45 ms apart, with a short noise body
    s = np.zeros(int(SR*0.25))
    for k, (dt, f) in enumerate(((0, 3200), (0.045, 2100))):
        c = tick(f, d=0.008, noise=.6) * (1 if k == 0 else .8)
        i = int(dt*SR); s[i:i+len(c)] += c
    n = int(SR*0.09); body = rng.standard_normal(n) * env(n, a=0.002, d=0.02) * .25
    s[:n] += body
    return s

def tone(freq=880, d=0.35):
    n = int(SR * 1.2); t = np.arange(n) / SR
    s = (np.sin(2*np.pi*freq*t) + .35*np.sin(2*np.pi*freq*2*t) + .15*np.sin(2*np.pi*freq*3.01*t))
    return s * env(n, a=0.004, d=d)

# --- events (seconds) synced to anim.html
place(tick(3400, .006, .2), 0.35, .4, .45)            # × folds to a point
for k, p in enumerate((-.3, .1, .4)):                 # point splits into three
    place(tick(2900 + k*250, .007), 0.65 + k*0.025, p, .55)
place(tick(2200, .014), 1.05, 0, .8); place(thump(110), 1.05, 0, .35)   # rooms land
place(tick(2500, .012), 1.65, -.2, .75)               # swap
place(tick(2350, .012), 2.25, .2, .75)                # swap
for k in range(4):                                    # restless search
    place(tick(3000 + 300*(k % 2), .005, .5), 2.30 + k*0.06, (-1)**k * .3, .35)
place(shutter(), 2.80, 0, 1.0); place(thump(70, .08), 2.80, 0, .6)       # the frame forms
place(tone(880, .45), 3.65, .25, .30)                  # × lands next to the title
place(tick(2000, .02, .1), 5.00, 0, .25)               # fade-out breath

# fade the very end so the loop seam is silent
fade = int(SR * 0.15); out[-fade:] *= np.linspace(1, 0, fade)[:, None]
out /= np.max(np.abs(out)) * 1.05
pcm = (out * 32767).astype(np.int16)
with wave.open(f"{D}/sfx.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok")
