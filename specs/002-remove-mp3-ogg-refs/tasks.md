# Tasks: Remove MP3-to-OGG Conversion References

**Input**: Design documents from `/specs/002-remove-mp3-ogg-refs/`
**Prerequisites**: plan.md (tech stack), spec.md (user stories), research.md (decisions), data-model.md (entities), quickstart.md

**Tests**: Tests are NOT requested in the feature specification - implementation only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Documentation update**: SKILL.md, scripts/review_skill_doc.py, .specify/memory/constitution.md at repository root
- Paths assume existing file structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify prerequisites and backup current state

- [ ] T001 Verify SKILL.md exists and contains mp3-to-ogg references to be removed
- [ ] T002 Verify scripts/review_skill_doc.py exists and is functional
- [ ] T003 [P] Create backup of SKILL.md before modifications (optional safety measure)

---

## Phase 2: User Story 1 - Update SKILL.md Documentation (Priority: P1) 🎯 MVP

**Goal**: Update SKILL.md to remove all mp3-to-ogg references and simplify workflow from 3 steps to 2 steps

**Independent Test**: Review updated SKILL.md and verify: (1) zero references to mp3-to-ogg, (2) workflow shows 2 steps, (3) code examples show TTS outputting OGG directly

### Implementation for User Story 1

- [ ] T004 [US1] Update SKILL.md frontmatter description to clarify TTS outputs OGG directly (if needed)
- [ ] T005 [US1] Update SKILL.md Step 1 title from "Generate TTS audio (MP3)" to "Generate TTS audio (OGG)" in SKILL.md
- [ ] T006 [US1] Update SKILL.md Step 1 Python code example to change variable from mp3_path to ogg_path in SKILL.md
- [ ] T007 [US1] Update SKILL.md Step 1 to add clarification that TTS outputs OGG (Opus) format directly in SKILL.md
- [ ] T008 [US1] Remove entire Step 2 section (MP3 to OGG conversion) including bash code block from SKILL.md
- [ ] T009 [US1] Renumber old Step 3 to new Step 2 in SKILL.md
- [ ] T010 [US1] Update new Step 2 title to "Send the OGG audio to WhatsApp" in SKILL.md
- [ ] T011 [US1] Add path-cleaner usage to new Step 2 Python code example in SKILL.md
- [ ] T012 [US1] Update variable names from clean_mp3_path to clean_ogg_path in new Step 2 in SKILL.md
- [ ] T013 [US1] Update final summary paragraph to mention TTS outputs OGG directly in SKILL.md
- [ ] T014 [US1] Verify SKILL.md contains exactly 2 workflow steps (not 3)
- [ ] T015 [US1] Search SKILL.md for any remaining "mp3-to-ogg" or "convert_mp3_to_ogg.py" references and remove them

**Checkpoint**: At this point, User Story 1 should be complete - SKILL.md has 2-step workflow with no mp3-to-ogg references

---

## Phase 3: User Story 2 - Update Constitution Validation (Priority: P2)

**Goal**: Update the constitution validation tool and constitution document to remove mp3-to-ogg from required dependencies

**Independent Test**: Run `python scripts/review_skill_doc.py` and verify constitution alignment shows PASS without requiring mp3-to-ogg keywords

### Implementation for User Story 2

- [ ] T016 [US2] Locate load_constitution_principles() function in scripts/review_skill_doc.py (around line 485)
- [ ] T017 [US2] Update Dependency Transparency principle's required_keywords list in scripts/review_skill_doc.py
- [ ] T018 [US2] Change required_keywords from ["mp3-to-ogg", "path-cleaner", "tts", "message"] to ["path-cleaner", "tts", "message"] in scripts/review_skill_doc.py
- [ ] T019 [US2] Update .specify/memory/constitution.md line 23 to remove mp3-to-ogg from dependency list
- [ ] T020 [US2] Change constitution.md text from "(`mp3-to-ogg`, `path-cleaner`)" to "(`path-cleaner`)" in Principle III
- [ ] T021 [US2] Run python scripts/review_skill_doc.py to validate SKILL.md passes constitution checks
- [ ] T022 [US2] Verify constitution alignment output shows PASS for Dependency Transparency without mp3-to-ogg

**Checkpoint**: At this point, User Story 2 should be complete - validation tool and constitution updated, SKILL.md passes validation

---

