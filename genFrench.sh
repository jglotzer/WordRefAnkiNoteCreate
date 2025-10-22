#! /usr/bin/bash

if [[ $# -ne 2 ]]; then
  echo "Usage: genFrench.sh text <outfile>"
  exit 1
fi

FFMPEG="/usr/bin/ffmpeg"
MPV="/usr/bin/mpv"
MODEL="$HOME/.local/share/piper/voices/fr_FR-siwis-medium"
TEXT="$1"
OUTFILE_WAV="$(mktemp --suffix=.wav)"
OUTFILE_MP3="$2.mp3"
if ! python3 -m piper --model "$MODEL" --output-file "$OUTFILE_WAV" -- $TEXT
then
  echo "Piper generation for $TEXT failed, exiting."
  exit 1
fi
if ! $FFMPEG -i $OUTFILE_WAV -loglevel warning -y -vn -ar 44100 -ac 2 -b:a 192k $OUTFILE_MP3
then
  echo "MP3 generation with ffmpeg failed for $TEXT, exiting."
  rm -f $OUTFILE_WAV
  exit 1
fi
rm -f $OUTFILE_WAV
$MPV $OUTFILE_MP3
