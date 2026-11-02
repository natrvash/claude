#!/usr/bin/env bash
# Build the Photography dictionary entry. Usage: ./build.sh <NA_Post_01_sfx.mp4> [ava_take] [ava_seconds]
set -euo pipefail; cd "$(dirname "$0")"
REF="$1"; AVA="${2:-}"; DUR="${3:-4.2}"
if [ -n "$AVA" ]; then DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$AVA"); fi
python3 tts.py
node rec.js "$DUR"
python3 mix.py "$REF" $AVA
ffmpeg -v error -y -i mix.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 mix_norm.wav
T=$(python3 -c "import json;print(json.load(open('plan.json'))['TOTAL'])")
ffmpeg -v error -y -framerate 30 -i frames/f%04d.png -i mix_norm.wav -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 256k -t "$T" -movflags +faststart ../../NxA_dict_01_Photography_draft.mp4
echo built
