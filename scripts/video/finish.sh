#!/usr/bin/env bash
# Join the silent render and the mix into the final MP4, with loudness normalised for YouTube.
# Usage: bash finish.sh [out/video.mp4] [out/mix.wav] [final.mp4] [target_lufs=-14]
# Two-pass loudnorm: integrated -14 LUFS, true peak -1.5 dBTP. Prints duration and measured loudness.
set -euo pipefail
V="${1:-out/video.mp4}"; A="${2:-out/mix.wav}"; O="${3:-final.mp4}"; I="${4:--14}"
m=$(ffmpeg -hide_banner -nostats -i "$A" -af "loudnorm=I=$I:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1 | sed -n '/{/,/}/p')
get() { echo "$m" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
ffmpeg -y -loglevel error -i "$V" -i "$A" -map 0:v -map 1:a -c:v copy \
  -af "loudnorm=I=$I:TP=-1.5:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true,aresample=48000" \
  -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart "$O"
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$O")
lufs=$(ffmpeg -hide_banner -nostats -i "$O" -af ebur128=peak=true -f null - 2>&1 | awk '/Integrated loudness/{f=1} f&&/I:/{print $2; exit}')
peak=$(ffmpeg -hide_banner -nostats -i "$O" -af ebur128=peak=true -f null - 2>&1 | awk '/True peak/{f=1} f&&/Peak:/{print $2; exit}')
printf '%s: %.2f s (%d:%05.2f), %s LUFS, true peak %s dBFS\n' "$O" "$d" "$(python3 -c "print(int($d//60))")" "$(python3 -c "print($d%60)")" "$lufs" "$peak"
