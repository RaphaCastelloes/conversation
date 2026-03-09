# Data Model: SKILL.md Documentation Review

**Feature**: 001-review-skill-doc  
**Date**: 2026-03-09  
**Purpose**: Define the data structures used in the documentation validation process

## Core Entities

### SkillDocument

Represents the parsed SKILL.md file being reviewed.

**Attributes**:
- `frontmatter`: Dictionary containing YAML metadata (name, description)
- `sections`: List of DocumentSection objects
- `code_blocks`: List of CodeBlock objects
- `file_paths`: List of FilePath objects
- `raw_content`: String of original markdown content

**Validation Rules**:
- Frontmatter MUST contain `name` and `description` fields
- At least one section with heading "Agent Workflow" MUST exist
- Description MUST be non-empty and < 500 characters

**Relationships**:
- Contains multiple DocumentSection instances
- Contains multiple CodeBlock instances
- Contains multiple FilePath instances

---

### DocumentSection

Represents a markdown section (heading + content).

**Attributes**:
- `heading`: String (e.g., "Agent Workflow", "WhatsApp Audio Sender")
- `level`: Integer (1-6, markdown heading level)
- `content`: String (section body text)
- `line_number`: Integer (starting line in SKILL.md)

**Validation Rules**:
- Heading MUST NOT be empty
- Level MUST be between 1 and 6

---

### CodeBlock

Represents a code example within SKILL.md.

**Attributes**:
- `language`: String (e.g., "python", "bash", None for unmarked blocks)
- `content`: String (code content)
- `line_number`: Integer (starting line in SKILL.md)
- `syntax_valid`: Boolean (result of syntax validation)
- `syntax_errors`: List of error messages (if any)

**Validation Rules**:
- If language is "python", content MUST parse with `ast.parse()`
- If language is "bash", content MUST pass basic syntax checks
- Content MUST NOT be empty

**State Transitions**:
1. **Extracted** → Initial state after parsing
2. **Validated** → After syntax validation completes
3. **Reported** → Included in validation report

---

### FilePath

Represents a file or directory path referenced in SKILL.md.

**Attributes**:
- `path_string`: String (original path as written)
- `path_type`: Enum ("local", "external", "placeholder")
- `exists`: Boolean (for local paths only)
- `line_number`: Integer (where path appears in SKILL.md)
- `context`: String (surrounding text for context)

**Validation Rules**:
- `path_type` determination:
  - "placeholder" if contains `<...>` pattern
  - "external" if absolute path outside repo root
  - "local" otherwise
- `exists` check only applies to "local" paths

---

### ConstitutionPrinciple

Represents one of the three constitution principles being checked.

**Attributes**:
- `name`: String ("Single Responsibility", "Format Compatibility", "Dependency Transparency")
- `required_keywords`: List of strings (terms that should appear in SKILL.md)
- `validation_result`: Boolean (pass/fail)
- `found_keywords`: List of strings (keywords found in document)
- `missing_keywords`: List of strings (keywords not found)
- `notes`: String (additional context or manual review flags)

**Validation Rules**:
- Each principle MUST have at least one required keyword
- `validation_result` is True only if all required keywords found

---

### ValidationReport

Represents the complete review output.

**Attributes**:
- `timestamp`: DateTime (when review was performed)
- `skill_doc`: SkillDocument reference
- `summary`: ReportSummary object
- `path_results`: List of PathValidationResult objects
- `code_results`: List of CodeValidationResult objects
- `constitution_results`: List of ConstitutionValidationResult objects
- `recommendations`: List of strings
- `exit_code`: Integer (0 = all pass, 1 = failures found)

**Validation Rules**:
- Summary MUST aggregate all sub-results
- Exit code MUST be non-zero if any validation fails

---

### ReportSummary

Aggregated validation statistics.

**Attributes**:
- `total_checks`: Integer
- `passed`: Integer
- `failed`: Integer
- `warnings`: Integer
- `overall_status`: Enum ("PASS", "FAIL", "WARNING")

**Validation Rules**:
- `total_checks` = `passed` + `failed` + `warnings`
- `overall_status` = "FAIL" if `failed` > 0, else "WARNING" if `warnings` > 0, else "PASS"

---

### PathValidationResult

Result of validating a single file path.

**Attributes**:
- `file_path`: FilePath reference
- `status`: Enum ("VALID", "BROKEN", "EXTERNAL", "PLACEHOLDER")
- `message`: String (explanation)

---

### CodeValidationResult

Result of validating a single code block.

**Attributes**:
- `code_block`: CodeBlock reference
- `status`: Enum ("VALID", "SYNTAX_ERROR")
- `errors`: List of error messages

---

### ConstitutionValidationResult

Result of checking one constitution principle.

**Attributes**:
- `principle`: ConstitutionPrinciple reference
- `status`: Enum ("PASS", "FAIL", "MANUAL_REVIEW")
- `details`: String (explanation of result)

---

## Data Flow

```
SKILL.md (file)
    ↓
[Parse] → SkillDocument
    ↓
[Extract] → DocumentSection[], CodeBlock[], FilePath[]
    ↓
[Validate Paths] → PathValidationResult[]
    ↓
[Validate Code] → CodeValidationResult[]
    ↓
[Check Constitution] → ConstitutionValidationResult[]
    ↓
[Aggregate] → ValidationReport
    ↓
[Output] → JSON / Markdown
```

---

## Enumerations

### PathType
- `LOCAL`: Path relative to repo or absolute within repo
- `EXTERNAL`: Absolute path outside repo (dependency)
- `PLACEHOLDER`: Example path with `<...>` markers

### ValidationStatus
- `PASS`: Validation succeeded
- `FAIL`: Validation failed
- `WARNING`: Non-critical issue detected
- `MANUAL_REVIEW`: Requires human judgment

### OutputFormat
- `JSON`: Structured JSON for agent consumption
- `MARKDOWN`: Human-readable markdown report
- `BOTH`: Generate both formats

---

## Validation Workflow

1. **Parse SKILL.md** → Create SkillDocument
2. **Extract Components** → Populate sections, code_blocks, file_paths
3. **Validate Paths** → Check each FilePath, create PathValidationResult
4. **Validate Code** → Parse each CodeBlock, create CodeValidationResult
5. **Check Constitution** → Match keywords, create ConstitutionValidationResult
6. **Generate Report** → Aggregate all results into ValidationReport
7. **Output** → Serialize to JSON/Markdown based on format flag

---

## Example Instance

```python
# Sample SkillDocument instance
skill_doc = SkillDocument(
    frontmatter={
        'name': 'whatsapp-audio-sender',
        'description': 'Sends text-to-speech (TTS) audio to WhatsApp...'
    },
    sections=[
        DocumentSection(
            heading='WhatsApp Audio Sender',
            level=1,
            content='This skill automates...',
            line_number=6
        ),
        DocumentSection(
            heading='Agent Workflow',
            level=2,
            content='When a request...',
            line_number=10
        )
    ],
    code_blocks=[
        CodeBlock(
            language='python',
            content='tts_response = default_api.tts(text = "<user_message>")',
            line_number=16,
            syntax_valid=True,
            syntax_errors=[]
        )
    ],
    file_paths=[
        FilePath(
            path_string='/home/opc/.openclaw/workspace/skills/mp3-to-ogg/scripts/convert_mp3_to_ogg.py',
            path_type=PathType.EXTERNAL,
            exists=None,  # Not checked for external paths
            line_number=27
        )
    ]
)
```
