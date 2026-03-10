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
    api.exec(command=f'openclaw message send --channel whatsapp --target "+1234567890" --media "{clean_path}" --message "hello"')
    ```
