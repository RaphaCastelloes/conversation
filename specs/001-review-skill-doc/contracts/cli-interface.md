# CLI Interface Contract: review_skill_doc.py

**Feature**: 001-review-skill-doc  
**Date**: 2026-03-09  
**Purpose**: Define the command-line interface contract for the SKILL.md validation tool

## Command Signature

```bash
python scripts/review_skill_doc.py [OPTIONS]
```

## Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--skill-file` | `-s` | Path | `./SKILL.md` | Path to SKILL.md file to review |
| `--constitution` | `-c` | Path | `./.specify/memory/constitution.md` | Path to constitution file |
| `--format` | `-f` | Enum | `markdown` | Output format: `json`, `markdown`, or `both` |
| `--output` | `-o` | Path | stdout | Output file path (stdout if not specified) |
| `--strict` | | Flag | False | Fail on warnings (exit code 1) |
| `--help` | `-h` | Flag | | Show help message |

## Exit Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 0 | Success | All validations passed |
| 1 | Validation Failed | One or more validation checks failed |
| 2 | File Not Found | SKILL.md or constitution.md not found |
| 3 | Parse Error | Failed to parse SKILL.md or constitution.md |
| 4 | Invalid Arguments | Invalid command-line arguments provided |

## Standard Output (Markdown Format)

```markdown
# SKILL.md Review Report

**Generated**: 2026-03-09 19:53:00  
**File**: ./SKILL.md  
**Status**: ✅ PASS | ❌ FAIL | ⚠️ WARNING

## Summary
- Total Checks: 10
- Passed: 8
- Failed: 2
- Warnings: 3

## Path Validation
✅ **3/5 paths valid**
- ✅ `SKILL.md` (local, exists)
- ⚠️ `/home/opc/.openclaw/...` (external dependency)
- ❌ `./scripts/missing.py` (local, not found)

## Code Syntax Validation
✅ **All code blocks valid (3/3)**
- ✅ Python block at line 16
- ✅ Bash block at line 22
- ✅ Python block at line 32

## Constitution Alignment
✅ **Single Responsibility**: Scope limited to TTS→WhatsApp audio
✅ **Format Compatibility**: OGG/Opus explicitly documented
❌ **Dependency Transparency**: Missing error handling examples

## Recommendations
1. Add error handling examples for failed conversions
2. Document expected output format for success verification
3. Add troubleshooting section for common issues
```

## Standard Output (JSON Format)

```json
{
  "metadata": {
    "generated": "2026-03-09T19:53:00Z",
    "file": "./SKILL.md",
    "constitution": "./.specify/memory/constitution.md",
    "version": "1.0.0"
  },
  "summary": {
    "total_checks": 10,
    "passed": 8,
    "failed": 2,
    "warnings": 3,
    "status": "FAIL"
  },
  "path_validation": {
    "total": 5,
    "valid": 3,
    "external": 1,
    "broken": 1,
    "results": [
      {
        "path": "SKILL.md",
        "type": "local",
        "exists": true,
        "status": "VALID",
        "line": 1
      },
      {
        "path": "/home/opc/.openclaw/workspace/skills/mp3-to-ogg/scripts/convert_mp3_to_ogg.py",
        "type": "external",
        "exists": null,
        "status": "EXTERNAL",
        "line": 27,
        "note": "External dependency - not validated"
      },
      {
        "path": "./scripts/missing.py",
        "type": "local",
        "exists": false,
        "status": "BROKEN",
        "line": 15
      }
    ]
  },
  "code_validation": {
    "total": 3,
    "valid": 3,
    "errors": 0,
    "results": [
      {
        "language": "python",
        "line": 16,
        "status": "VALID",
        "errors": []
      },
      {
        "language": "bash",
        "line": 22,
        "status": "VALID",
        "errors": []
      }
    ]
  },
  "constitution_alignment": {
    "principles": [
      {
        "name": "Single Responsibility",
        "status": "PASS",
        "found_keywords": ["TTS", "WhatsApp", "audio"],
        "missing_keywords": [],
        "details": "Scope limited to TTS→WhatsApp audio sending"
      },
      {
        "name": "Format Compatibility",
        "status": "PASS",
        "found_keywords": ["OGG", "Opus", "convert"],
        "missing_keywords": [],
        "details": "OGG/Opus format explicitly documented in workflow"
      },
      {
        "name": "Dependency Transparency",
        "status": "FAIL",
        "found_keywords": ["mp3-to-ogg", "path-cleaner", "tts", "message"],
        "missing_keywords": ["error handling"],
        "details": "Dependencies documented but missing error handling examples"
      }
    ]
  },
  "recommendations": [
    "Add error handling examples for failed conversions",
    "Document expected output format for success verification",
    "Add troubleshooting section for common issues"
  ],
  "exit_code": 1
}
```

## Standard Error

Errors and warnings are written to stderr:

```
ERROR: SKILL.md not found at ./SKILL.md
WARNING: External dependency path not validated: /home/opc/.openclaw/...
ERROR: Local path not found: ./scripts/missing.py (line 15)
```

## Usage Examples

### Basic usage (default markdown output to stdout)
```bash
python scripts/review_skill_doc.py
```

### JSON output to file
```bash
python scripts/review_skill_doc.py --format json --output review-report.json
```

### Custom paths
```bash
python scripts/review_skill_doc.py \
  --skill-file ./docs/SKILL.md \
  --constitution ./config/constitution.md
```

### Strict mode (warnings treated as failures)
```bash
python scripts/review_skill_doc.py --strict
```

### Both formats
```bash
python scripts/review_skill_doc.py --format both --output review-report
# Generates: review-report.md and review-report.json
```

## Validation Behavior

### Path Validation
- **Local paths** (relative or absolute within repo): MUST exist, else FAIL
- **External paths** (absolute outside repo): Flagged as WARNING (external dependency)
- **Placeholder paths** (containing `<...>`): Ignored (example code)

### Code Validation
- **Python blocks**: Parsed with `ast.parse()`, syntax errors cause FAIL
- **Bash blocks**: Basic checks (unmatched quotes, unclosed expansions), errors cause FAIL
- **Unmarked blocks**: Skipped (no language specified)

### Constitution Validation
- **Single Responsibility**: Check frontmatter description for scope keywords
- **Format Compatibility**: Search workflow for "OGG", "Opus", "convert"
- **Dependency Transparency**: Verify all dependencies documented with examples

## Error Handling

| Error Scenario | Behavior | Exit Code |
|----------------|----------|-----------|
| SKILL.md not found | Print error to stderr, exit | 2 |
| Constitution not found | Print error to stderr, exit | 2 |
| Invalid markdown syntax | Print parse error, exit | 3 |
| Invalid YAML frontmatter | Print parse error, exit | 3 |
| Invalid --format value | Print usage help, exit | 4 |
| Output file write fails | Print error to stderr, exit | 1 |

## Backward Compatibility

This is the initial version (1.0.0). Future versions will maintain:
- Exit code semantics (0=success, non-zero=failure)
- JSON schema structure (new fields may be added, existing fields preserved)
- Command-line options (new options may be added, existing options preserved)

## Performance Contract

- **Execution time**: < 5 seconds for SKILL.md files up to 500 lines
- **Memory usage**: < 50MB for typical SKILL.md files
- **No external network calls**: Fully offline operation
