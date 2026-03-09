# Tasks: SKILL.md Documentation Review

**Input**: Design documents from `/specs/001-review-skill-doc/`
**Prerequisites**: plan.md (tech stack), spec.md (user stories), research.md (decisions), data-model.md (entities), contracts/cli-interface.md

**Tests**: Tests are NOT requested in the feature specification - implementation only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `scripts/`, `tests/` at repository root
- Paths assume simple CLI tool structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create scripts/ directory for main validation script
- [ ] T002 Create tests/ directory structure with fixtures/ subdirectory
- [ ] T003 [P] Create tests/fixtures/ directory for test SKILL.md samples

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data structures and parsing infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Implement SkillDocument class with frontmatter, sections, code_blocks, file_paths attributes in scripts/review_skill_doc.py
- [ ] T005 [P] Implement DocumentSection class with heading, level, content, line_number in scripts/review_skill_doc.py
- [ ] T006 [P] Implement CodeBlock class with language, content, line_number, syntax_valid, syntax_errors in scripts/review_skill_doc.py
- [ ] T007 [P] Implement FilePath class with path_string, path_type, exists, line_number, context in scripts/review_skill_doc.py
- [ ] T008 Implement YAML frontmatter parser using re module in scripts/review_skill_doc.py
- [ ] T009 Implement markdown section extractor using re patterns in scripts/review_skill_doc.py
- [ ] T010 Implement code block extractor with language detection in scripts/review_skill_doc.py
- [ ] T011 Implement file path extractor with regex for Unix/Windows paths in scripts/review_skill_doc.py
- [ ] T012 Implement CLI argument parser with argparse (--skill-file, --constitution, --format, --output, --strict) in scripts/review_skill_doc.py
- [ ] T013 Implement error handling for file not found (exit code 2) in scripts/review_skill_doc.py
- [ ] T014 Implement error handling for parse errors (exit code 3) in scripts/review_skill_doc.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Documentation Accuracy Validation (Priority: P1) 🎯 MVP

**Goal**: Validate that all file paths exist or are marked as external, and all code examples are syntactically correct

**Independent Test**: Run the tool on SKILL.md and verify it reports path validation status and code syntax validation status

### Implementation for User Story 1

- [ ] T015 [P] [US1] Implement PathValidationResult class with file_path, status, message in scripts/review_skill_doc.py
- [ ] T016 [P] [US1] Implement CodeValidationResult class with code_block, status, errors in scripts/review_skill_doc.py
- [ ] T017 [US1] Implement path type detection (local/external/placeholder) logic in scripts/review_skill_doc.py
- [ ] T018 [US1] Implement local path existence check using pathlib.Path.exists() in scripts/review_skill_doc.py
- [ ] T019 [US1] Implement external path detection (absolute path outside repo) in scripts/review_skill_doc.py
- [ ] T020 [US1] Implement placeholder path detection (contains <...>) in scripts/review_skill_doc.py
- [ ] T021 [US1] Implement Python code syntax validation using ast.parse() in scripts/review_skill_doc.py
- [ ] T022 [US1] Implement bash code basic validation (unmatched quotes, unclosed expansions) in scripts/review_skill_doc.py
- [ ] T023 [US1] Implement validate_paths() function that processes all FilePath objects in scripts/review_skill_doc.py
- [ ] T024 [US1] Implement validate_code() function that processes all CodeBlock objects in scripts/review_skill_doc.py
- [ ] T025 [US1] Create test fixture tests/fixtures/valid_skill.md with correct paths and syntax
- [ ] T026 [US1] Create test fixture tests/fixtures/invalid_paths.md with broken local paths
- [ ] T027 [US1] Add path validation results to report generation logic in scripts/review_skill_doc.py
- [ ] T028 [US1] Add code validation results to report generation logic in scripts/review_skill_doc.py

**Checkpoint**: At this point, User Story 1 should be fully functional - tool validates paths and code syntax

---

## Phase 4: User Story 2 - Constitution Alignment Check (Priority: P2)

