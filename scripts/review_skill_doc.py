#!/usr/bin/env python3
"""
SKILL.md Documentation Review Tool

Validates SKILL.md documentation against:
1. Path accuracy - All referenced files exist or are marked as external
2. Code syntax - All code examples are syntactically valid
3. Constitution alignment - Documentation follows the 3 core principles
"""

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Any


# ============================================================================
# Enumerations
# ============================================================================

class PathType(Enum):
    LOCAL = "local"
    EXTERNAL = "external"
    PLACEHOLDER = "placeholder"


class ValidationStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    VALID = "VALID"
    BROKEN = "BROKEN"
    SYNTAX_ERROR = "SYNTAX_ERROR"
    MANUAL_REVIEW = "MANUAL_REVIEW"


# ============================================================================
# Data Classes - Foundational (Phase 2: T004-T007)
# ============================================================================

@dataclass
class DocumentSection:
    """Represents a markdown section (heading + content)."""
    heading: str
    level: int
    content: str
    line_number: int


@dataclass
class CodeBlock:
    """Represents a code example within SKILL.md."""
    language: Optional[str]
    content: str
    line_number: int
    syntax_valid: bool = False
    syntax_errors: List[str] = field(default_factory=list)


@dataclass
class FilePath:
    """Represents a file or directory path referenced in SKILL.md."""
    path_string: str
    path_type: PathType
    exists: Optional[bool]
    line_number: int
    context: str = ""


@dataclass
class SkillDocument:
    """Represents the parsed SKILL.md file being reviewed."""
    frontmatter: Dict[str, Any]
    sections: List[DocumentSection]
    code_blocks: List[CodeBlock]
    file_paths: List[FilePath]
    raw_content: str


# ============================================================================
# Data Classes - User Story 1 (Phase 3: T015-T016)
# ============================================================================

@dataclass
class PathValidationResult:
    """Result of validating a single file path."""
    file_path: FilePath
    status: ValidationStatus
    message: str


@dataclass
class CodeValidationResult:
    """Result of validating a single code block."""
    code_block: CodeBlock
    status: ValidationStatus
    errors: List[str] = field(default_factory=list)


# ============================================================================
# Data Classes - User Story 2 (Phase 4: T029-T030)
# ============================================================================

@dataclass
class ConstitutionPrinciple:
    """Represents one of the three constitution principles being checked."""
    name: str
    required_keywords: List[str]
    validation_result: bool = False
    found_keywords: List[str] = field(default_factory=list)
    missing_keywords: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class ConstitutionValidationResult:
    """Result of checking one constitution principle."""
    principle: ConstitutionPrinciple
    status: ValidationStatus
    details: str


# ============================================================================
# Data Classes - Report Generation (Phase 6: T044-T045)
# ============================================================================

@dataclass
class ReportSummary:
    """Aggregated validation statistics."""
    total_checks: int
    passed: int
    failed: int
    warnings: int
    overall_status: ValidationStatus


@dataclass
class ValidationReport:
    """Represents the complete review output."""
    timestamp: datetime
    skill_file: str
    constitution_file: str
    summary: ReportSummary
    path_results: List[PathValidationResult]
    code_results: List[CodeValidationResult]
    constitution_results: List[ConstitutionValidationResult]
    recommendations: List[str]
    exit_code: int


# ============================================================================
# Parsing Functions - Foundational (Phase 2: T008-T011)
# ============================================================================

def parse_frontmatter(content: str) -> Dict[str, Any]:
    """Extract YAML frontmatter from SKILL.md."""
    pattern = r'^---\n(.*?)\n---'
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    
    if not match:
        return {}
    
    frontmatter_text = match.group(1)
    result = {}
    
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip()
    
    return result


