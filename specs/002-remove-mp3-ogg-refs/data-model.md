# Data Model: Remove MP3-to-OGG Conversion References

**Feature**: Remove MP3-to-OGG Conversion References  
**Date**: 2026-03-09  
**Status**: Complete

## Overview

This is a documentation-only feature with minimal data modeling requirements. The "entities" are documentation artifacts and validation rules rather than traditional data structures.

## Core Entities

### 1. SkillDocumentation

**Description**: Represents the SKILL.md file and its structure

**Attributes**:
- `frontmatter`: YAML metadata (name, description)
- `workflow_steps`: List of sequential steps in the agent workflow
- `code_examples`: Python and bash code blocks demonstrating the workflow
- `dependencies`: List of external skills and APIs required

**Validation Rules**:
- Frontmatter MUST include `name` and `description` fields
- Workflow MUST be sequential and numbered
- Code examples MUST be syntactically valid
- Dependencies MUST match actual workflow requirements

**State Transitions**:
- Current state: 3-step workflow (TTS → Convert → Send) with mp3-to-ogg dependency
- Target state: 2-step workflow (TTS → Send) without mp3-to-ogg dependency

**Relationships**:
- References ConstitutionPrinciples for validation
- Contains WorkflowStep entities
- Validated by ValidationTool

---

### 2. WorkflowStep

**Description**: Individual step in the SKILL.md agent workflow

**Attributes**:
- `step_number`: Integer (1, 2, 3, etc.)
- `title`: Brief description of the step
- `code_example`: Code block demonstrating the step
- `dependencies`: Skills/APIs used in this step

**Validation Rules**:
- Steps MUST be numbered sequentially starting from 1
- Each step MUST have a code example
- Code examples MUST be executable

**Current Workflow**:
1. **Generate TTS audio (MP3)**: Uses `tts` API
2. **Convert MP3 to OGG (Opus)**: Uses `mp3-to-ogg` skill and `path-cleaner` skill
3. **Send to WhatsApp**: Uses `message` API

**Target Workflow**:
1. **Generate TTS audio (OGG)**: Uses `tts` API (outputs OGG directly)
2. **Send to WhatsApp**: Uses `path-cleaner` skill and `message` API

**Changes**:
- Remove step 2 (conversion)
- Update step 1 to clarify TTS outputs OGG
- Renumber step 3 to step 2
- Move path-cleaner usage to step 2 (before sending)

---

### 3. ConstitutionPrinciple

**Description**: Validation rule from the project constitution

**Attributes**:
- `name`: Principle name (e.g., "Dependency Transparency")
- `required_keywords`: List of keywords that must appear in SKILL.md
- `validation_status`: PASS or FAIL
- `found_keywords`: Keywords found during validation
- `missing_keywords`: Keywords not found during validation

**Validation Rules**:
- All required_keywords MUST be present in SKILL.md for PASS status
- Case-insensitive keyword matching

**Current State** (Dependency Transparency):
- `required_keywords`: ["mp3-to-ogg", "path-cleaner", "tts", "message"]

**Target State** (Dependency Transparency):
- `required_keywords`: ["path-cleaner", "tts", "message"]

**Changes**:
- Remove "mp3-to-ogg" from required_keywords list
- Update constitution.md to reflect actual dependencies

---

### 4. ValidationTool

**Description**: The scripts/review_skill_doc.py tool that validates SKILL.md

**Attributes**:
- `constitution_principles`: List of ConstitutionPrinciple objects
- `validation_results`: Results of path, code, and constitution checks
- `exit_code`: 0 (pass), 1 (fail), 2 (file not found), 3 (parse error)

**Validation Rules**:
- Tool MUST check all constitution principles
- Tool MUST validate code syntax
- Tool MUST validate file paths

**Current Behavior**:
- Checks for "mp3-to-ogg" keyword in SKILL.md
- Fails if "mp3-to-ogg" is missing

**Target Behavior**:
- Does NOT check for "mp3-to-ogg" keyword
- Passes if "path-cleaner", "tts", and "message" are present