## Phase 4: Polish & Validation

**Purpose**: Final verification and optional test fixture updates

- [ ] T023 [P] Run python scripts/review_skill_doc.py and confirm exit code 0 (PASS or WARNING)
- [ ] T024 [P] Verify SKILL.md workflow is clear and executable for AI agents
- [ ] T025 Update tests/fixtures/valid_skill.md to remove mp3-to-ogg references (optional - matches new structure)
- [ ] T026 Run python scripts/review_skill_doc.py --skill-file tests/fixtures/valid_skill.md to verify fixture passes (if T025 completed)
- [ ] T027 Review all changes against success criteria (SC-001 through SC-005 from spec.md)
- [ ] T028 Verify path-cleaner is still documented as required dependency in SKILL.md
- [ ] T029 Confirm no breaking changes to existing workflow execution (backward compatibility check)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **User Story 1 (Phase 2)**: Depends on Setup completion - This is the MVP
- **User Story 2 (Phase 3)**: Can start after Setup - Independent of US1 (different files)
- **Polish (Phase 4)**: Depends on both US1 and US2 completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Setup - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Setup - Independent of US1 (modifies different files)

### Parallel Opportunities

**After Setup completes, User Stories 1 and 2 can run in parallel**:
- US1 modifies: SKILL.md
- US2 modifies: scripts/review_skill_doc.py and .specify/memory/constitution.md
- No file conflicts - completely independent

### Within Each User Story

- **US1 Tasks**: Must run sequentially (all modify SKILL.md)
- **US2 Tasks**: Must run sequentially (modify validation tool and constitution)
- **Polish Tasks**: T023 and T024 can run in parallel (different validation aspects)

---

## Parallel Example: After Setup Complete

```bash
# Launch both user stories together (different files):
Task T004-T015: "User Story 1 - Update SKILL.md"
Task T016-T022: "User Story 2 - Update Constitution Validation"
```

These can be implemented by different developers or in parallel sessions since they modify different files.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: User Story 1 (T004-T015)
3. **STOP and VALIDATE**: Review SKILL.md manually
4. **This is a functional MVP!** - Documentation is updated and accurate

### Incremental Delivery

1. Complete Setup → Prerequisites verified
2. Add User Story 1 → Test independently → **MVP: SKILL.md updated**
3. Add User Story 2 → Test independently → **V1.1: Validation tool updated**
4. Add Polish → **V1.2: Fully validated and tested**

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup together (T001-T003)
2. Once Setup is done:
   - Developer A: User Story 1 (T004-T015) - Updates SKILL.md
   - Developer B: User Story 2 (T016-T022) - Updates validation tool and constitution
3. Both stories complete and integrate independently
4. Team runs Polish tasks together (T023-T029)

---

## Task Summary

- **Total Tasks**: 29
- **Setup**: 3 tasks
- **User Story 1 (P1)**: 12 tasks - SKILL.md documentation update
- **User Story 2 (P2)**: 7 tasks - Constitution validation update
- **Polish**: 7 tasks

**Parallel Opportunities**: User Stories 1 and 2 can run completely in parallel after Setup (different files, no conflicts)

**Suggested MVP Scope**: Phase 1 + Phase 2 (User Story 1) = 15 tasks → Updated SKILL.md with simplified workflow

---

## Success Criteria Validation

After completing all tasks, verify against spec.md success criteria:

- **SC-001**: SKILL.md contains zero references to "mp3-to-ogg" or "convert_mp3_to_ogg.py" → Validated by T014, T015
- **SC-002**: Workflow section describes exactly 2 steps instead of 3 → Validated by T008, T009, T014
- **SC-003**: Running `python scripts/review_skill_doc.py` shows constitution alignment PASS status → Validated by T021, T022, T023
- **SC-004**: Code examples in SKILL.md execute successfully without calling mp3-to-ogg conversion → Validated by T006, T008, T011
- **SC-005**: Documentation clearly states that TTS outputs OGG format compatible with WhatsApp → Validated by T007, T013

---

## Notes

- This is a documentation-only change - no code execution required
- All tasks modify existing files (no new files created)
- Changes are low-risk and easily reversible (T003 creates backup)
- Total implementation time: ~10-15 minutes for all tasks
- Each user story is independently testable and deliverable
- No external dependencies or API changes required
- Backward compatibility maintained (old workflows still functional, just not documented)
