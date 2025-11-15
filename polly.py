#! /usr/bin/python3
import boto3
import sys
import subprocess
import os

def generate_tts_polly(text, filename):
    polly = boto3.client("polly", region_name="us-east-1")  # IAD

    response = polly.synthesize_speech(
        Text=text,
        Engine="generative",
        OutputFormat="mp3",
        VoiceId="Celine",  # Other French voices: Lea, Mathieu
        LanguageCode="fr-FR",
    )

    with open(filename, "wb") as f:
        f.write(response["AudioStream"].read())
        print(f"✅ Saved to {filename}")


def generate_tts_ssml_polly(text, filename):
    polly = boto3.client("polly", region_name="us-east-1")  # IAD

    # Use SSML with an f-string to inject text dynamically
    # Volume control doesn't seem to work.
    ssml_text = f"""
    <speak>
      <prosody volume="x-loud">{text}</prosody>
    </speak>
    """
    response = polly.synthesize_speech(
        Engine="generative",
        VoiceId="Celine",
        OutputFormat="mp3",
        TextType="ssml",
        LanguageCode="fr-FR",
        Text=ssml_text
    )

    with open(filename, "wb") as f:
        f.write(response["AudioStream"].read())
        print(f"✅ Saved to {filename}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: polly.py <text> <filename base>")
        sys.exit(1)
    text = sys.argv[1]
    fileNameBase = sys.argv[2]
    filename = f"{fileNameBase}.mp3"
    boost_db = 6.0
    generate_tts_ssml_polly(text, "/tmp/" + filename)
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
