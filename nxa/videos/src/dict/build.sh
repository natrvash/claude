#!/usr/bin/env bash
# Build dictionary-entry videos. Usage: [YESBUT=1] ./build.sh <NA_Post_01_sfx.mp4> [id ...]   (no id = all six)
set -euo pipefail; cd "$(dirname "$0")"
REF="$1"; shift
IDS=("$@"); [ ${#IDS[@]} -eq 0 ] && IDS=($(python3 -c "import json;print(' '.join(e['id'] for e in json.load(open('entries.json'))['entries']))"))
for ID in "${IDS[@]}"; do
  AVA="../../vo/$(python3 -c "import json;print({e['id']:e['ava'] for e in json.load(open('entries.json'))['entries']}['$ID'])")"
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$AVA")
  python3 tts.py "$ID"; python3 envelope.py "$ID"; python3 plan.py "$ID" "$DUR"
  node rec.js "$ID"
  python3 mix.py "$ID" "$REF" "$AVA"
  W=work/$ID
  ffmpeg -v error -y -i $W/mix.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 $W/mix_norm.wav
  T=$(python3 -c "import json;print(json.load(open('$W/plan.json'))['TOTAL'])")
  ffmpeg -v error -y -framerate 30 -i $W/frames/f%04d.png -i $W/mix_norm.wav -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -r 30 \
    -c:a aac -b:a 256k -t "$T" -movflags +faststart "../../NxA_${ID}${YESBUT:+_yesbut}$([ "${YESBUT:-}" = 2 ] && echo 2).mp4"
  echo "built NxA_${ID}${YESBUT:+_yesbut}$([ "${YESBUT:-}" = 2 ] && echo 2).mp4 (${T}s)"
done
