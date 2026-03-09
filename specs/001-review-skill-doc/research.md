# Research: SKILL.md Documentation Review Tool

**Feature**: 001-review-skill-doc  
**Date**: 2026-03-09  
**Purpose**: Resolve technical unknowns and establish best practices for implementing the documentation validation tool

## Research Questions

### Q1: Markdown Parsing Library Selection

**Decision**: Use Python's standard library `re` module with minimal external dependencies

**Rationale**: 
- The SKILL.md structure is simple (YAML frontmatter + markdown sections)
- We only need to extract code blocks, file paths, and section headings
- Avoiding heavy dependencies (markdown-it-py, mistune) aligns with constitution's simplicity principle
- Standard library regex is sufficient for our validation needs (code blocks, paths, frontmatter)

**Alternatives Considered**:
- **markdown-it-py**: Full-featured parser, but overkill for simple validation tasks
- **mistune**: Lightweight but still adds external dependency
- **CommonMark**: Spec-compliant but unnecessary complexity

**Implementation Approach**:
```python
import re
import yaml

# Extract YAML frontmatter
frontmatter_pattern = r'^---\n(.*?)\n---'

# Extract code blocks with language
code_block_pattern = r'```(\w+)?\n(.*?)```'

# Extract file paths (Linux/Windows)
path_pattern = r'(?:/[\w\-./]+|[A-Z]:\\[\w\-\\./]+)'
```

---

### Q2: Path Validation Strategy

**Decision**: Implement tiered validation with clear external dependency marking

**Rationale**:
- Some paths in SKILL.md are external (e.g., `/home/opc/.openclaw/...`)
- Need to distinguish between "should exist locally" vs "external dependency"
- Cross-platform support requires handling both Unix and Windows paths

**Validation Tiers**:
1. **Local paths** (relative to repo root): Must exist, validation fails if missing
2. **External paths** (absolute paths outside repo): Flagged as external dependencies in report
3. **Placeholder paths** (containing `<...>`): Marked as examples, no validation

**Implementation**:
```python
from pathlib import Path

def validate_path(path_str, repo_root):
    path = Path(path_str)
    
    # Check if it's a placeholder
    if '<' in path_str and '>' in path_str:
        return {'type': 'placeholder', 'valid': True}
    
    # Check if it's external (absolute path outside repo)
    if path.is_absolute():
        if not str(path).startswith(str(repo_root)):
            return {'type': 'external', 'valid': True, 'note': 'External dependency'}
        # Absolute path inside repo
        return {'type': 'local', 'valid': path.exists()}
    
    # Relative path - check against repo root
    full_path = repo_root / path
    return {'type': 'local', 'valid': full_path.exists()}
```

---

### Q3: Code Syntax Validation Approach

**Decision**: Use `ast.parse()` for Python, regex patterns for bash/shell

**Rationale**:
- Python has built-in AST parser - no external dependencies
- Bash syntax validation is complex; focus on common errors (unmatched quotes, invalid variable syntax)
- Goal is to catch obvious syntax errors, not full language validation

**Python Validation**:
```python
import ast

def validate_python_code(code_str):
    try:
        ast.parse(code_str)
        return {'valid': True}
    except SyntaxError as e:
        return {'valid': False, 'error': str(e), 'line': e.lineno}
```

**Bash Validation** (basic checks):
```python
def validate_bash_code(code_str):
    errors = []
    
    # Check for unmatched quotes
    if code_str.count('"') % 2 != 0:
        errors.append("Unmatched double quotes")
    if code_str.count("'") % 2 != 0:
        errors.append("Unmatched single quotes")
    
    # Check for common syntax issues
    if re.search(r'\$\{[^}]*$', code_str):
        errors.append("Unclosed variable expansion")
    
    return {'valid': len(errors) == 0, 'errors': errors}
```

---

### Q4: Constitution Alignment Validation

**Decision**: Keyword-based section matching with manual review flags

**Rationale**:
- Constitution principles are well-defined (Single Responsibility, Format Compatibility, Dependency Transparency)
- Can validate presence of key terms and sections
- Some alignment checks require semantic understanding - flag for manual review

