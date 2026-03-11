# Data Model: Rename Skill to 'Conversation'

**Feature**: 003-rename-skill-conversation  
**Date**: 2026-03-10  
**Status**: Complete

## Overview

This feature involves modifying the SKILL.md file structure. While this is a documentation file rather than a traditional data model, we document its structure to ensure consistent updates.

## Entities

### SKILL.md File Structure

**Purpose**: Primary skill definition file that LLM agents read to understand skill capabilities and usage.

**Format**: Markdown file with YAML frontmatter

**Structure**:
```yaml
---
name: [skill-name]
description: [skill-description]
---

# [Skill Title]

[Skill overview paragraph]

## Agent Workflow

[Workflow steps and code examples]
```

**Fields to Modify**:

| Field | Current Value | New Value | Validation Rule |
|-------|---------------|-----------|-----------------|
| `name` | `whatsapp-audio-sender` | `conversation` | Must be lowercase, alphanumeric with hyphens |
| `description` | "Sends text-to-speech (TTS) audio to WhatsApp..." | "Enables conversation with users via WhatsApp by sending text-to-speech (TTS) audio messages..." | Must describe current functionality accurately |
| Title (H1) | "WhatsApp Audio Sender" | "Conversation" | Should match the skill's new identity |
| Overview paragraph | "This skill automates the process of sending text-generated audio messages..." | "This skill enables conversation with users by automating the process of sending text-generated audio messages..." | Should align with new description |

**Fields to Preserve**:

| Field | Preservation Rule |
|-------|-------------------|
| `Agent Workflow` section | Must remain completely unchanged - contains critical execution steps |
| Code examples | Must remain unchanged - contains exact API calls and paths |
| Dependency references | Must remain unchanged - references to `path-cleaner`, `tts`, `message` |
| Format specifications | Must remain unchanged - OGG/Opus format requirements |

**Relationships**:
- **SKILL.md** references → **scripts/clean_media_path.py** (dependency, unchanged)
- **SKILL.md** references → External APIs: `tts`, `message`, `exec` (dependencies, unchanged)
- **SKILL.md** references → **path-cleaner** skill (external dependency, unchanged)

## Validation Rules

### Name Field
- **Format**: Lowercase letters, numbers, and hyphens only
- **Length**: 3-50 characters
- **Pattern**: `^[a-z0-9-]+$`
- **Example Valid**: `conversation`, `user-auth`, `data-sync`
- **Example Invalid**: `Conversation`, `conversation_tool`, `conv.`

### Description Field
- **Format**: Plain text, single paragraph
- **Length**: 50-500 characters
- **Must Include**: Current functionality description (TTS, WhatsApp, OGG/Opus)
- **Must Avoid**: Implementation details, version numbers, author names

### Workflow Section
- **Preservation**: Must remain byte-for-byte identical
- **Rationale**: Contains tested, working code examples that agents depend on

## State Transitions

This is a one-time state change:

```
State: BEFORE RENAME
├── name: "whatsapp-audio-sender"
├── description: "Sends text-to-speech..."
└── title: "WhatsApp Audio Sender"

        ↓ [Apply Rename]

State: AFTER RENAME
├── name: "conversation"
├── description: "Enables conversation with users via WhatsApp..."
└── title: "Conversation"
```

**Invariants**:
- Agent Workflow section remains unchanged
- File format remains Markdown with YAML frontmatter
- Dependency declarations remain intact
- Code examples remain executable

## Edge Cases

### Case 1: Partial Update
**Scenario**: Only name field updated, description not updated  
**Impact**: Inconsistency between name and description  
**Mitigation**: Atomic update of both fields in single commit

### Case 2: Workflow Section Modified
**Scenario**: Accidental modification to Agent Workflow during rename  
**Impact**: Breaking change to agent execution  
**Mitigation**: Validation step to diff workflow section before/after

### Case 3: YAML Frontmatter Syntax Error
**Scenario**: Invalid YAML syntax after edit  
**Impact**: File becomes unparseable by agents  
**Mitigation**: YAML validation before commit

## Non-Entities

The following are **NOT** part of this data model and should not be modified:

- **scripts/clean_media_path.py**: Python script (no changes)
- **tests/**: Test files (no changes)
- **specs/**: Historical specification files (no changes)
- **.specify/**: Specification framework (no changes)

## Summary

This data model defines the structure of SKILL.md and the precise fields that must be updated during the rename. The key principle is surgical precision: update only the identity fields (name, description, title) while preserving all functional documentation (workflow, code examples, dependencies).
