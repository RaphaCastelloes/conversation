# Research: Rename Skill to 'Conversation'

**Feature**: 003-rename-skill-conversation  
**Date**: 2026-03-10  
**Status**: Complete

## Overview

This research phase identifies all locations where the skill name "whatsapp-audio-sender" appears and determines the appropriate renaming strategy for each context.

## Research Tasks

### Task 1: Identify All References to Old Skill Name

**Objective**: Locate all instances of "whatsapp-audio-sender" in the repository.

**Findings**:
- **SKILL.md** (1 match): Line 2 - `name: whatsapp-audio-sender` in YAML frontmatter
- **specs/001-review-skill-doc/data-model.md** (1 match): Historical reference in previous spec
- **specs/003-rename-skill-conversation/spec.md** (6 matches): This feature's own specification
- **specs/003-rename-skill-conversation/plan.md** (2 matches): This feature's own plan
- **.windsurf/rules/specify-rules.md** (1 match): Workflow rules file

**Decision**: Update SKILL.md name field. Leave spec files unchanged as they document the rename itself. Review .windsurf/rules/specify-rules.md to determine if update is needed.

**Rationale**: Spec files (003-*) contain the rename feature documentation and should preserve the old name in context. Historical specs (001-*) serve as documentation history and should not be modified retroactively.

### Task 2: Determine New Description Text

**Objective**: Craft a new description that reflects "conversation" capabilities while maintaining accuracy about current functionality.

**Current Description**:
> "Sends text-to-speech (TTS) audio to WhatsApp, ensuring compatibility with OGG (Opus) format. Use to send text-generated audio messages directly to the user's WhatsApp."

**Proposed Description**:
> "Enables conversation with users via WhatsApp by sending text-to-speech (TTS) audio messages in OGG (Opus) format. Use to send text-generated audio messages directly to the user's WhatsApp."

**Decision**: Use proposed description.

**Rationale**: 
- Maintains accuracy about current TTS functionality
- Positions skill as conversation-enabling tool
- Preserves critical format information (OGG/Opus)
- Keeps usage instructions clear
- Aligns with constitution principle of transparency

**Alternatives Considered**:
1. Generic "conversation tool" - Rejected: Too vague, loses technical specifics
2. "Multi-modal conversation" - Rejected: Overpromises capabilities not yet implemented
3. Keep original description - Rejected: Doesn't reflect new skill name

### Task 3: Backward Compatibility Strategy

**Objective**: Ensure external systems referencing "whatsapp-audio-sender" continue to function.

**Findings**:
- LLM skills are typically referenced by their `name` field in SKILL.md
- No evidence of external API contracts or integrations in repository
- Skill appears to be used via agent orchestration, not direct API calls

**Decision**: Document the rename but do not create aliases or compatibility layers.

**Rationale**: 
- Simple documentation change with minimal external impact
- Agent systems will adapt to new name in SKILL.md
- No breaking changes to actual functionality
- If issues arise, can add compatibility note to SKILL.md

**Alternatives Considered**:
1. Create alias/symlink - Rejected: Adds unnecessary complexity for documentation change
2. Maintain both names - Rejected: Violates single source of truth principle

### Task 4: Validation Approach

**Objective**: Define how to verify the rename was successful.

**Decision**: Multi-step validation process:
1. Verify SKILL.md name field updated to "conversation"
2. Verify SKILL.md description reflects conversation positioning
3. Search repository for unintended "whatsapp-audio-sender" references
4. Verify Agent Workflow section remains unchanged
5. Manual review of SKILL.md for consistency

**Rationale**: Systematic validation ensures completeness while preventing over-modification.

## Summary of Decisions

| Decision Point | Choice | Rationale |
|----------------|--------|-----------|
| Primary target | SKILL.md name + description | Core identity file for LLM skill |
| Historical specs | Leave unchanged | Preserve documentation history |
| New description | Conversation-focused with TTS specifics | Balances new positioning with accuracy |
| Backward compatibility | No special handling | Simple rename, low external impact |
| Validation | Multi-step manual verification | Ensures completeness and correctness |

## Unknowns Resolved

All technical context items were clear from the start:
- ✅ Language: Markdown (documentation)
- ✅ Dependencies: None
- ✅ Testing: Manual verification
- ✅ Scope: SKILL.md + documentation review

No research into external technologies or patterns was required for this documentation-focused feature.

## Next Steps

Proceed to Phase 1 to generate:
- **data-model.md**: Document the SKILL.md structure
- **contracts/**: Not applicable (no external interfaces)
- **quickstart.md**: Step-by-step rename instructions
