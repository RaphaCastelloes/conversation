---
name: whatsapp-audio-sender
description: Sends text-to-speech (TTS) audio to WhatsApp, ensuring compatibility with OGG (Opus) format. Use to send text-generated audio messages directly to the user's WhatsApp.
---

# WhatsApp Audio Sender

This skill automates the process of sending text-generated audio messages to the user's WhatsApp, ensuring the format is compatible (OGG with Opus codec).

## Agent Workflow

When a request to send TTS audio to WhatsApp is received, the agent should follow these steps:

1.  **Generate TTS audio (MP3):** Use the `tts` tool with the message provided by the user.
    ```python
    tts_response = default_api.tts(text = "<user_message>")
    mp3_path = tts_response["tts_response"]["output"]
    ```

2.  **Convert MP3 to OGG (Opus):** Use the `mp3-to-ogg` skill to convert the generated MP3 file to OGG (Opus), ensuring WhatsApp compatibility. To do this, execute the `convert_mp3_to_ogg.py` script from the `mp3-to-ogg` skill.
    ```bash
    # First, clean the MEDIA: prefix from the MP3 path
    clean_mp3_path = default_api.exec(command = "python /home/opc/.openclaw/workspace/skills/path-cleaner/scripts/clean_media_path.py " + mp3_path)
    clean_mp3_path = clean_mp3_path["exec_response"]["output"].strip()

    # Convert to OGG
    ogg_conversion_output = default_api.exec(command = "python /home/opc/.openclaw/workspace/skills/mp3-to-ogg/scripts/convert_mp3_to_ogg.py " + clean_mp3_path)
    ogg_path = ogg_conversion_output["exec_response"]["output"].strip().split('\n')[-1]
    ```

3.  **Send the OGG audio to WhatsApp:** Use the `message` tool with the OGG file path and the recipient's number (obtained from `USER.md`).
    ```python
    user_number = "+553288314794" # Replace with the actual number from USER.md
    default_api.message(action = "send", channel = "whatsapp", media = ogg_path, message = "<original_message>", to = user_number)
    ```

The final result will be sending an OGG audio compatible with WhatsApp containing the provided text message.
