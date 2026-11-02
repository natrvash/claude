#!/usr/bin/env bash
# Build the Photography dictionary entry.
# Usage: MUSIC=<track.mp3> ./build.sh <NA_Post_01_sfx.mp4> [ava_take]
set -euo pipefail; cd "$(dirname "$0")"
REF="$1"; AVA="${2:-}"; DUR=4.2
if [ -n "$AVA" ]; then DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$AVA"); fi
python3 tts.py
python3 plan.py "$DUR" ${MUSIC:-}
node rec.js "$DUR"
python3 mix.py "$REF" $AVA
# loudness without a limiter tail: the music must stop dead, so only a static gain is applied
G=$(ffmpeg -v info -i mix.wav -af ebur128 -f null - 2>&1 | grep -A6 Summary | awk '/I:/{print -16-$2}')
ffmpeg -v error -y -i mix.wav -af "volume=${G}dB,alimiter=limit=0.89:attack=1:release=20:level=false" -ar 48000 mix_norm.wav
T=$(python3 -c "import json;print(json.load(open('plan.json'))['TOTAL'])")
ffmpeg -v error -y -framerate 30 -i frames/f%04d.png -i mix_norm.wav -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 256k -t "$T" -movflags +faststart "${OUT:-../../NxA_dict_01_Photography_draft.mp4}"
echo built