**Validation Checks**:

| Principle | Validation Method | Success Criteria |
|-----------|------------------|------------------|
| Single Responsibility | Check description field in frontmatter | Must mention "TTS", "WhatsApp", "audio"; must NOT mention unrelated features |
| Format Compatibility | Search for "OGG", "Opus" in workflow | Must explicitly mention format conversion and validation |
| Dependency Transparency | Extract all external references | Must document: mp3-to-ogg, path-cleaner, tts API, message API |

**Implementation**:
```python
def check_constitution_alignment(skill_md_content, constitution_content):
    results = {
        'single_responsibility': check_single_responsibility(skill_md_content),
        'format_compatibility': check_format_compatibility(skill_md_content),
        'dependency_transparency': check_dependency_transparency(skill_md_content)
    }
    return results

def check_format_compatibility(content):
    required_terms = ['OGG', 'Opus', 'convert']
    found = [term for term in required_terms if term.lower() in content.lower()]
    return {
        'pass': len(found) == len(required_terms),
        'found': found,
        'missing': [t for t in required_terms if t not in found]
    }
```

---

### Q5: Report Output Format

**Decision**: Dual output format - JSON for agents, Markdown for humans

**Rationale**:
- AI agents need structured JSON for parsing
- Human reviewers need readable markdown reports
- Support both with `--format` flag

**JSON Structure**:
```json
{
  "summary": {
    "total_checks": 10,
    "passed": 8,
    "failed": 2,
    "warnings": 3
  },
  "path_validation": {
    "total_paths": 5,
    "valid": 3,
    "external": 2,
    "broken": 0
  },
  "code_validation": {
    "python_blocks": 2,
    "bash_blocks": 1,
    "syntax_errors": []
  },
  "constitution_alignment": {
    "single_responsibility": {"pass": true},
    "format_compatibility": {"pass": true},
    "dependency_transparency": {"pass": false, "missing": ["error handling"]}
  },
  "recommendations": [
    "Add error handling examples for failed conversions",
    "Document expected output format for success verification"
  ]
}
```

**Markdown Structure**:
```markdown
# SKILL.md Review Report

**Generated**: 2026-03-09  
**Status**: ⚠️ 2 issues found

## Summary
- ✅ 8/10 checks passed
- ❌ 2 checks failed
- ⚠️ 3 warnings

## Path Validation
✅ All paths validated (3 local, 2 external)

## Code Syntax
✅ All code blocks valid

## Constitution Alignment
❌ Dependency Transparency: Missing error handling documentation

## Recommendations
1. Add error handling examples...
```

---

## Technology Stack Summary

| Component | Technology | Justification |
|-----------|-----------|---------------|
| Language | Python 3.9+ | Cross-platform, stdlib-focused, minimal dependencies |
| Parsing | re + yaml (stdlib) | Sufficient for SKILL.md structure, no heavy dependencies |
| Path validation | pathlib (stdlib) | Cross-platform path handling |
| Syntax check | ast (stdlib) + regex | Built-in Python parser, basic bash validation |
| Output | json (stdlib) + custom markdown | Dual format for agents and humans |
| Testing | pytest | Industry standard, simple fixture-based testing |

---

## Best Practices Applied

1. **Zero External Dependencies** (except pytest for testing): Aligns with constitution's simplicity and offline-capable constraint
2. **Cross-Platform**: Uses pathlib for Windows/Linux/macOS compatibility
3. **Fail Fast**: Non-zero exit codes on validation failures
4. **Structured Output**: JSON for programmatic consumption, Markdown for human review
5. **Tiered Validation**: Distinguishes local/external/placeholder paths to avoid false positives

---

## Open Questions / Future Enhancements

- **Q**: Should we validate API signatures (tts, exec, message methods)?
  - **A**: Out of scope - these are external framework APIs not in this repo
  
- **Q**: Should we check for version-specific dependency references?
  - **A**: Flag as warning if version numbers detected, recommend version pinning in docs

- **Q**: Should we auto-fix issues or only report?
  - **A**: Report only per spec - fixes are out of scope for this feature