**Goal**: Ensure SKILL.md aligns with the three constitution principles (Single Responsibility, Format Compatibility, Dependency Transparency)

**Independent Test**: Run the tool on SKILL.md and verify it checks all three constitution principles with keyword matching

### Implementation for User Story 2

- [ ] T029 [P] [US2] Implement ConstitutionPrinciple class with name, required_keywords, validation_result, found_keywords, missing_keywords in scripts/review_skill_doc.py
- [ ] T030 [P] [US2] Implement ConstitutionValidationResult class with principle, status, details in scripts/review_skill_doc.py
- [ ] T031 [US2] Implement constitution.md file parser to load principles in scripts/review_skill_doc.py
- [ ] T032 [US2] Implement Single Responsibility check (frontmatter description scope validation) in scripts/review_skill_doc.py
- [ ] T033 [US2] Implement Format Compatibility check (search for OGG, Opus, convert keywords) in scripts/review_skill_doc.py
- [ ] T034 [US2] Implement Dependency Transparency check (verify mp3-to-ogg, path-cleaner, tts, message documented) in scripts/review_skill_doc.py
- [ ] T035 [US2] Implement validate_constitution() function that checks all three principles in scripts/review_skill_doc.py
- [ ] T036 [US2] Create test fixture tests/fixtures/missing_principles.md with missing constitution alignment
- [ ] T037 [US2] Add constitution validation results to report generation logic in scripts/review_skill_doc.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - tool validates paths, code, and constitution

---

## Phase 5: User Story 3 - Completeness and Clarity Assessment (Priority: P3)

**Goal**: Assess whether SKILL.md provides complete information about prerequisites, error handling, and expected outputs

**Independent Test**: Run the tool and verify it generates recommendations for missing prerequisites, error handling, and output documentation

### Implementation for User Story 3

- [ ] T038 [US3] Implement check for prerequisites section presence in SKILL.md in scripts/review_skill_doc.py
- [ ] T039 [US3] Implement check for error handling examples in workflow in scripts/review_skill_doc.py
- [ ] T040 [US3] Implement check for expected output documentation in scripts/review_skill_doc.py
- [ ] T041 [US3] Implement recommendation generation logic based on missing sections in scripts/review_skill_doc.py
- [ ] T042 [US3] Add completeness checks to validation workflow in scripts/review_skill_doc.py
- [ ] T043 [US3] Add recommendations to report output (both JSON and Markdown) in scripts/review_skill_doc.py

**Checkpoint**: All user stories should now be independently functional - full validation coverage

---

## Phase 6: Report Generation & Output

**Purpose**: Generate structured reports in JSON and Markdown formats

- [ ] T044 [P] Implement ValidationReport class with timestamp, skill_doc, summary, path_results, code_results, constitution_results, recommendations, exit_code in scripts/review_skill_doc.py
- [ ] T045 [P] Implement ReportSummary class with total_checks, passed, failed, warnings, overall_status in scripts/review_skill_doc.py
- [ ] T046 Implement JSON report formatter with schema per CLI contract in scripts/review_skill_doc.py
- [ ] T047 Implement Markdown report formatter with sections per CLI contract in scripts/review_skill_doc.py
- [ ] T048 Implement output file writer with format detection (json/markdown/both) in scripts/review_skill_doc.py
- [ ] T049 Implement stdout output for default case in scripts/review_skill_doc.py
- [ ] T050 Implement stderr output for errors and warnings in scripts/review_skill_doc.py
- [ ] T051 Implement exit code logic (0=pass, 1=fail, 2=file not found, 3=parse error, 4=invalid args) in scripts/review_skill_doc.py
- [ ] T052 Implement --strict mode that treats warnings as failures in scripts/review_skill_doc.py

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T053 [P] Add docstrings to all classes and functions in scripts/review_skill_doc.py
- [ ] T054 [P] Add inline comments for complex regex patterns in scripts/review_skill_doc.py
- [ ] T055 Add help text with usage examples to argparse in scripts/review_skill_doc.py
- [ ] T056 Test tool on actual SKILL.md in repository root
- [ ] T057 Fix any issues found during real SKILL.md validation
- [ ] T058 Verify all exit codes work correctly with test cases
- [ ] T059 Verify cross-platform path handling (Windows/Linux) works correctly
- [ ] T060 Run tool with --format both to verify dual output generation
- [ ] T061 Validate JSON output schema matches CLI contract specification
- [ ] T062 Validate Markdown output format matches CLI contract specification
- [ ] T063 Update quickstart.md with actual tool execution results if needed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Report Generation (Phase 6)**: Depends on at least US1 completion (can start after US1)
- **Polish (Phase 7)**: Depends on all user stories and report generation being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 (different validation logic)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2 (different validation logic)