def extract_sections(content: str) -> List[DocumentSection]:
    """Extract markdown sections with headings."""
    sections = []
    lines = content.split('\n')
    current_section = None
    current_content = []
    
    for i, line in enumerate(lines, 1):
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        
        if heading_match:
            if current_section:
                current_section.content = '\n'.join(current_content).strip()
                sections.append(current_section)
            
            level = len(heading_match.group(1))
            heading = heading_match.group(2)
            current_section = DocumentSection(
                heading=heading,
                level=level,
                content="",
                line_number=i
            )
            current_content = []
        elif current_section:
            current_content.append(line)
    
    if current_section:
        current_section.content = '\n'.join(current_content).strip()
        sections.append(current_section)
    
    return sections


def extract_code_blocks(content: str) -> List[CodeBlock]:
    """Extract code blocks with language detection."""
    code_blocks = []
    lines = content.split('\n')
    in_code_block = False
    current_language = None
    current_code = []
    start_line = 0
    
    for i, line in enumerate(lines, 1):
        if line.startswith('```'):
            if not in_code_block:
                in_code_block = True
                start_line = i
                lang_match = re.match(r'```(\w+)?', line)
                current_language = lang_match.group(1) if lang_match and lang_match.group(1) else None
                current_code = []
            else:
                in_code_block = False
                code_blocks.append(CodeBlock(
                    language=current_language,
                    content='\n'.join(current_code),
                    line_number=start_line
                ))
                current_language = None
                current_code = []
        elif in_code_block:
            current_code.append(line)
    
    return code_blocks


def extract_file_paths(content: str) -> List[FilePath]:
    """Extract file paths with regex for Unix/Windows paths."""
    file_paths = []
    lines = content.split('\n')
    
    # Patterns for different path types
    unix_path_pattern = r'(?:/[\w\-./]+(?:\.[\w]+)?)'
    windows_path_pattern = r'(?:[A-Z]:\\[\w\-\\./]+(?:\.[\w]+)?)'
    
    for i, line in enumerate(lines, 1):
        # Find Unix paths
        for match in re.finditer(unix_path_pattern, line):
            path_str = match.group(0)
            file_paths.append(FilePath(
                path_string=path_str,
                path_type=PathType.EXTERNAL,  # Will be determined later
                exists=None,
                line_number=i,
                context=line.strip()
            ))
        
        # Find Windows paths
        for match in re.finditer(windows_path_pattern, line):
            path_str = match.group(0)
            file_paths.append(FilePath(
                path_string=path_str,
                path_type=PathType.EXTERNAL,  # Will be determined later
                exists=None,
                line_number=i,
                context=line.strip()
            ))
    
    return file_paths


