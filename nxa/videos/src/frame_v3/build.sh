#!/usr/bin/env bash
# Build NxA 01 — FRAME v3. Usage: ./build.sh <NA_Post_01_sfx.mp4> [out.mp4]
set -euo pipefail
cd "$(dirname "$0")"
REF="$1"; OUT="${2:-../../NxA_01_FRAME_v3.mp4}"
node rec.js
python3 sfx.py "$REF"
ffmpeg -v error -y -i sfx.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 sfx_norm.wav
# Post 01 (white on #0F0F0F) -> Ink lines with alpha, placed in the feed-safe square, 1.05s–5.05s, fading out at the end
ffmpeg -v error -y -framerate 30 -i frames/f%04d.png -i "$REF" -i sfx_norm.wav -filter_complex "
 [1:v]trim=0:4,setpts=PTS-STARTPTS,fps=30,format=gray,lut=y='clip((val-15)*255/240,0,255)',
      fade=t=out:st=3.7:d=0.3,fade=t=in:st=0:d=0.05,setpts=PTS+1.05/TB[mask];
 color=c=0x111111:s=1080x1080:r=30:d=8.2,format=gray[ink];
 [ink][mask]alphamerge,format=yuva420p[lines];
 [0:v][lines]overlay=x=0:y=420:eof_action=pass:enable='between(t,1.05,5.05)',format=yuv420p[v]" \
 -map "[v]" -map 2:a -c:v libx264 -preset slow -crf 16 -profile:v high -r 30 -c:a aac -b:a 256k -t 8.2 -movflags +faststart "$OUT"
echo "built $OUT"
