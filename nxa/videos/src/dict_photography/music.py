"""Minimal warm bed for the dictionary series: soft pad, a gentle arpeggio and a round low note.
Fmaj7 · Am7 · Dm9 · Bbmaj7, 84 BPM, one chord per bar. Pure numpy, no samples."""
import numpy as np
SR = 48000
BPM = 84; BEAT = 60 / BPM; BAR = 4 * BEAT
CHORDS = [  # (bass, chord tones) in MIDI
    (41, [53, 57, 60, 64]),      # Fmaj7
    (45, [57, 60, 64, 67]),      # Am7
    (38, [53, 57, 60, 64, 69]),  # Dm9 (F A C E + A)
    (46, [53, 58, 62, 65]),      # Bbmaj7
]
hz = lambda m: 440 * 2 ** ((m - 69) / 12)

def _env(n, a, r):
    e = np.ones(n); ai = int(a * SR); ri = int(r * SR)
    if ai: e[:ai] = np.linspace(0, 1, ai)
    if ri: e[-ri:] *= np.linspace(1, 0, ri)
    return e

def pad(freqs, dur):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for f in freqs:
        for det in (-0.12, 0.0, 0.11):                 # gentle chorus
            ff = f * 2 ** (det / 12)
            s += np.sin(2*np.pi*ff*t) + .18*np.sin(2*np.pi*2*ff*t)
    return s / (len(freqs) * 3) * _env(n, .9, .9)

def pluck(f, dur=1.6):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2*np.pi*f*t) + .35*np.sin(2*np.pi*2*f*t)*np.exp(-t/.25) + .12*np.sin(2*np.pi*3*f*t)*np.exp(-t/.12)
    return s * np.minimum(t/.004, 1) * np.exp(-t/.55)

def bass(f, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2*np.pi*f*t) + .2*np.sin(2*np.pi*2*f*t)) * _env(n, .05, .4) * np.exp(-t/2.2)

def bed(total):
    N = int(total * SR) + SR * 2; out = np.zeros((N, 2))
    def put(sig, at, g, pan=0):
        i = int(at * SR); n = min(len(sig), N - i)
        out[i:i+n, 0] += sig[:n] * g * np.sqrt((1-pan)/2) * 1.41
        out[i:i+n, 1] += sig[:n] * g * np.sqrt((1+pan)/2) * 1.41
    bars = int(np.ceil(total / BAR))
    pattern = [0, 2, 1, 3, 2, 1]                        # arpeggio order over the bar, on eighths 0,1.5,2,3,4.5,6
    steps = [0, 1.5, 2, 3, 4.5, 6]
    for b in range(bars):
        lo, tones = CHORDS[b % 4]; t0 = b * BAR
        put(pad([hz(m) for m in tones], BAR + .9), t0, .55)
        put(bass(hz(lo), BAR), t0, .45)
        for k, st in zip(pattern, steps):
            m = tones[k % len(tones)] + 12
            put(pluck(hz(m)), t0 + st * BEAT / 2, .22, pan=(-.35 if st % 2 else .35))
    out = out[:int(total * SR)]
    fade = int(SR * 1.2); out[:int(SR*.8)] *= np.linspace(0, 1, int(SR*.8))[:, None]; out[-fade:] *= np.linspace(1, 0, fade)[:, None]
    return out / np.abs(out).max()

def duck_curve(total, spans, depth=.32, ramp=.25):
    """1.0 normally, `depth` under each (start, end) span, with smooth ramps."""
    t = np.arange(int(total * SR)) / SR; g = np.ones_like(t)
    for a, z in spans:
        down = np.clip((t - (a - ramp)) / ramp, 0, 1); up = np.clip(((z + ramp) - t) / ramp, 0, 1)
        g = np.minimum(g, 1 - (1 - depth) * np.minimum(down, up))
    return g
