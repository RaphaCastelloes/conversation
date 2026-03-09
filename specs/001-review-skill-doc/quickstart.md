# Quickstart: SKILL.md Documentation Review Tool

**Feature**: 001-review-skill-doc  
**Last Updated**: 2026-03-09

## What This Tool Does

The SKILL.md review tool validates your skill documentation against:
1. **Path accuracy** - All referenced files exist or are marked as external
2. **Code syntax** - All code examples are syntactically valid
3. **Constitution alignment** - Documentation follows the 3 core principles

## Prerequisites

- Python 3.9 or higher
- No external dependencies (uses Python standard library only)

## Quick Start

### 1. Run the review

```bash
python scripts/review_skill_doc.py
```

This validates `./SKILL.md` against `./.specify/memory/constitution.md` and outputs a markdown report to your terminal.

### 2. Interpret the results

**✅ PASS** - All validations succeeded, documentation is ready  
**⚠️ WARNING** - Minor issues found (e.g., external dependencies)  
**❌ FAIL** - Critical issues found (broken paths, syntax errors, missing constitution alignment)

### 3. Fix issues

The report shows:
- Which paths are broken (with line numbers)
- Which code blocks have syntax errors
- Which constitution principles are not documented

Update SKILL.md based on the recommendations, then re-run the review.

## Common Use Cases

### Generate JSON report for CI/CD

```bash
python scripts/review_skill_doc.py --format json --output review.json
```

Check exit code in your CI pipeline:
```bash
python scripts/review_skill_doc.py && echo "Documentation valid" || exit 1
```

### Review a different SKILL file

```bash
python scripts/review_skill_doc.py --skill-file ./docs/ALTERNATE_SKILL.md
```

### Strict mode (warnings fail the build)

```bash
python scripts/review_skill_doc.py --strict
```

Useful in CI to enforce zero warnings.

### Generate both formats

```bash
python scripts/review_skill_doc.py --format both --output report
# Creates: report.md and report.json
```

## Understanding the Report

### Path Validation Section

```markdown
## Path Validation
✅ **3/5 paths valid**
- ✅ `SKILL.md` (local, exists)
- ⚠️ `/home/opc/.openclaw/...` (external dependency)
- ❌ `./scripts/missing.py` (local, not found)
```

- **✅ Local paths** - Files in your repo that exist
- **⚠️ External paths** - Dependencies outside your repo (expected)
- **❌ Broken paths** - Files that should exist but don't (fix these!)

### Code Syntax Section

```markdown
## Code Syntax Validation
❌ **2/3 code blocks valid**
- ✅ Python block at line 16
- ❌ Python block at line 25: SyntaxError: invalid syntax
- ✅ Bash block at line 32
```

Fix syntax errors in the code examples at the specified line numbers.

### Constitution Alignment Section

```markdown
## Constitution Alignment
✅ **Single Responsibility**: Scope limited to TTS→WhatsApp audio
✅ **Format Compatibility**: OGG/Opus explicitly documented
❌ **Dependency Transparency**: Missing error handling examples
```

Each principle shows PASS/FAIL and what's missing. Add the missing documentation to align with constitution.

## Troubleshooting

### "SKILL.md not found"

Ensure you're running from the repository root, or use `--skill-file` to specify the path:
```bash
python scripts/review_skill_doc.py --skill-file ./path/to/SKILL.md
```

### "Constitution not found"

The tool looks for `./.specify/memory/constitution.md` by default. Specify a different path:
```bash
python scripts/review_skill_doc.py --constitution ./path/to/constitution.md
```

### "Parse error: Invalid YAML frontmatter"

Check that SKILL.md starts with valid YAML frontmatter:
```yaml
---
name: skill-name
description: Description here
---
```

### External paths flagged as warnings

This is expected! External dependencies (like `/home/opc/.openclaw/...`) are not validated because they're outside your repo. The tool flags them so you know they're documented.

## Integration with Development Workflow

### Pre-commit hook

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python scripts/review_skill_doc.py --format json > /dev/null
if [ $? -ne 0 ]; then
  echo "SKILL.md validation failed. Run 'python scripts/review_skill_doc.py' to see issues."
  exit 1
fi
```

### CI/CD pipeline (GitHub Actions example)

```yaml
- name: Validate SKILL.md
  run: |
    python scripts/review_skill_doc.py --format json --output review.json
    cat review.json
```

### Manual review checklist

Before committing SKILL.md changes:
1. ✅ Run `python scripts/review_skill_doc.py`
2. ✅ Fix all ❌ FAIL items
3. ✅ Review ⚠️ WARNING items (external deps are OK)
4. ✅ Verify recommendations are addressed or documented as future work

## Next Steps

- **Fix issues**: Update SKILL.md based on report recommendations
- **Re-run validation**: Ensure all checks pass
- **Commit changes**: Once validation passes, commit your updated SKILL.md
- **Automate**: Add to CI/CD pipeline to prevent documentation drift

## Getting Help

- Review the [CLI Interface Contract](./contracts/cli-interface.md) for detailed command options
- Check the [Data Model](./data-model.md) to understand validation logic
- See the [Feature Specification](./spec.md) for requirements and acceptance criteria
