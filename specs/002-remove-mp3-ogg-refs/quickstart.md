# Quickstart: Remove MP3-to-OGG Conversion References

**Feature**: Remove MP3-to-OGG Conversion References  
**Date**: 2026-03-09  
**Audience**: Developers implementing this documentation update

## Overview

This guide provides step-by-step instructions for updating SKILL.md and related files to remove mp3-to-ogg library references. The TTS tool now outputs OGG (Opus) format directly, eliminating the need for MP3 to OGG conversion.

## Prerequisites

- Git repository access with branch `002-remove-mp3-ogg-refs` checked out
- Python 3.9+ installed (for running validation tool)
- Text editor for modifying markdown and Python files

## Quick Start (5 minutes)

### Step 1: Update SKILL.md

**File**: `SKILL.md`

**Changes Required**:

1. **Update frontmatter description** (if it mentions MP3 to OGG conversion):
   ```yaml
   # Before
   description: Sends text-to-speech (TTS) audio to WhatsApp, ensuring compatibility with OGG (Opus) format. Use to send text-generated audio messages directly to the user's WhatsApp.
   
   # After (if needed - current description is already correct)
   description: Sends text-to-speech (TTS) audio to WhatsApp in OGG (Opus) format. The TTS tool outputs OGG directly. Use to send text-generated audio messages to the user's WhatsApp.
   ```

2. **Simplify workflow from 3 steps to 2 steps**:

   **Remove this entire section** (Step 2):
   ```markdown
   2.  **Convert MP3 to OGG (Opus):** Use the `mp3-to-ogg` skill to convert the generated MP3 file to OGG (Opus), ensuring WhatsApp compatibility. To do this, execute the `convert_mp3_to_ogg.py` script from the `mp3-to-ogg` skill.
       ```bash
       # First, clean the MEDIA: prefix from the MP3 path
       clean_mp3_path = default_api.exec(command = "python /home/opc/.openclaw/workspace/skills/path-cleaner/scripts/clean_media_path.py " + mp3_path)
       clean_mp3_path = clean_mp3_path["exec_response"]["output"].strip()

       # Convert to OGG
       ogg_conversion_output = default_api.exec(command = "python /home/opc/.openclaw/workspace/skills/mp3-to-ogg/scripts/convert_mp3_to_ogg.py " + clean_mp3_path)
       ogg_path = ogg_conversion_output["exec_response"]["output"].strip().split('\n')[-1]
       ```
   ```

3. **Update Step 1** to clarify TTS outputs OGG:
   ```markdown
   # Before
   1.  **Generate TTS audio (MP3):** Use the `tts` tool with the message provided by the user.
       ```python
       tts_response = default_api.tts(text = "<user_message>")
       mp3_path = tts_response["tts_response"]["output"]
       ```
   
   # After
   1.  **Generate TTS audio (OGG):** Use the `tts` tool with the message provided by the user. The TTS tool outputs OGG (Opus) format directly.
       ```python
       tts_response = default_api.tts(text = "<user_message>")
       ogg_path = tts_response["tts_response"]["output"]
       ```
   ```

4. **Update Step 3 to Step 2** and add path cleaning:
   ```markdown
   # Before (was Step 3)
   3.  **Send the OGG audio to WhatsApp:** Use the `message` tool with the OGG file path and the recipient's number (obtained from `USER.md`).
       ```python
       user_number = "+553288314794" # Replace with the actual number from USER.md
       default_api.message(action = "send", channel = "whatsapp", media = ogg_path, message = "<original_message>", to = user_number)
       ```
   
   # After (now Step 2)
   2.  **Send the OGG audio to WhatsApp:** Clean the MEDIA: prefix from the OGG path using `path-cleaner`, then use the `message` tool with the cleaned path and the recipient's number (obtained from `USER.md`).
       ```python
       # Clean the MEDIA: prefix from the OGG path
       clean_ogg_path = default_api.exec(command = "python /home/opc/.openclaw/workspace/skills/path-cleaner/scripts/clean_media_path.py " + ogg_path)
       clean_ogg_path = clean_ogg_path["exec_response"]["output"].strip()
       
       # Send to WhatsApp
       user_number = "+553288314794" # Replace with the actual number from USER.md
       default_api.message(action = "send", channel = "whatsapp", media = clean_ogg_path, message = "<original_message>", to = user_number)
       ```
   ```

5. **Update final summary** (if present):
   ```markdown
   # Before
   The final result will be sending an OGG audio compatible with WhatsApp containing the provided text message.
   
   # After (optional enhancement)
   The final result will be sending an OGG (Opus) audio compatible with WhatsApp containing the provided text message. The TTS tool outputs OGG format directly, eliminating the need for MP3 to OGG conversion.
   ```

---

### Step 2: Update Constitution Validation Tool

**File**: `scripts/review_skill_doc.py`

