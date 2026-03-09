---
name: test-skill
description: A valid test skill for TTS to WhatsApp audio using OGG Opus format
---

# Test Skill

This skill demonstrates proper documentation with mp3-to-ogg, path-cleaner, tts, and message dependencies.

## Agent Workflow

When processing audio:

1. Generate TTS audio:
    ```python
    response = api.tts(text="hello")
    output = response["output"]
    ```

2. Convert to OGG format with Opus codec:
    ```bash
    python convert.py input.mp3
    ```

3. Send via message API to WhatsApp.