**Changes**:
- Update `load_constitution_principles()` function
- Modify Dependency Transparency principle's required_keywords

---

## Data Flow

### Current Flow (Before Changes)

```
SKILL.md (3 steps, mp3-to-ogg referenced)
    ↓
ValidationTool reads SKILL.md
    ↓
Checks for keywords: ["mp3-to-ogg", "path-cleaner", "tts", "message"]
    ↓
All found → PASS
```

### Target Flow (After Changes)

```
SKILL.md (2 steps, no mp3-to-ogg)
    ↓
ValidationTool reads SKILL.md
    ↓
Checks for keywords: ["path-cleaner", "tts", "message"]
    ↓
All found → PASS
```

---

## File Relationships

```
SKILL.md
    ├── Validated by: scripts/review_skill_doc.py
    ├── Governed by: .specify/memory/constitution.md
    └── Tested with: tests/fixtures/valid_skill.md

scripts/review_skill_doc.py
    ├── Reads: SKILL.md
    ├── References: .specify/memory/constitution.md (hardcoded principles)
    └── Outputs: Validation report (JSON or Markdown)

.specify/memory/constitution.md
    ├── Defines: Dependency Transparency principle
    └── Referenced by: scripts/review_skill_doc.py (indirectly)

tests/fixtures/valid_skill.md
    ├── Mimics: SKILL.md structure
    └── Used for: Testing validation tool
```

---

## Validation Rules Summary

### SKILL.md Validation

| Rule | Current | Target |
|------|---------|--------|
| Workflow steps | 3 steps | 2 steps |
| mp3-to-ogg references | Required | Forbidden (0 occurrences) |
| path-cleaner references | Required | Required |
| tts references | Required | Required |
| message references | Required | Required |
| Code syntax | Valid Python/bash | Valid Python/bash |

### Constitution Validation

| Principle | Current Keywords | Target Keywords |
|-----------|------------------|-----------------|
| Single Responsibility | TTS, WhatsApp, audio | TTS, WhatsApp, audio (unchanged) |
| Format Compatibility | OGG, Opus | OGG, Opus (unchanged) |
| Dependency Transparency | mp3-to-ogg, path-cleaner, tts, message | path-cleaner, tts, message |

---

## Implementation Notes

### Files to Modify

1. **SKILL.md**
   - Remove step 2 (MP3 to OGG conversion)
   - Update step 1 to clarify TTS outputs OGG
   - Renumber step 3 to step 2
   - Update variable names (clean_mp3_path → clean_ogg_path)
   - Remove bash code block calling convert_mp3_to_ogg.py
   - Update frontmatter description if needed

2. **scripts/review_skill_doc.py**
   - Locate `load_constitution_principles()` function (around line 485)
   - Update Dependency Transparency required_keywords
   - Change from: `["mp3-to-ogg", "path-cleaner", "tts", "message"]`
   - Change to: `["path-cleaner", "tts", "message"]`

3. **.specify/memory/constitution.md**
   - Update line 23 (Principle III description)
   - Remove `mp3-to-ogg` from dependency list
   - Keep path-cleaner, tts, message

4. **tests/fixtures/valid_skill.md** (optional)
   - Update to match new SKILL.md structure
   - Ensure it passes validation with updated tool

---

## Success Criteria Mapping

| Success Criterion | Data Model Validation |
|-------------------|----------------------|
| SC-001: Zero "mp3-to-ogg" references | SkillDocumentation.dependencies excludes mp3-to-ogg |
| SC-002: Exactly 2 workflow steps | SkillDocumentation.workflow_steps.length == 2 |
| SC-003: Validation PASS status | ValidationTool.exit_code == 0 |
| SC-004: Code examples execute | WorkflowStep.code_example is syntactically valid |
| SC-005: TTS outputs OGG | WorkflowStep[1].title mentions OGG output |

---

## No Traditional Database Schema

This feature does not involve databases, APIs, or persistent data storage. All "entities" are documentation artifacts (markdown files) and in-memory validation objects (Python dataclasses in review_skill_doc.py).
