# Implementation Plan: Rename Skill to 'Conversation'

**Branch**: `003-rename-skill-conversation` | **Date**: 2026-03-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-rename-skill-conversation/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

This feature renames the skill from "whatsapp-audio-sender" to "conversation" to reflect a broader purpose beyond just audio sending. The implementation involves updating the SKILL.md file's name and description fields, reviewing all documentation for references to the old name, and ensuring zero functional regression. This is a documentation-focused change with no code modifications required.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Markdown (documentation only)  
**Primary Dependencies**: None (documentation change)  
**Storage**: N/A  
**Testing**: Manual verification via grep/search for old skill name references  
**Target Platform**: Documentation files (SKILL.md, README, specs)
**Project Type**: LLM skill documentation  
**Performance Goals**: N/A (documentation change)  
**Constraints**: Must maintain backward compatibility for external systems referencing old name  
**Scale/Scope**: ~5-10 documentation files to review and update

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Single Responsibility ✅ PASS
**Assessment**: This rename does not change the skill's single responsibility (text-to-speech via WhatsApp). The skill continues to have one clear purpose; only the name changes to better reflect potential future expansion while maintaining current functionality.

### Principle II: Format Compatibility (NON-NEGOTIABLE) ✅ PASS
**Assessment**: No changes to audio format handling. OGG/Opus validation and workflow remain unchanged. This is purely a documentation update.

### Principle III: Dependency Transparency ✅ PASS
**Assessment**: SKILL.md workflow documentation will be preserved. Dependencies on `path-cleaner`, `tts`, and `message` APIs remain clearly documented with exact command sequences.

**GATE STATUS**: ✅ ALL CHECKS PASSED - Proceed to Phase 0

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
whatsapp-audio-sender/
├── SKILL.md              # Primary file to update (name + description)
├── scripts/              # No changes needed
│   └── clean_media_path.py
├── tests/                # No changes needed
├── specs/                # Specification files (already use feature numbers)
└── .specify/             # Specification framework (no changes)
```

**Structure Decision**: This is an LLM skill with minimal structure. The repository root contains the SKILL.md file which is the primary target for this rename. Scripts and tests remain unchanged as this is purely a documentation update.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A - No constitution violations. All checks passed.

## Post-Design Constitution Re-evaluation

*Re-check after Phase 1 design artifacts completed*

### Principle I: Single Responsibility ✅ PASS
**Re-assessment**: Design artifacts (data-model.md, quickstart.md) confirm the rename maintains single responsibility. The skill continues to focus solely on TTS audio delivery via WhatsApp. No scope expansion detected.

### Principle II: Format Compatibility (NON-NEGOTIABLE) ✅ PASS
**Re-assessment**: Quickstart guide explicitly preserves the Agent Workflow section unchanged, ensuring OGG/Opus format validation and handling remain intact. Zero risk to format compatibility.

### Principle III: Dependency Transparency ✅ PASS
**Re-assessment**: Data model documents preservation of all dependency references (path-cleaner, tts, message APIs). Quickstart verification steps ensure workflow documentation remains transparent and executable.

**FINAL GATE STATUS**: ✅ ALL CHECKS PASSED - Design maintains constitutional compliance

## Phase Completion Summary

### Phase 0: Research ✅ Complete
- **Output**: `research.md`
- **Key Findings**: 
  - Identified 11 references to old skill name across 5 files
  - Determined SKILL.md as primary update target
  - Defined new description balancing conversation positioning with technical accuracy
  - Established validation approach

### Phase 1: Design & Contracts ✅ Complete
- **Outputs**: 
  - `data-model.md` - SKILL.md structure and field update specifications
  - `quickstart.md` - Step-by-step rename instructions with validation
  - Agent context updated (Windsurf rules file)
- **Contracts**: Not applicable (no external interfaces modified)
- **Key Decisions**:
  - Surgical update approach: modify only identity fields
  - Preserve Agent Workflow section byte-for-byte
  - Atomic commit of all changes

### Phase 2: Task Generation - NOT STARTED
**Note**: Phase 2 (tasks.md generation) is handled by the `/speckit.tasks` command, not `/speckit.plan`.