def parse_skill_document(file_path: Path) -> SkillDocument:
    """Parse SKILL.md into a SkillDocument object."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        print(f"ERROR: SKILL.md not found at {file_path}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"ERROR: Failed to read SKILL.md: {e}", file=sys.stderr)
        sys.exit(3)
    
    try:
        frontmatter = parse_frontmatter(content)
        sections = extract_sections(content)
        code_blocks = extract_code_blocks(content)
        file_paths = extract_file_paths(content)
        
        return SkillDocument(
            frontmatter=frontmatter,
            sections=sections,
            code_blocks=code_blocks,
            file_paths=file_paths,
            raw_content=content
        )
    except Exception as e:
        print(f"ERROR: Failed to parse SKILL.md: {e}", file=sys.stderr)
        sys.exit(3)


# ============================================================================
# Path Validation - User Story 1 (Phase 3: T017-T020, T023)
# ============================================================================

def determine_path_type(path_str: str, repo_root: Path) -> PathType:
    """Determine if path is local, external, or placeholder."""
    # Check for placeholder pattern
    if '<' in path_str and '>' in path_str:
        return PathType.PLACEHOLDER
    
    # Unix absolute paths starting with / are typically external dependencies
    if path_str.startswith('/'):
        # Check if it starts with common external paths
        external_prefixes = ['/home/', '/usr/', '/opt/', '/var/', '/etc/']
        if any(path_str.startswith(prefix) for prefix in external_prefixes):
            return PathType.EXTERNAL
    
    path = Path(path_str)
    
    # Check if it's an absolute path
    if path.is_absolute():
        # Check if it's within the repo
        try:
            path.relative_to(repo_root)
            return PathType.LOCAL
        except (ValueError, OSError):
            return PathType.EXTERNAL
    
    # Relative path - treat as local
    return PathType.LOCAL


def validate_paths(skill_doc: SkillDocument, repo_root: Path) -> List[PathValidationResult]:
    """Validate all file paths in the document."""
    results = []
    
    for file_path in skill_doc.file_paths:
        # Determine path type
        file_path.path_type = determine_path_type(file_path.path_string, repo_root)
        
        if file_path.path_type == PathType.PLACEHOLDER:
            results.append(PathValidationResult(
                file_path=file_path,
                status=ValidationStatus.VALID,
                message="Placeholder path (example code)"
            ))
        elif file_path.path_type == PathType.EXTERNAL:
            results.append(PathValidationResult(
                file_path=file_path,
                status=ValidationStatus.WARNING,
                message="External dependency - not validated"
            ))
        else:  # LOCAL
            # Check if path exists
            path = Path(file_path.path_string)
            if not path.is_absolute():
                path = repo_root / path
            
            file_path.exists = path.exists()
            
            if file_path.exists:
                results.append(PathValidationResult(
                    file_path=file_path,
                    status=ValidationStatus.VALID,
                    message="Path exists"
                ))
            else:
                results.append(PathValidationResult(
                    file_path=file_path,
                    status=ValidationStatus.BROKEN,
                    message=f"Local path not found"
                ))
    
    return results


# ============================================================================
# Code Validation - User Story 1 (Phase 3: T021-T022, T024)
# ============================================================================

def validate_python_code(code: str) -> tuple[bool, List[str]]:
    """Validate Python code syntax using ast.parse()."""
    try:
        ast.parse(code)
        return True, []
    except SyntaxError as e:
        return False, [f"SyntaxError at line {e.lineno}: {e.msg}"]
    except Exception as e:
        return False, [f"Parse error: {str(e)}"]


def validate_bash_code(code: str) -> tuple[bool, List[str]]:
    """Basic bash code validation (unmatched quotes, unclosed expansions)."""
    errors = []
    
    # Check for unmatched double quotes
    if code.count('"') % 2 != 0:
        errors.append("Unmatched double quotes")
    
    # Check for unmatched single quotes
    if code.count("'") % 2 != 0:
        errors.append("Unmatched single quotes")
    
    # Check for unclosed variable expansions
    if re.search(r'\$\{[^}]*$', code):
        errors.append("Unclosed variable expansion")
    
    return len(errors) == 0, errors


def validate_code(skill_doc: SkillDocument) -> List[CodeValidationResult]:
    """Validate all code blocks in the document."""
    results = []
    
    for code_block in skill_doc.code_blocks:
        if code_block.language == 'python':
            valid, errors = validate_python_code(code_block.content)
            code_block.syntax_valid = valid
            code_block.syntax_errors = errors
            
            results.append(CodeValidationResult(
                code_block=code_block,
                status=ValidationStatus.VALID if valid else ValidationStatus.SYNTAX_ERROR,
                errors=errors
            ))
        elif code_block.language in ['bash', 'sh', 'shell']:
            valid, errors = validate_bash_code(code_block.content)
            code_block.syntax_valid = valid
            code_block.syntax_errors = errors
            
            results.append(CodeValidationResult(
                code_block=code_block,
                status=ValidationStatus.VALID if valid else ValidationStatus.SYNTAX_ERROR,
                errors=errors
            ))
        else:
            # Skip validation for unmarked or unknown language blocks
            code_block.syntax_valid = True
            results.append(CodeValidationResult(
                code_block=code_block,
                status=ValidationStatus.VALID,
                errors=[]
            ))
    
    return results


# ============================================================================
# Constitution Validation - User Story 2 (Phase 4: T031-T035)
# ============================================================================

def load_constitution_principles() -> List[ConstitutionPrinciple]:
    """Define the three constitution principles with required keywords."""
    return [
        ConstitutionPrinciple(
            name="Single Responsibility",
            required_keywords=["TTS", "WhatsApp", "audio"]
        ),
        ConstitutionPrinciple(
            name="Format Compatibility",
            required_keywords=["OGG", "Opus"]
        ),
        ConstitutionPrinciple(
            name="Dependency Transparency",
            required_keywords=["mp3-to-ogg", "path-cleaner", "tts", "message"]
        )
    ]


def validate_constitution(skill_doc: SkillDocument) -> List[ConstitutionValidationResult]:
    """Check all three constitution principles."""
    principles = load_constitution_principles()
    results = []
    content_lower = skill_doc.raw_content.lower()
    
    for principle in principles:
        found = []
        missing = []
        
        for keyword in principle.required_keywords:
            if keyword.lower() in content_lower:
                found.append(keyword)
            else:
                missing.append(keyword)
        
        principle.found_keywords = found
        principle.missing_keywords = missing
        principle.validation_result = len(missing) == 0
        
        if principle.validation_result:
            status = ValidationStatus.PASS
            details = f"All required keywords found: {', '.join(found)}"
        else:
            status = ValidationStatus.FAIL
            details = f"Missing keywords: {', '.join(missing)}"
        
        results.append(ConstitutionValidationResult(
            principle=principle,
            status=status,
            details=details
        ))
    
    return results


# ============================================================================
# Completeness Assessment - User Story 3 (Phase 5: T038-T042)
# ============================================================================

def assess_completeness(skill_doc: SkillDocument) -> List[str]:
    """Generate recommendations for missing sections."""
    recommendations = []
    content_lower = skill_doc.raw_content.lower()
    
    # Check for prerequisites section
    if 'prerequisite' not in content_lower and 'requirement' not in content_lower:
        recommendations.append("Add prerequisites section documenting required tools and dependencies")
    
    # Check for error handling examples
    if 'error' not in content_lower and 'fail' not in content_lower:
        recommendations.append("Add error handling examples for failed conversions")
    
    # Check for expected output documentation
    if 'output' not in content_lower and 'result' not in content_lower:
        recommendations.append("Document expected output format for success verification")
    
    # Check for troubleshooting guidance
    if 'troubleshoot' not in content_lower and 'debug' not in content_lower:
        recommendations.append("Add troubleshooting section for common issues")
    
    return recommendations


# ============================================================================
# Report Generation - Phase 6 (T046-T052)
# ============================================================================

def generate_json_report(report: ValidationReport) -> str:
    """Generate JSON format report."""
    output = {
        "metadata": {
            "generated": report.timestamp.isoformat(),
            "file": report.skill_file,
            "constitution": report.constitution_file,
            "version": "1.0.0"
        },
        "summary": {
            "total_checks": report.summary.total_checks,
            "passed": report.summary.passed,
            "failed": report.summary.failed,
            "warnings": report.summary.warnings,
            "status": report.summary.overall_status.value
        },
        "path_validation": {
            "total": len(report.path_results),
            "valid": sum(1 for r in report.path_results if r.status == ValidationStatus.VALID),
            "external": sum(1 for r in report.path_results if r.status == ValidationStatus.WARNING),
            "broken": sum(1 for r in report.path_results if r.status == ValidationStatus.BROKEN),
            "results": [
                {
                    "path": r.file_path.path_string,
                    "type": r.file_path.path_type.value,
                    "exists": r.file_path.exists,
                    "status": r.status.value,
                    "line": r.file_path.line_number,
                    "message": r.message
                }
                for r in report.path_results
            ]
        },
        "code_validation": {
            "total": len(report.code_results),
            "valid": sum(1 for r in report.code_results if r.status == ValidationStatus.VALID),
            "errors": sum(1 for r in report.code_results if r.status == ValidationStatus.SYNTAX_ERROR),
            "results": [
                {
                    "language": r.code_block.language,
                    "line": r.code_block.line_number,
                    "status": r.status.value,
                    "errors": r.errors
                }
                for r in report.code_results
            ]
        },
        "constitution_alignment": {
            "principles": [
                {
                    "name": r.principle.name,
                    "status": r.status.value,
                    "found_keywords": r.principle.found_keywords,
                    "missing_keywords": r.principle.missing_keywords,
                    "details": r.details
                }
                for r in report.constitution_results
            ]
        },
        "recommendations": report.recommendations,
        "exit_code": report.exit_code
    }
    
    return json.dumps(output, indent=2)


def generate_markdown_report(report: ValidationReport) -> str:
    """Generate Markdown format report."""
    status_emoji = {
        ValidationStatus.PASS: "✅",
        ValidationStatus.FAIL: "❌",
        ValidationStatus.WARNING: "⚠️"
    }
    
    overall_emoji = status_emoji.get(report.summary.overall_status, "❓")
    
    lines = [
        "# SKILL.md Review Report",
        "",
        f"**Generated**: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
        f"**File**: {report.skill_file}",
        f"**Status**: {overall_emoji} {report.summary.overall_status.value}",
        "",
        "## Summary",
        f"- Total Checks: {report.summary.total_checks}",
        f"- Passed: {report.summary.passed}",
        f"- Failed: {report.summary.failed}",
        f"- Warnings: {report.summary.warnings}",
        ""
    ]
    
    # Path Validation Section
    valid_count = sum(1 for r in report.path_results if r.status == ValidationStatus.VALID)
    total_paths = len(report.path_results)
    
    lines.extend([
        "## Path Validation",
        f"{'✅' if report.summary.failed == 0 else '❌'} **{valid_count}/{total_paths} paths valid**",
        ""
    ])
    
    for result in report.path_results:
        emoji = "✅" if result.status == ValidationStatus.VALID else ("⚠️" if result.status == ValidationStatus.WARNING else "❌")
        lines.append(f"- {emoji} `{result.file_path.path_string}` ({result.file_path.path_type.value}, line {result.file_path.line_number}): {result.message}")
    
    lines.append("")
    
    # Code Syntax Validation Section
    valid_code = sum(1 for r in report.code_results if r.status == ValidationStatus.VALID)
    total_code = len(report.code_results)
    
    lines.extend([
        "## Code Syntax Validation",
        f"{'✅' if valid_code == total_code else '❌'} **{valid_code}/{total_code} code blocks valid**",
        ""
    ])
    
    for result in report.code_results:
        emoji = "✅" if result.status == ValidationStatus.VALID else "❌"
        lang = result.code_block.language or "unmarked"
        if result.errors:
            lines.append(f"- {emoji} {lang.capitalize()} block at line {result.code_block.line_number}: {', '.join(result.errors)}")
        else:
            lines.append(f"- {emoji} {lang.capitalize()} block at line {result.code_block.line_number}")
    
    lines.append("")
    
    # Constitution Alignment Section
    lines.extend([
        "## Constitution Alignment",
        ""
    ])
    
    for result in report.constitution_results:
        emoji = "✅" if result.status == ValidationStatus.PASS else "❌"
        lines.append(f"{emoji} **{result.principle.name}**: {result.details}")
    
    lines.append("")
    
    # Recommendations
    if report.recommendations:
        lines.extend([
            "## Recommendations",
            ""
        ])
        for i, rec in enumerate(report.recommendations, 1):
            lines.append(f"{i}. {rec}")
        lines.append("")
    
    return '\n'.join(lines)


def create_validation_report(
    skill_doc: SkillDocument,
    skill_file: str,
    constitution_file: str,
    path_results: List[PathValidationResult],
    code_results: List[CodeValidationResult],
    constitution_results: List[ConstitutionValidationResult],
    recommendations: List[str],
    strict_mode: bool = False
) -> ValidationReport:
    """Create a complete validation report with summary."""
    # Calculate summary statistics
    total_checks = len(path_results) + len(code_results) + len(constitution_results)
    
    passed = (
        sum(1 for r in path_results if r.status == ValidationStatus.VALID) +
        sum(1 for r in code_results if r.status == ValidationStatus.VALID) +
        sum(1 for r in constitution_results if r.status == ValidationStatus.PASS)
    )
    
    failed = (
        sum(1 for r in path_results if r.status == ValidationStatus.BROKEN) +
        sum(1 for r in code_results if r.status == ValidationStatus.SYNTAX_ERROR) +
        sum(1 for r in constitution_results if r.status == ValidationStatus.FAIL)
    )
    
    warnings = sum(1 for r in path_results if r.status == ValidationStatus.WARNING)
    
    # Determine overall status
    if failed > 0:
        overall_status = ValidationStatus.FAIL
        exit_code = 1
    elif warnings > 0 and strict_mode:
        overall_status = ValidationStatus.FAIL
        exit_code = 1
    elif warnings > 0:
        overall_status = ValidationStatus.WARNING
        exit_code = 0
    else:
        overall_status = ValidationStatus.PASS
        exit_code = 0
    
    summary = ReportSummary(
        total_checks=total_checks,
        passed=passed,
        failed=failed,
        warnings=warnings,
        overall_status=overall_status
    )
    
    return ValidationReport(
        timestamp=datetime.now(),
        skill_file=skill_file,
        constitution_file=constitution_file,
        summary=summary,
        path_results=path_results,
        code_results=code_results,
        constitution_results=constitution_results,
        recommendations=recommendations,
        exit_code=exit_code
    )


# ============================================================================
# CLI and Main - Foundational (Phase 2: T012-T014)
# ============================================================================

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="SKILL.md Documentation Review Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/review_skill_doc.py
  python scripts/review_skill_doc.py --format json --output report.json
  python scripts/review_skill_doc.py --strict
        """
    )
    
    parser.add_argument(
        '-s', '--skill-file',
        type=Path,
        default=Path('./SKILL.md'),
        help='Path to SKILL.md file to review (default: ./SKILL.md)'
    )
    
    parser.add_argument(
        '-c', '--constitution',
        type=Path,
        default=Path('./.specify/memory/constitution.md'),
        help='Path to constitution file (default: ./.specify/memory/constitution.md)'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['json', 'markdown', 'both'],
        default='markdown',
        help='Output format (default: markdown)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file path (default: stdout)'
    )
    
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Fail on warnings (exit code 1)'
    )
    
    return parser.parse_args()


