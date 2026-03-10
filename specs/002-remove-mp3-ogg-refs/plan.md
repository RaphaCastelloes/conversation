# Implementation Plan: Remove MP3-to-OGG Conversion References

**Branch**: `002-remove-mp3-ogg-refs` | **Date**: 2026-03-09 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-remove-mp3-ogg-refs/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Update SKILL.md documentation to remove all references to the mp3-to-ogg library since the TTS tool now outputs OGG (Opus) format directly. This is a documentation-only change that simplifies the workflow from 3 steps to 2 steps (TTS → Send instead of TTS → Convert → Send). Additionally, update the constitution validation tool to remove mp3-to-ogg from the Dependency Transparency principle's required keywords.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.9+ (for validation tool), Markdown (for documentation)
**Primary Dependencies**: Python stdlib only (pathlib, re, ast for review_skill_doc.py)
**Storage**: N/A (documentation files only)
**Testing**: Manual validation via `python scripts/review_skill_doc.py`
**Target Platform**: Cross-platform (documentation is platform-agnostic)
**Project Type**: Documentation update with validation tool modification
**Performance Goals**: N/A (documentation changes)
**Constraints**: Must maintain backward compatibility; documentation must remain clear for AI agents
**Scale/Scope**: 2 files to modify (SKILL.md, scripts/review_skill_doc.py)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Single Responsibility ✅
**Status**: PASS
**Assessment**: This feature maintains single responsibility by updating documentation to accurately reflect the simplified workflow. The skill still has one clear purpose: convert text to speech and send via WhatsApp in OGG/Opus format.

### Principle II: Format Compatibility (NON-NEGOTIABLE) ✅
**Status**: PASS
**Assessment**: This change reinforces format compatibility by documenting that TTS now outputs OGG/Opus directly, eliminating the conversion step. The documentation will continue to emphasize that WhatsApp requires OGG/Opus format.

### Principle III: Dependency Transparency ✅
**Status**: PASS (with required updates)
**Assessment**: This feature updates dependency transparency by removing the outdated mp3-to-ogg dependency from documentation. The constitution itself states dependencies must be kept up-to-date in SKILL.md. This change fulfills that requirement.

**Required Constitution Updates**:
- Update line 23 in constitution.md to remove `mp3-to-ogg` from the dependency list
- Current: "The skill explicitly declares its dependencies on external skills (`mp3-to-ogg`, `path-cleaner`) and APIs (`tts`, `message`)."
- Updated: "The skill explicitly declares its dependencies on external skills (`path-cleaner`) and APIs (`tts`, `message`)."

**Gate Decision**: ✅ PASS - All principles align. The feature improves dependency transparency by removing obsolete references.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# Documentation-only change - existing structure
SKILL.md                           # Main documentation file (TO BE UPDATED)
scripts/
└── review_skill_doc.py            # Constitution validation tool (TO BE UPDATED)

.specify/
└── memory/
    └── constitution.md            # Project constitution (TO BE UPDATED)

tests/
└── fixtures/
    ├── valid_skill.md             # Test fixture (may need update)
    ├── invalid_paths.md           # Test fixture
    └── missing_principles.md      # Test fixture (may need update)
```

**Structure Decision**: This is a documentation update feature affecting existing files. No new source code directories are needed. The changes are limited to:
1. SKILL.md - Remove mp3-to-ogg references and update workflow
2. scripts/review_skill_doc.py - Update Dependency Transparency keywords
3. .specify/memory/constitution.md - Update dependency list in Principle III

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
