---
name: test-skill
description: A valid test skill for TTS to WhatsApp audio using OGG Opus format
---

# Test Skill

This skill demonstrates proper documentation with path-cleaner, tts, and message dependencies.

## Agent Workflow

When processing audio:

1. Generate TTS audio:
    ```python
    response = api.tts(text="hello")
    output = response["output"]
    ```

2. Send via message API to WhatsApp:
    ```python
    # Clean the path and send
    clean_path = api.exec(command="python /path/to/cleaner.py " + output)
    api.message(action="send", channel="whatsapp", media=clean_path, to="+1234567890")
    ```
