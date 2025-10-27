#!/usr/bin/env python3
import subprocess
import json
import os
import re
import urllib.request
import sys

# ------------------------
# Configuration
# ------------------------
ANKI_CONNECT_URL = "http://127.0.0.1:8765"
MODEL_PATH = os.path.expanduser("~/.local/share/piper/voices/fr_FR-siwis-medium")
GEN_SCRIPT = os.path.expanduser("~/bin/genFrench.sh")
NOTE_ID = 1761501756693

# ------------------------
# AnkiConnect helpers
# ------------------------
def anki_request(action, **params):
    request_json = json.dumps({"action": action, "version": 6, "params": params}).encode("utf-8")
    with urllib.request.urlopen(urllib.request.Request(ANKI_CONNECT_URL, request_json)) as response:
        data = json.load(response)
        if data.get("error"):
            raise Exception(f"AnkiConnect error: {data['error']}")
        return data["result"]
# --- Precompiled regex patterns ---
BOLD_RE = re.compile(r"<b>([^<\n]*)", re.IGNORECASE)          # bold text at start of front of card
RE_REFLEXIVE = re.compile(r"^\((s['e])\)\s*", re.IGNORECASE)  # capture (se) or (s')
RE_BRACKETS  = re.compile(r"[\(\[\{<].*$")                    # strip after (, [, {, or <
RE_HTML      = re.compile(r"&.*$")                            # strip trailing &nbsp etc.
RE_SPACES    = re.compile(r"\s{2,}")                          # normalize multiple spaces


def clean_entry(entry: str) -> str:
    """
    Clean a dictionary/Anki entry for Piper audio generation:
    - replaces "un(e) with un"
    - replaces &nbsp; with a simple space
    - replaces "/" with "ou"
    - does away with qqn and qch for robustness and accurate voice generation
    - Removes leading reflexive prefixes for general cleaning
    - Strips trailing bracketed or HTML content
    - Normalizes spaces
    - If leading reflexive prefix exists, generates 'headword - reflexive form'
      specifically for audio, preserving a natural pause.
    """
    entry = entry.strip()
    entry = entry.replace("un(e) ", "un ")
    entry = entry.replace("&nbsp;", " ")
    entry = entry.replace("[qqn]", "quelque'un")
    entry = entry.replace("[qch]", "quelque chose")
    entry = entry.replace("qqn", "quelque'un")
    entry = entry.replace("qch", "quelque chose")
    entry = entry.replace("/", " ou ")

    # Check for leading reflexive
    reflexive_match = RE_REFLEXIVE.match(entry)
    reflexive_prefix = reflexive_match.group(1) if reflexive_match else None

    # Remove leading reflexive and trailing clutter
    entry = RE_REFLEXIVE.sub("", entry)
    entry = RE_BRACKETS.sub("", entry)
    entry = RE_HTML.sub("", entry)
    entry = RE_SPACES.sub(" ", entry).strip()

    # If reflexive prefix exists, append "headword - reflexive form"
    if reflexive_prefix:
        # Concatenate properly for (s') vs (se)
        reflexive_word = reflexive_prefix.lower() + entry if reflexive_prefix == "s'" else f"{reflexive_prefix.lower()} {entry}"
        entry = f"{entry} - {reflexive_word}"

    return entry

# ------------------------
# Step 0: Find Notes
# ------------------------
note_list = anki_request("findNotes", query="deck:French")

# The syntax for list slicing is my_list[start:stop:step].
# The start index is inclusive and the stop index is exclusive (up to, but not including).
# Here's a poor man's multi use paradigm - pick one of the following two lines
# for note_id in note_list[2400:2500]:
for note_id in [NOTE_ID]:

    # ------------------------
    # Step 1: Get note content
    # ------------------------
    note_info = anki_request("notesInfo", notes=[note_id])[0]
    front_html = note_info["fields"]["Front"]["value"]
    #word_match = re.search(r"<b>(.*?)</b>", front_html)
    word_match = BOLD_RE.search(front_html)
    if not word_match:
        print("❌ No <b>word</b> found in note Front field for .", front_html)
        sys.exit(1)
        #continue
    mp3_match = re.search(r"\[sound:.*\.mp3\]", front_html)
    if mp3_match:
        print("🔁 Sound tag already present — skipping update.")
        continue
    word = word_match.group(1).strip()
    # Do some cleanup.
    word = clean_entry(word)
    filename_base = word.replace(" ", "_")
    output_mp3 = f"/tmp/{filename_base}.mp3"

    print(f"✅ Extracted word: {word}")

    # ------------------------
    # Step 2: Generate audio file via genFrench.sh
    # ------------------------
    cmd = [GEN_SCRIPT, word, f"/tmp/{filename_base}"]
    # print("🎤 Generating audio with Piper...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit("❌ Piper audio generation failed.")
    print(f"✅ Audio generated: {output_mp3}")

    # ------------------------
    # Step 3: Store file in Anki media
    # ------------------------
    media_filename = os.path.basename(output_mp3)
    anki_request("storeMediaFile",
                 filename=media_filename,
                 path=output_mp3)
    print(f"✅ Stored as {media_filename}")
    os.remove(output_mp3)

    # ------------------------
    # Step 4: Append sound tag to Front field
    # ------------------------
    front_value = note_info["fields"]["Front"]["value"]
    sound_tag = f"[sound:{media_filename}]"

    # Insert before the last </pre> if it exists, else append
    if front_value.strip().endswith("</pre>"):
        new_front = re.sub(r"</pre>\s*$", f"{sound_tag}<br></pre>", front_value)
    else:
        # Add a <br> tag for cleaner appearing HTML
        new_front = front_value + f"<br><pre>{sound_tag}<br></pre>"

    update_payload = {"id": note_id, "fields": { "Front": new_front }}
    try:
        anki_request("updateNoteFields", note=update_payload)
        print(f"🎧 Updated note {note_id} Front field with sound tag.")
    except Exception as e:
        print("Anki request failed", e)

