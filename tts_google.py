#! /usr/bin/python3
# https://docs.cloud.google.com/text-to-speech/docs/list-voices-and-types for voices

from google.cloud import texttospeech
import sys

def generate_tts_google(text, filename="output.mp3"):
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
        volume_gain_db=2.0        # increase volume slightly
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f"✅ Saved to {filename}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: tts.google.py <text> <filename>")
    generate_tts_google(sys.argv[1], sys.argv[2])
