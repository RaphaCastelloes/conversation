# Research: Remove MP3-to-OGG Conversion References

**Feature**: Remove MP3-to-OGG Conversion References  
**Date**: 2026-03-09  
**Status**: Complete

## Overview

This research phase addresses technical decisions for updating documentation to remove mp3-to-ogg library references. Since this is a documentation-only change with minimal technical complexity, research focuses on ensuring consistency and validation.

## Research Questions

### 1. Documentation Update Strategy

**Question**: What is the best approach to update SKILL.md while maintaining clarity for AI agents?

**Decision**: Direct text replacement with workflow simplification

**Rationale**:
- The change is straightforward: remove step 2 (MP3 to OGG conversion) from the workflow
- TTS tool now outputs OGG directly, so the intermediate conversion is obsolete
- AI agents need clear, linear workflows without deprecated steps
- Maintaining the same documentation structure (frontmatter, workflow sections, code examples) ensures consistency

**Alternatives Considered**:
- **Add deprecation notice**: Rejected because mp3-to-ogg is completely removed, not deprecated
- **Keep conversion as optional**: Rejected because TTS now handles OGG output natively
- **Create migration guide**: Rejected as out of scope (only documentation update, not code migration)

**Implementation Notes**:
- Update frontmatter description to clarify TTS outputs OGG directly
- Simplify workflow from 3 steps to 2 steps
- Update Python code example to show TTS returning OGG path
- Remove bash code block that calls convert_mp3_to_ogg.py
- Verify path-cleaner is still needed (assumption: yes, for MEDIA: prefix cleaning)

---

### 2. Constitution Validation Tool Update

**Question**: How should the review_skill_doc.py tool be updated to reflect new dependencies?

**Decision**: Update hardcoded Dependency Transparency keywords in load_constitution_principles() function

**Rationale**:
- The validation tool currently checks for specific keywords: ["mp3-to-ogg", "path-cleaner", "tts", "message"]
- Removing "mp3-to-ogg" from this list aligns validation with actual dependencies
- This is a simple list modification in the ConstitutionPrinciple definition
- No changes to validation logic or data structures needed

**Alternatives Considered**:
- **Load keywords from constitution.md dynamically**: Rejected as over-engineering for this simple change
- **Make keywords configurable via CLI**: Rejected as out of scope
- **Remove Dependency Transparency check entirely**: Rejected because other dependencies still need validation

**Implementation Notes**:
- Locate the `load_constitution_principles()` function in scripts/review_skill_doc.py
- Update the Dependency Transparency principle's required_keywords list
- Change from: `["mp3-to-ogg", "path-cleaner", "tts", "message"]`
- Change to: `["path-cleaner", "tts", "message"]`
- Run validation after update to ensure SKILL.md passes

---

### 3. Constitution Document Update

**Question**: Should the constitution.md file be updated to reflect the dependency change?

**Decision**: Yes, update Principle III (Dependency Transparency) to remove mp3-to-ogg reference

**Rationale**:
- Constitution states: "The skill explicitly declares its dependencies on external skills (`mp3-to-ogg`, `path-cleaner`) and APIs (`tts`, `message`)"
- This list must match actual dependencies for accuracy
- Constitution is the source of truth for project principles
- Keeping outdated dependencies in constitution creates confusion

**Alternatives Considered**:
- **Leave constitution unchanged**: Rejected because it would be inaccurate
- **Add version history**: Considered but out of scope for this change
- **Mark mp3-to-ogg as deprecated**: Rejected because it's completely removed, not deprecated

**Implementation Notes**:
- Update line 23 in .specify/memory/constitution.md
- Remove `mp3-to-ogg` from the dependency list
- Maintain the same principle structure and rationale
- No version bump needed (constitution version remains 1.0.0 as this is a correction, not a principle change)

---

### 4. Test Fixture Updates

**Question**: Do test fixtures need updates to reflect the new dependency list?

**Decision**: Update valid_skill.md fixture to remove mp3-to-ogg references

**Rationale**:
- tests/fixtures/valid_skill.md is used to test successful validation
- It should demonstrate a valid SKILL.md that passes all constitution checks
- Removing mp3-to-ogg references ensures the fixture remains valid after the tool update

**Alternatives Considered**:
- **Leave fixtures unchanged**: Rejected because valid_skill.md would fail validation after tool update
- **Create new fixture**: Rejected as unnecessary; updating existing fixture is simpler
- **Remove fixtures entirely**: Rejected because they're useful for testing

**Implementation Notes**:
- Update tests/fixtures/valid_skill.md to remove mp3-to-ogg from dependency list
- Ensure it still includes path-cleaner, tts, and message keywords
- Verify missing_principles.md doesn't need updates (it's designed to fail validation)

---

### 5. Path-Cleaner Dependency Verification

**Question**: Is the path-cleaner utility still needed after removing mp3-to-ogg?

**Decision**: Yes, path-cleaner is still required for cleaning MEDIA: prefix from TTS output

**Rationale**:
- Current SKILL.md shows: `clean_mp3_path = default_api.exec(command = "python /home/opc/.openclaw/workspace/skills/path-cleaner/scripts/clean_media_path.py " + mp3_path)`
- This step cleans the MEDIA: prefix before conversion
- Even though TTS outputs OGG directly, the path still needs cleaning
- The output variable should be renamed from `clean_mp3_path` to `clean_ogg_path` for clarity

**Alternatives Considered**:
- **Remove path-cleaner entirely**: Rejected because TTS output paths still have MEDIA: prefix
- **Assume TTS outputs clean paths**: Rejected as unverified assumption
- **Make path-cleaner optional**: Rejected because it's still required

**Implementation Notes**:
- Keep path-cleaner in dependency list
- Update SKILL.md to show path-cleaner being used on TTS output (OGG file)
- Rename variables from `clean_mp3_path` to `clean_ogg_path` for accuracy
- Update code example to reflect: TTS → path-cleaner → WhatsApp send

---

## Summary of Decisions

| Decision Area | Choice | Impact |
|--------------|--------|--------|
| Documentation Strategy | Direct replacement, workflow simplification | SKILL.md updated to 2-step process |
| Validation Tool | Update hardcoded keywords in load_constitution_principles() | scripts/review_skill_doc.py modified |
| Constitution Update | Remove mp3-to-ogg from Principle III | .specify/memory/constitution.md updated |
| Test Fixtures | Update valid_skill.md to match new dependencies | tests/fixtures/valid_skill.md modified |
| Path-Cleaner | Keep as required dependency | Remains in all documentation and validation |

## Technical Constraints Confirmed

- **Backward Compatibility**: Documentation changes don't affect existing code; old workflows remain functional
- **AI Agent Clarity**: Simplified 2-step workflow is clearer and easier to execute
- **Validation Accuracy**: Constitution validation will pass after all updates are applied
- **No Code Changes**: This is purely a documentation update; no Python/bash scripts are modified (except validation tool)

## Next Steps (Phase 1)

1. Generate data-model.md (minimal - only documentation entities)
2. Skip contracts/ (no external interfaces for documentation)
3. Generate quickstart.md with update instructions
4. Update agent context with documentation change details