### Within Each User Story

- Data classes before validation logic
- Validation functions before report integration
- Test fixtures alongside implementation
- Report integration after validation logic complete

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003)
- All Foundational data classes marked [P] can run in parallel (T005, T006, T007)
- Once Foundational phase completes, all user stories can start in parallel (US1, US2, US3 are independent)
- Within US1: PathValidationResult and CodeValidationResult classes can be built in parallel (T015, T016)
- Within US2: ConstitutionPrinciple and ConstitutionValidationResult classes can be built in parallel (T029, T030)
- Report generation classes can be built in parallel (T044, T045)
- Documentation tasks can run in parallel (T053, T054)

---

## Parallel Example: Foundational Phase

```bash
# Launch all data class implementations together:
Task T005: "Implement DocumentSection class"
Task T006: "Implement CodeBlock class"
Task T007: "Implement FilePath class"
```

## Parallel Example: User Story 1

```bash
# Launch both result classes together:
Task T015: "Implement PathValidationResult class"
Task T016: "Implement CodeValidationResult class"
```

## Parallel Example: After Foundation Complete

```bash
# Launch all user stories together (different validation domains):
Task T015-T028: "User Story 1 - Path and Code Validation"
Task T029-T037: "User Story 2 - Constitution Alignment"
Task T038-T043: "User Story 3 - Completeness Assessment"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T014) - CRITICAL
3. Complete Phase 3: User Story 1 (T015-T028)
4. Complete Phase 6: Basic Report Generation (T044-T051)
5. **STOP and VALIDATE**: Test on actual SKILL.md
6. Deploy/demo if ready - **This is a functional MVP!**

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 + Basic Reports → Test independently → **MVP: Path & Code Validation**
3. Add User Story 2 → Test independently → **V1.1: Constitution Alignment**
4. Add User Story 3 → Test independently → **V1.2: Completeness Assessment**
5. Add Polish → **V1.3: Production Ready**

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T014)
2. Once Foundational is done:
   - Developer A: User Story 1 (T015-T028)
   - Developer B: User Story 2 (T029-T037)
   - Developer C: User Story 3 (T038-T043)
3. One developer: Report Generation (T044-T052) - can start after US1
4. Stories complete and integrate independently

---

## Task Summary

- **Total Tasks**: 63
- **Setup**: 3 tasks
- **Foundational**: 11 tasks (BLOCKS all stories)
- **User Story 1 (P1)**: 14 tasks - Path & Code Validation
- **User Story 2 (P2)**: 9 tasks - Constitution Alignment
- **User Story 3 (P3)**: 6 tasks - Completeness Assessment
- **Report Generation**: 9 tasks
- **Polish**: 11 tasks

**Parallel Opportunities**: 15 tasks marked [P] can run in parallel with others

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1) + Phase 6 (Basic Reports) = 37 tasks

---

## Notes

- [P] tasks = different files or independent logic, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- All code in single file (scripts/review_skill_doc.py) per plan.md simplicity principle
- No external dependencies except Python stdlib (pathlib, re, json, yaml, ast, argparse)
- Commit after each logical group of tasks
- Stop at any checkpoint to validate story independently
- Tool should work on actual SKILL.md in repo root as final validation
