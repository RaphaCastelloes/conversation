# conversation Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-03-09

## Active Technologies
- Python 3.9+ (for validation tool), Markdown (for documentation) + Python stdlib only (pathlib, re, ast for review_skill_doc.py) (002-remove-mp3-ogg-refs)
- N/A (documentation files only) (002-remove-mp3-ogg-refs)
- Markdown (documentation only) + None (documentation change) (003-rename-skill-conversation)

- Python 3.9+ (for cross-platform compatibility with Windows/Linux) + Standard library (pathlib, re, json), markdown parser (markdown-it-py or mistune) (001-review-skill-doc)

## Project Structure

```text
src/
tests/
```

## Commands

cd src; pytest; ruff check .

## Code Style

Python 3.9+ (for cross-platform compatibility with Windows/Linux): Follow standard conventions

## Recent Changes
- 003-rename-skill-conversation: Added Markdown (documentation only) + None (documentation change)
- 002-remove-mp3-ogg-refs: Added Python 3.9+ (for validation tool), Markdown (for documentation) + Python stdlib only (pathlib, re, ast for review_skill_doc.py)

- 001-review-skill-doc: Added Python 3.9+ (for cross-platform compatibility with Windows/Linux) + Standard library (pathlib, re, json), markdown parser (markdown-it-py or mistune)

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