**Locate the function** (around line 485):
```python
def load_constitution_principles() -> List[ConstitutionPrinciple]:
    """Define the three constitution principles with required keywords."""
    return [
        ConstitutionPrinciple(
            name="Single Responsibility",
            required_keywords=["TTS", "WhatsApp", "audio"]
        ),
        ConstitutionPrinciple(
            name="Format Compatibility",
            required_keywords=["OGG", "Opus"]
        ),
        ConstitutionPrinciple(
            name="Dependency Transparency",
            required_keywords=["mp3-to-ogg", "path-cleaner", "tts", "message"]  # ← UPDATE THIS LINE
        )
    ]
```

**Make this change**:
```python
# Before
required_keywords=["mp3-to-ogg", "path-cleaner", "tts", "message"]

# After
required_keywords=["path-cleaner", "tts", "message"]
```

---

### Step 3: Update Constitution Document

**File**: `.specify/memory/constitution.md`

**Locate line 23** (Principle III):
```markdown
# Before
The skill explicitly declares its dependencies on external skills (`mp3-to-ogg`, `path-cleaner`) and APIs (`tts`, `message`).

# After
The skill explicitly declares its dependencies on external skills (`path-cleaner`) and APIs (`tts`, `message`).
```

---

### Step 4: Validate Changes

Run the validation tool to ensure all changes are correct:

```bash
python scripts/review_skill_doc.py
```

**Expected Output**:
```
# SKILL.md Review Report

**Status**: ✅ PASS (or ⚠️ WARNING if external paths detected)

## Constitution Alignment

✅ **Single Responsibility**: All required keywords found: TTS, WhatsApp, audio
✅ **Format Compatibility**: All required keywords found: OGG, Opus
✅ **Dependency Transparency**: All required keywords found: path-cleaner, tts, message
```

**If validation fails**:
- Check that you removed ALL occurrences of "mp3-to-ogg" from SKILL.md
- Verify the validation tool was updated correctly
- Ensure path-cleaner, tts, and message are still mentioned in SKILL.md

---

### Step 5: Update Test Fixtures (Optional)

**File**: `tests/fixtures/valid_skill.md`

Update this file to match the new SKILL.md structure (2 steps, no mp3-to-ogg references). This ensures future tests use the correct format.

---

## Verification Checklist

After completing all steps, verify:

- [ ] SKILL.md has exactly 2 workflow steps (not 3)
- [ ] SKILL.md contains zero references to "mp3-to-ogg" or "convert_mp3_to_ogg.py"
- [ ] SKILL.md mentions that TTS outputs OGG format directly
- [ ] SKILL.md still references path-cleaner for cleaning MEDIA: prefix
- [ ] scripts/review_skill_doc.py no longer checks for "mp3-to-ogg" keyword
- [ ] .specify/memory/constitution.md no longer lists mp3-to-ogg as a dependency
- [ ] Running `python scripts/review_skill_doc.py` shows constitution alignment PASS
- [ ] Code examples in SKILL.md are syntactically valid

---

## Troubleshooting

### Issue: Validation still fails with "Missing keywords: mp3-to-ogg"

**Solution**: You didn't update scripts/review_skill_doc.py correctly. Re-check Step 2 and ensure you removed "mp3-to-ogg" from the required_keywords list.

---

### Issue: SKILL.md still has 3 steps

**Solution**: You didn't remove Step 2 (the conversion step). Delete the entire section including the bash code block that calls convert_mp3_to_ogg.py.

---

### Issue: Path-cleaner is missing from SKILL.md

**Solution**: Path-cleaner is still needed! Add it to Step 2 (sending to WhatsApp) to clean the MEDIA: prefix from the OGG path before sending.

---

### Issue: Variable names are confusing (mp3_path vs ogg_path)

**Solution**: Update all variable names for consistency:
- `mp3_path` → `ogg_path` (TTS output)
- `clean_mp3_path` → `clean_ogg_path` (path-cleaner output)

---

## Testing

### Manual Test

1. Read the updated SKILL.md as if you were an AI agent
2. Verify the workflow is clear and executable
3. Confirm there are no references to deprecated mp3-to-ogg conversion

### Automated Test

```bash
# Run validation tool
python scripts/review_skill_doc.py

# Expected: Exit code 0 (PASS) or 0 (WARNING for external paths)
echo $?  # Should be 0
```

### Regression Test

```bash
# Test with valid fixture
python scripts/review_skill_doc.py --skill-file tests/fixtures/valid_skill.md

# Expected: PASS status
```

---

## Summary

This update simplifies the WhatsApp audio sender workflow by removing the obsolete MP3 to OGG conversion step. The TTS tool now outputs OGG (Opus) format directly, reducing complexity and potential failure points.

**Files Modified**:
1. SKILL.md - Simplified workflow from 3 to 2 steps
2. scripts/review_skill_doc.py - Updated Dependency Transparency keywords
3. .specify/memory/constitution.md - Removed mp3-to-ogg from dependency list

**Time to Complete**: ~5 minutes  
**Risk Level**: Low (documentation-only change)  
**Testing Required**: Run validation tool to confirm PASS status