def main():
    """Main entry point for the SKILL.md review tool."""
    args = parse_arguments()
    
    # Determine repository root
    repo_root = Path.cwd()
    
    # Parse SKILL.md
    skill_doc = parse_skill_document(args.skill_file)
    
    # Validate paths
    path_results = validate_paths(skill_doc, repo_root)
    
    # Validate code
    code_results = validate_code(skill_doc)
    
    # Validate constitution alignment
    constitution_results = validate_constitution(skill_doc)
    
    # Assess completeness
    recommendations = assess_completeness(skill_doc)
    
    # Create report
    report = create_validation_report(
        skill_doc=skill_doc,
        skill_file=str(args.skill_file),
        constitution_file=str(args.constitution),
        path_results=path_results,
        code_results=code_results,
        constitution_results=constitution_results,
        recommendations=recommendations,
        strict_mode=args.strict
    )
    
    # Generate output
    if args.format == 'json':
        output_text = generate_json_report(report)
    elif args.format == 'markdown':
        output_text = generate_markdown_report(report)
    else:  # both
        if args.output:
            # Write both formats with different extensions
            json_path = args.output.with_suffix('.json')
            md_path = args.output.with_suffix('.md')
            
            json_path.write_text(generate_json_report(report), encoding='utf-8')
            md_path.write_text(generate_markdown_report(report), encoding='utf-8')
            
            print(f"Reports generated: {json_path} and {md_path}")
            sys.exit(report.exit_code)
        else:
            print("ERROR: --output required when using --format both", file=sys.stderr)
            sys.exit(4)
    
    # Write output
    if args.output:
        try:
            args.output.write_text(output_text, encoding='utf-8')
            print(f"Report written to {args.output}")
        except Exception as e:
            print(f"ERROR: Failed to write output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output_text)
    
    # Exit with appropriate code
    sys.exit(report.exit_code)


if __name__ == '__main__':
    main()
