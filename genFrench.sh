#! /usr/bin/bash

if [[ $# -ne 2 ]]; then
  echo "Usage: genFrench.sh text <outfile>"
  exit 1
fi

TEXT="$1"
FFMPEG="/usr/bin/ffmpeg"
MPV="/usr/bin/mpv"
MODEL="$HOME/.local/share/piper/voices/fr_FR-siwis-medium"
OUTFILE_WAV="$(mktemp --suffix=.wav)"
OUTFILE_MP3="$2.mp3"
PGREP="/usr/bin/pgrep"
CURL="/usr/bin/curl"
JQ="/usr/bin/jq"
PIPER_SERVER="piper.http_server"

if ! "${PGREP}" -f "${PIPER_SERVER}" > /dev/null
then
   echo "Piper HTTP server not running, starting in background."
   python3 -m "${PIPER_SERVER}" --model "${MODEL}" &
   sleep 3
fi

# https://stackoverflow.com/questions/48470049/build-a-json-string-with-bash-variables
JSON_STRING=$($JQ -n --arg text "$TEXT" '{text: $text}')
echo $JSON_STRING > /tmp/json_string
if ! $CURL -s -X POST -H 'Content-Type: application/json' -d "$JSON_STRING" -o "${OUTFILE_WAV}" localhost:5000
then
  echo "Curl to Piper Webserver call failed."
  exit 1
fi

if ! $FFMPEG -i $OUTFILE_WAV -loglevel quiet -y -vn -ar 44100 -ac 2 -b:a 192k $OUTFILE_MP3
then
  echo "MP3 generation with ffmpeg failed for $TEXT, exiting."
  rm -f $OUTFILE_WAV
  exit 1
fi
rm -f $OUTFILE_WAV
$MPV $OUTFILE_MP3
