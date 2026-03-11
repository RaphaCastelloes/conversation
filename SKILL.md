---
name: conversation
description: Enables conversation with users via WhatsApp by sending text-to-speech (TTS) audio messages in OGG (Opus) format. Use to send text-generated audio messages directly to the user's WhatsApp.
---

# Conversation

This skill enables conversation with users by automating the process of sending text-generated audio messages to the user's WhatsApp, ensuring the format is compatible (OGG with Opus codec).

## When to Use

Use this skill when:
- When the user send an audio message
- The user explicitly asks to send a TTS audio message to WhatsApp
- The user sends a text message that needs to be converted to audio and sent via WhatsApp
- You need to send any text-generated audio to the user's WhatsApp

## Agent Workflow

When a request to send TTS audio to WhatsApp is received, the agent should follow these steps:

1.  **Generate TTS audio (OGG):** Use the `tts` tool with the message provided by the user. The TTS tool outputs OGG (Opus) format directly.
    ```python
    tts_response = default_api.tts(text = "<user_message>")
    ogg_path = tts_response["tts_response"]["output"]
    ```

2.  **Send the OGG audio to WhatsApp:** Clean the MEDIA: prefix from the OGG path using `path-cleaner`, then use the `exec` tool to run the `openclaw message send` command with the cleaned path and the recipient's number (obtained from `USER.md`).
    ```python
    # Clean the MEDIA: prefix from the OGG path
    clean_ogg_path = default_api.exec(command = "python /home/opc/.openclaw/workspace/skills/path-cleaner/scripts/clean_media_path.py " + ogg_path)
    clean_ogg_path = clean_ogg_path["exec_response"]["output"].strip()
    
    # Send to WhatsApp
    user_number = "+553288314794" # Replace with the actual number from USER.md
    default_api.exec(command = f'openclaw message send --channel whatsapp --target "{user_number}" --media "{clean_ogg_path}" --message "<original_message>"')
    ```

The final result will be sending an OGG (Opus) audio compatible with WhatsApp containing the provided text message. The TTS tool outputs OGG (Opus) format directly.
