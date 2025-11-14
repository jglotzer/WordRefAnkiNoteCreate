#! /usr/bin/python3
# https://docs.cloud.google.com/text-to-speech/docs/list-voices-and-types for voices

from google.cloud import texttospeech
import sys
import subprocess
import os

def generate_tts_google(text, filename):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="fr-FR",
        name="fr-FR-Wavenet-E",  # Try others: Wavenet-A…E
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.0,       # default
        pitch=0.0,               # default
        volume_gain_db=0.0       # doesn't seem to do anything
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open("/tmp/" + filename, "wb") as out:
        out.write(response.audio_content)
        print(f"✅ Saved to /tmp/{filename}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: google_tts.py <text> <filename base>")
        sys.exit(1)
    text = sys.argv[1]
    fileName = sys.argv[2]
    filename = f"{fileName}.mp3"
    boost_db = 8.0
    generate_tts_google(text, filename)
    subprocess.run(["/usr/bin/ffmpeg", "-y", "-loglevel", "error", "-i", "/tmp/" + filename,
                    "-filter:a", f"volume=+{boost_db}dB", filename], check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL
                   )
    print(f"✅ Saved to {filename}")
    os.remove("/tmp/" + filename)
    subprocess.run(["/usr/bin/mpv", filename], check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL
                   )

