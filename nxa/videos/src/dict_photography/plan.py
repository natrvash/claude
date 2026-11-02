"""Timeline plan: where the strike, Ava's line and the end fall — and the end snapped to the music's next downbeat,
so the music can stop dead on the beat. Usage: python3 plan.py <ava_seconds> [music.mp3]"""
import json, sys, os
D = os.path.dirname(os.path.abspath(__file__))
tm = json.load(open(f"{D}/timings.json")); ava = float(sys.argv[1])
d_end = tm["def"][1]
STRIKE = [d_end + .35, d_end + .9]
AVA = [STRIKE[1] + .45, STRIKE[1] + .45 + ava]
content_end = AVA[1] + 1.3                     # the × lands at AVA end + .8, give it a beat to sit
total, cut = content_end, None
if len(sys.argv) > 2:
    import librosa, numpy as np
    y, sr = librosa.load(sys.argv[2], sr=22050, mono=True, duration=content_end + 12)
    _, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
    bars = beats[::4]                          # every 4th beat from the first one = bar lines
    nxt = [b for b in bars if b >= content_end]
    cut = float(nxt[0]) if nxt else content_end
    total = cut
plan = {"STRIKE": STRIKE, "AVA": AVA, "TOTAL": round(total, 3), "MUSIC_CUT": cut}
json.dump(plan, open(f"{D}/plan.json", "w")); print(plan)
