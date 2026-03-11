---
description: "Task list for renaming skill from 'whatsapp-audio-sender' to 'conversation'"
---

# Tasks: Rename Skill to 'Conversation'

**Input**: Design documents from `/specs/003-rename-skill-conversation/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Not applicable - this is a documentation-only change with manual verification steps.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

This is an LLM skill documentation project with minimal structure:
- **SKILL.md**: Primary skill definition file at repository root
- **specs/**: Feature specification files (no changes needed)
- **scripts/**: Python scripts (no changes needed)

---

## Phase 1: Setup (Preparation)

**Purpose**: Prepare for the rename operation with backup and validation setup

- [ ] T001 Create backup of SKILL.md at repository root as SKILL.md.backup
- [ ] T002 Verify current SKILL.md structure matches data-model.md expectations (YAML frontmatter on lines 1-4, title on line 6, overview on line 8, workflow starts line 10)

---

## Phase 2: User Story 1 - Update Skill Identity (Priority: P1) 🎯 MVP

**Goal**: Rename the skill from "whatsapp-audio-sender" to "conversation" in SKILL.md, updating name, description, title, and overview while preserving the Agent Workflow section.

**Independent Test**: Verify that SKILL.md name field is "conversation", description emphasizes conversation capability, and Agent Workflow section (lines 10-32) remains unchanged.

### Implementation for User Story 1

- [ ] T003 [US1] Update YAML frontmatter name field from "whatsapp-audio-sender" to "conversation" in SKILL.md line 2
- [ ] T004 [US1] Update YAML frontmatter description field to "Enables conversation with users via WhatsApp by sending text-to-speech (TTS) audio messages in OGG (Opus) format. Use to send text-generated audio messages directly to the user's WhatsApp." in SKILL.md line 3
- [ ] T005 [US1] Update H1 title from "WhatsApp Audio Sender" to "Conversation" in SKILL.md line 6
- [ ] T006 [US1] Update overview paragraph to "This skill enables conversation with users by automating the process of sending text-generated audio messages to the user's WhatsApp, ensuring the format is compatible (OGG with Opus codec)." in SKILL.md line 8
- [ ] T007 [US1] Verify Agent Workflow section (lines 10-32) remains completely unchanged by comparing with SKILL.md.backup
- [ ] T008 [US1] Validate YAML frontmatter syntax is correct (3 dashes on lines 1 and 4, proper YAML structure)
- [ ] T009 [US1] Run validation: verify "name: conversation" exists in SKILL.md using grep/Select-String
- [ ] T010 [US1] Run validation: verify "whatsapp-audio-sender" does NOT exist in SKILL.md name field using grep/Select-String
- [ ] T011 [US1] Run validation: verify description contains "Enables conversation with users via WhatsApp" using grep/Select-String
- [ ] T012 [US1] Run validation: verify "## Agent Workflow" section still exists on line 10 using grep/Select-String
- [ ] T013 [US1] Perform visual review of complete SKILL.md file for consistency and formatting

**Checkpoint**: At this point, User Story 1 should be complete - SKILL.md has new identity while preserving all functional documentation.

---

## Phase 3: User Story 2 - Update Repository References (Priority: P2)

**Goal**: Review and update any repository-level references to the old skill name for consistency.

**Independent Test**: Search repository for "whatsapp-audio-sender" references and verify only expected historical references remain (in specs/ directories documenting the rename itself).

### Implementation for User Story 2

- [ ] T014 [US2] Search repository for all "whatsapp-audio-sender" references excluding specs/ directory using grep/Select-String
- [ ] T015 [US2] Review .windsurf/rules/specify-rules.md for references to old skill name and determine if update needed
- [ ] T016 [US2] If .windsurf/rules/specify-rules.md needs update, modify references from "whatsapp-audio-sender" to "conversation" in .windsurf/rules/specify-rules.md
- [ ] T017 [US2] Verify no unintended references to old skill name remain outside of specs/ directory
- [ ] T018 [US2] Document any external systems or integrations that may reference old skill name (create note in specs/003-rename-skill-conversation/external-references.md if needed)

**Checkpoint**: At this point, User Story 2 should be complete - all repository references updated appropriately.

---

## Phase 4: Polish & Finalization

**Purpose**: Commit changes and cleanup

- [ ] T019 Stage SKILL.md changes using git add
- [ ] T020 Stage any other modified files (e.g., .windsurf/rules/specify-rules.md if updated) using git add
- [ ] T021 Commit changes with message: "Rename skill from 'whatsapp-audio-sender' to 'conversation'\n\n- Update name field in YAML frontmatter\n- Update description to emphasize conversation capability\n- Update title and overview paragraph\n- Preserve Agent Workflow section unchanged\n\nRefs: 003-rename-skill-conversation"
- [ ] T022 Push changes to remote branch 003-rename-skill-conversation
- [ ] T023 Remove backup file SKILL.md.backup from repository root
- [ ] T024 Run final validation: search for "whatsapp-audio-sender" in repository (excluding specs/) to confirm no unintended references remain
- [ ] T025 Run quickstart.md verification steps to confirm all success criteria met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **User Story 1 (Phase 2)**: Depends on Setup completion - CRITICAL for feature success
- **User Story 2 (Phase 3)**: Can start after User Story 1 completion - Independent but recommended after US1
- **Polish (Phase 4)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Setup (Phase 1) - No dependencies on other stories - **This is the MVP**
- **User Story 2 (P2)**: Can start after User Story 1 - Independently testable but logically follows US1

### Within Each User Story

**User Story 1 (Update Skill Identity)**:
- T003-T006: Core file edits (must be done in order to maintain file integrity)
- T007-T013: Validation tasks (can run after edits complete)

**User Story 2 (Update Repository References)**:
- T014: Search task (must run first to identify what needs updating)
- T015-T016: Review and update tasks (sequential, depends on T014 findings)
- T017-T018: Final verification (runs after updates)

### Parallel Opportunities

Limited parallel opportunities due to documentation-focused nature:
- T009, T010, T011, T012 (validation commands) can run in parallel after T008 completes
- T015 and T017 can run in parallel (different files)

---

## Parallel Example: User Story 1 Validation

```bash
# After completing T003-T008, launch all validation tasks together:
Task: "Run validation: verify 'name: conversation' exists in SKILL.md"
Task: "Run validation: verify 'whatsapp-audio-sender' does NOT exist in name field"
Task: "Run validation: verify description contains 'Enables conversation with users'"
Task: "Run validation: verify '## Agent Workflow' section still exists"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (backup and verify structure)
2. Complete Phase 2: User Story 1 (rename skill identity in SKILL.md)
3. **STOP and VALIDATE**: Run all validation tasks (T007-T013)
4. If validation passes, commit and push
5. **MVP COMPLETE**: Skill is renamed and functional

### Incremental Delivery

1. Complete Setup → Backup created, ready to proceed
2. Complete User Story 1 → Test independently → **MVP ready to deploy**
3. Complete User Story 2 → Test independently → Full consistency achieved
4. Complete Polish → Changes committed and finalized

### Single Developer Strategy

This is a straightforward sequential workflow:

1. Run Setup tasks (T001-T002)
2. Execute User Story 1 tasks in order (T003-T013)
3. Validate User Story 1 success independently
4. Execute User Story 2 tasks in order (T014-T018)
5. Validate User Story 2 success independently
6. Run Polish tasks (T019-T025)
7. Feature complete

**Estimated Total Time**: 10-15 minutes for all phases

---

## Notes

- This is a documentation-only change - no code modifications required
- Agent Workflow section (lines 10-32 of SKILL.md) is **CRITICAL** and must remain unchanged
- YAML frontmatter syntax errors will break skill parsing - validate carefully
- Historical spec files (specs/001-*, specs/003-*) should NOT be modified
- Each user story delivers independent value and can be tested separately
- User Story 1 alone constitutes a complete MVP
- Commit after completing each user story for clean git history
- If any validation fails, restore from SKILL.md.backup and retry
