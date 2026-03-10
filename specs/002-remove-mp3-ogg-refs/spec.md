# Feature Specification: Remove MP3-to-OGG Conversion References

**Feature Branch**: `002-remove-mp3-ogg-refs`  
**Created**: 2026-03-09  
**Status**: Draft  
**Input**: User description: "Remove all references to the ogg-to-mp3 library. The tts skill handles the convertion."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Update SKILL.md Documentation (Priority: P1)

As a developer or AI agent using this skill, I need the SKILL.md to accurately reflect that the TTS tool now outputs OGG format directly, so that I don't attempt to use the deprecated mp3-to-ogg conversion step.

**Why this priority**: This is the core documentation change that prevents confusion and incorrect implementation. Without this update, users will follow outdated workflow instructions that reference non-existent dependencies.

**Independent Test**: Can be fully tested by reviewing the updated SKILL.md and verifying that: (1) no references to mp3-to-ogg skill exist, (2) the workflow shows TTS outputting OGG directly, (3) all code examples reflect the simplified flow.

**Acceptance Scenarios**:

1. **Given** the SKILL.md contains references to mp3-to-ogg skill, **When** the documentation is updated, **Then** all mentions of mp3-to-ogg conversion are removed
2. **Given** the workflow describes a 3-step process (TTS → Convert → Send), **When** the documentation is updated, **Then** the workflow describes a 2-step process (TTS → Send)
3. **Given** code examples show MP3 conversion, **When** the documentation is updated, **Then** code examples show TTS outputting OGG format directly

---

### User Story 2 - Update Constitution Validation (Priority: P2)

As a documentation maintainer, I need the constitution validation tool to reflect the updated dependency list, so that SKILL.md validation passes with the correct dependencies.

**Why this priority**: The review tool currently expects mp3-to-ogg as a required dependency. After removing it from SKILL.md, validation will fail unless the constitution principles are updated.

**Independent Test**: Can be tested by running `python scripts/review_skill_doc.py` and verifying that constitution alignment checks pass without requiring mp3-to-ogg keywords.

**Acceptance Scenarios**:

1. **Given** the constitution requires mp3-to-ogg in Dependency Transparency, **When** the principle is updated, **Then** mp3-to-ogg is no longer a required keyword
2. **Given** the updated SKILL.md without mp3-to-ogg references, **When** validation runs, **Then** constitution alignment shows PASS status

---

### Edge Cases

- What happens if the TTS tool output format changes in the future (e.g., returns MP3 instead of OGG)?
- How does the system handle backward compatibility if older documentation or code still references mp3-to-ogg?
- What if path-cleaner is still needed for the TTS output path?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: SKILL.md MUST remove all references to the mp3-to-ogg skill and conversion step
- **FR-002**: SKILL.md MUST update the workflow to show TTS outputting OGG format directly
- **FR-003**: SKILL.md MUST update code examples to reflect the simplified 2-step process (TTS → Send)
- **FR-004**: SKILL.md MUST remove the bash code block that calls convert_mp3_to_ogg.py
- **FR-005**: Constitution validation tool MUST update Dependency Transparency principle to remove mp3-to-ogg from required keywords
- **FR-006**: SKILL.md MUST clarify whether path-cleaner is still needed for TTS output paths
- **FR-007**: SKILL.md description/frontmatter MUST be updated if it references MP3 to OGG conversion

### Key Entities

- **SKILL.md**: The main documentation file that describes the WhatsApp audio sender workflow
- **Constitution Principles**: The validation rules in scripts/review_skill_doc.py that check for required dependencies
- **Workflow Steps**: The sequential process documented in SKILL.md for sending TTS audio to WhatsApp

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: SKILL.md contains zero references to "mp3-to-ogg" or "convert_mp3_to_ogg.py"
- **SC-002**: Workflow section describes exactly 2 steps instead of 3 (TTS generation and WhatsApp sending)
- **SC-003**: Running `python scripts/review_skill_doc.py` shows constitution alignment PASS status
- **SC-004**: Code examples in SKILL.md execute successfully without calling mp3-to-ogg conversion
- **SC-005**: Documentation clearly states that TTS outputs OGG format compatible with WhatsApp

## Assumptions *(mandatory)*

- The TTS tool now outputs OGG (Opus) format directly, eliminating the need for MP3 to OGG conversion
- The path-cleaner utility may still be needed to clean the MEDIA: prefix from TTS output paths
- No other skills or documentation files reference the mp3-to-ogg dependency
- The WhatsApp message API accepts OGG files directly from the TTS output

## Out of Scope *(mandatory)*

- Removing or archiving the actual mp3-to-ogg skill repository (only documentation references are being removed)
- Updating any other skills that might use mp3-to-ogg for different purposes
- Modifying the TTS tool itself or its output format
- Testing the actual TTS to WhatsApp workflow execution (only documentation updates)

## Dependencies & Constraints

**Dependencies**:
- Current SKILL.md file exists and contains mp3-to-ogg references
- Constitution validation tool (scripts/review_skill_doc.py) exists and is functional

**Constraints**:
- Changes must maintain backward compatibility for any existing code that might still use the old workflow
- Documentation must remain clear and accurate for AI agents interpreting the workflow
