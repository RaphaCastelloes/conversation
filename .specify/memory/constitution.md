# WhatsApp Audio Sender Constitution
<!--
Sync Impact Report:
- Version: 1.0.0 (initial constitution)
- Principles defined: 3 core principles for simple LLM skill development
- Templates status: ✅ No dependent templates require updates (new project)
- Follow-up: None
-->

## Core Principles

### I. Single Responsibility
This skill has one clear purpose: convert text to speech and send it via WhatsApp in the correct audio format (OGG/Opus). The skill MUST NOT expand beyond this core function. Any additional messaging features, TTS providers, or communication channels require a separate skill.

**Rationale**: LLM skills are most maintainable and composable when they solve exactly one problem. Clear boundaries prevent scope creep and enable reliable agent orchestration.

### II. Format Compatibility (NON-NEGOTIABLE)
All audio sent to WhatsApp MUST be in OGG format with Opus codec. The skill MUST validate output format before attempting to send. If conversion fails, the skill MUST fail fast with a clear error message rather than attempting to send incompatible formats.

**Rationale**: WhatsApp strictly requires OGG/Opus for audio messages. Silent failures or format mismatches create poor user experience and debugging nightmares.

### III. Dependency Transparency
The skill explicitly declares its dependencies on external skills (`path-cleaner`) and APIs (`tts`, `message`). The SKILL.md documentation MUST maintain up-to-date workflow steps showing exact command sequences and expected outputs.

**Rationale**: LLM agents need clear execution paths. Transparent dependencies enable agents to diagnose failures, verify prerequisites, and compose skills reliably.

## Development Standards

### Code Quality
- All Python scripts MUST include error handling for file I/O and external command execution
- Output paths MUST be validated before use
- Scripts MUST return non-zero exit codes on failure
- Logging SHOULD include timestamps and operation context

### Documentation
- SKILL.md is the single source of truth for agent workflow
- Code examples in documentation MUST be executable and tested
- Breaking changes to workflow require version bump in skill metadata

## Governance

This constitution defines the non-negotiable principles for the WhatsApp Audio Sender skill. Any modifications to core principles (Section I-III) require:

1. Clear justification of why the change improves skill reliability or agent usability
2. Update to SKILL.md with migration notes if workflow changes
3. Version increment following semantic versioning

**Compliance**: All code changes and documentation updates MUST align with the three core principles. Principle II (Format Compatibility) is non-negotiable and cannot be relaxed under any circumstances.

**Version**: 1.0.0 | **Ratified**: 2026-03-09 | **Last Amended**: 2026-03-09
