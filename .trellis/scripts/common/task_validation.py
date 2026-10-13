"""Read-only planning and decision checks, enabled per project."""

from __future__ import annotations

import json
from dataclasses import dataclass, field, replace
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Literal, NoReturn

from .paths import DIR_ARCHIVE, DIR_WORKFLOW, FILE_TASK_JSON, get_tasks_dir
from .task_utils import resolve_task_dir
from .trellis_config import _strip_inline_comment, parse_simple_yaml


@dataclass(frozen=True)
class ValidationIssue:
    path: Path
    line: int | None
    message: str
    hint: str
    severity: Literal["error", "warning"] = "error"

    def __str__(self) -> str:
        location = f"{self.path}:{self.line}" if self.line is not None else str(self.path)
        return f"{self.severity.capitalize()}: {location}: {self.message}\n  Hint: {self.hint}"


@dataclass
class _Decision:
    path: Path
    text: str | None = None
    metadata: dict[str, object] | None = None
    issues: list[ValidationIssue] = field(default_factory=list)


_PLANNING_SECTIONS = {
    "prd.md": ("Goal", "Requirements", "Acceptance Criteria"),
    "design.md": ("Scope", "Contracts", "Data Flow", "Tradeoffs", "Rollout and Rollback"),
    "implement.md": ("Ordered Steps", "Validation", "Review Gates", "Rollback Points"),
}
_DECISION_SECTIONS = ("Context", "Options Considered", "Decision", "Applicability")
_SETTING = "task_structure_validation"


def _read_text(path: Path, issues: list[ValidationIssue]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError, ValueError) as exc:
        issues.append(ValidationIssue(path, None, f"Cannot read UTF-8 file: {exc}",
                                      "Restore the file and its read permissions."))
        return None


def _unique_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> NoReturn:
    raise ValueError(f"Not a JSON value: {value}")


def _json_object(text: str) -> dict[str, object]:
    value = json.loads(text, object_pairs_hook=_unique_pairs, parse_constant=_reject_constant)
    if not isinstance(value, dict):
        raise ValueError("Expected a JSON object")
    return value


def _enabled(repo_root: Path, issues: list[ValidationIssue]) -> bool:
    path = repo_root / DIR_WORKFLOW / "config.yaml"
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        if path.is_symlink():
            issues.append(ValidationIssue(path, None, "Configuration symlink is broken.",
                                          "Restore its target; an unreadable configuration is not disabled."))
        return False
    except (OSError, UnicodeError) as exc:
        issues.append(ValidationIssue(path, None, f"Cannot read configuration: {exc}",
                                      "Restore a readable UTF-8 configuration."))
        return False

    declarations: list[tuple[int, str]] = []
    continuation = False
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = _strip_inline_comment(raw).strip()
        if not line:
            continue
        if raw[0].isspace():
            if continuation:
                issues.append(ValidationIssue(path, lineno, "Validation setting cannot have an indented body.",
                                              f"Use one top-level {_SETTING}: true or false scalar."))
            continue
        continuation = False
        key, separator, value = line.partition(":")
        # Unrelated YAML forms must not opt projects in or block them.
        if key.strip(" \"'?-") != _SETTING:
            continue
        declarations.append((lineno, value))
        continuation = True
        if not separator or key != _SETTING or value.strip() not in ("true", "false"):
            issues.append(ValidationIssue(path, lineno, "Invalid validation setting.",
                                          f"Use exactly {_SETTING}: true or {_SETTING}: false (unquoted)."))
    if len(declarations) > 1:
        issues.append(ValidationIssue(path, declarations[1][0], "Duplicate validation setting.",
                                      f"Keep exactly one top-level {_SETTING} declaration."))
    if issues or not declarations:
        return False
    # Retain the scalar interpretation shared by all other configuration readers.
    return parse_simple_yaml(f"{_SETTING}: {declarations[0][1]}", source=str(path))[_SETTING] == "true"


def _markdown_sections(text: str, path: Path, required: tuple[str, ...]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    sections: dict[str, list[int]] = {}
    populated: set[int] = set()
    current: int | None = None
    fence = ""
    fence_line = 0
    comment_line: int | None = None
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if fence:
            if line.startswith(fence) and not line.strip(fence[0]):
                fence = ""
            elif line and current is not None and line.strip("`~"):
                populated.add(current)
            continue

        visible = ""
        remainder = raw
        while remainder:
            if comment_line is not None:
                _, end, remainder = remainder.partition("-->")
                if not end:
                    break
                comment_line = None
            else:
                before, start, remainder = remainder.partition("<!--")
                visible += before
                if not start:
                    break
                comment_line = lineno
        line = visible.strip()
        if not line:
            continue
        if line.startswith(("```", "~~~")):
            fence = line[:len(line) - len(line.lstrip(line[0]))]
            fence_line = lineno
            continue
        level = len(line) - len(line.lstrip("#"))
        if 1 <= level <= 6 and (len(line) == level or line[level].isspace()):
            if level <= 2:
                current = None
            if level == 2:
                heading = line[2:].strip()
                without_closing = heading.rstrip("#")
                if without_closing != heading and without_closing.endswith(" "):
                    heading = without_closing.rstrip()
                sections.setdefault(heading, []).append(lineno)
                current = lineno
            continue
        if current is not None:
            populated.add(current)

    if fence:
        issues.append(ValidationIssue(path, fence_line, "Unclosed code fence.", "Close the matching code fence."))
    if comment_line is not None:
        issues.append(ValidationIssue(path, comment_line, "Unclosed HTML comment.", "Close the comment with -->."))
    for heading in required:
        occurrences = sections.get(heading, [])
        if not occurrences:
            issues.append(ValidationIssue(path, None, f"Missing section: ## {heading}.",
                                          "Add the required level-two heading and substantive content."))
        elif len(occurrences) > 1:
            issues.append(ValidationIssue(path, occurrences[1], f"Duplicate section: ## {heading}.",
                                          "Keep exactly one instance of this required section."))
        for lineno in occurrences:
            if lineno not in populated:
                issues.append(ValidationIssue(path, lineno, f"Empty section: ## {heading}.",
                                              "Add content other than headings, comments or fence markers."))
    return issues


def _is_segment(value: object) -> bool:
    return (isinstance(value, str) and bool(value) and value not in (".", "..")
            and not any(char in value for char in ("/", "\\", "\0"))
            and not PureWindowsPath(value).drive)


def _read_decision(path: Path, boundary: Path) -> _Decision:
    record = _Decision(path)
    if not _is_segment(path.stem) or path.stem.casefold() == "readme":
        record.issues.append(ValidationIssue(path, None, "Invalid decision filename ID.",
                                             "Use a single non-reserved filename stem, not README, . or ..."))
    try:
        if path.resolve().parent != boundary:
            record.issues.append(ValidationIssue(path, None, "Decision path escapes the decisions directory.",
                                                 "Keep the record and its symlink target inside the flat decisions directory."))
            return record
    except (OSError, RuntimeError, ValueError) as exc:
        record.issues.append(ValidationIssue(path, None, f"Cannot resolve decision path: {exc}",
                                             "Repair the decision path or symlink."))
        return record
    record.text = _read_text(path, record.issues)
    if record.text is None:
        return record
    lines = record.text.splitlines()
    first = next((i for i, line in enumerate(lines) if line.strip()), len(lines))
    if first == len(lines) or not lines[first].startswith("# ") or not lines[first][2:].strip():
        record.issues.append(ValidationIssue(path, first + 1, "Decision must begin with a level-one title.",
                                             "Start with # <title>, followed by the JSON metadata fence."))
        return record
    start = first + 1
    while start < len(lines) and not lines[start].strip():
        start += 1
    opener = lines[start].strip() if start < len(lines) else ""
    fence = opener[:len(opener) - len(opener.lstrip(opener[0]))] if opener else ""
    if not fence.startswith(("```", "~~~")) or opener[len(fence):].strip() != "json":
        record.issues.append(ValidationIssue(path, start + 1, "Missing JSON metadata immediately after title.",
                                             "Insert the JSON fenced block from decisions/README.md; only blank lines may intervene."))
        return record
    end = start + 1
    while end < len(lines):
        stripped = lines[end].strip()
        if stripped.startswith(fence) and not stripped.strip(fence[0]):
            break
        end += 1
    if end == len(lines):
        record.issues.append(ValidationIssue(path, start + 1, "Unclosed metadata fence.", "Close the JSON code fence."))
        return record
    try:
        record.metadata = _json_object("\n".join(lines[start + 1:end]))
    except (ValueError, RecursionError) as exc:
        lineno = start + 1 + exc.lineno if isinstance(exc, json.JSONDecodeError) else start + 2
        record.issues.append(ValidationIssue(path, lineno, f"Invalid decision metadata: {exc}",
                                             "Use a JSON object with unique keys: status, source_task, reconsiders."))
        return record
    metadata = record.metadata
    if set(metadata) != {"status", "source_task", "reconsiders"}:
        record.issues.append(ValidationIssue(path, start + 2, "Unexpected or missing metadata fields.",
                                             "Use exactly status, source_task and reconsiders."))
    if metadata.get("status") not in ("proposed", "accepted", "rejected"):
        record.issues.append(ValidationIssue(path, start + 2, "Invalid decision status.",
                                             "Choose proposed, accepted or rejected; this is a conclusion, not delivery progress."))
    if not _is_segment(metadata.get("source_task")):
        record.issues.append(ValidationIssue(path, start + 2, "Invalid source_task.",
                                             "Use the full source task directory name, without any path components."))
    predecessor = metadata.get("reconsiders")
    if predecessor is not None and (not _is_segment(predecessor) or str(predecessor).casefold() == "readme"):
        record.issues.append(ValidationIssue(path, start + 2, "Invalid reconsiders ID.",
                                             "Use null or the filename stem of a finalized decision."))
    return record


def _source_task(repo_root: Path, name: str, decision: Path) -> list[ValidationIssue]:
    tasks = get_tasks_dir(repo_root)
    try:
        candidates = [tasks / name] if (tasks / name).is_dir() else []
        archive = tasks / DIR_ARCHIVE
        if archive.exists():
            candidates.extend(month / name for month in archive.iterdir()
                              if month.is_dir() and (month / name).is_dir())
    except (OSError, ValueError) as exc:
        return [ValidationIssue(decision, None, f"Cannot locate source task {name}: {exc}",
                                "Restore access to the active and archived task directories.")]
    if len(candidates) != 1:
        return [ValidationIssue(decision, None, f"Source task {name} resolves to {len(candidates)} directories.",
                                "Use one exact, unique directory name across tasks/ and tasks/archive/*/.")]
    candidate = resolve_task_dir(str(candidates[0]), repo_root)
    if candidate is None:
        return [ValidationIssue(decision, None, f"Source task {name} escapes the task directory.",
                                "Restore the source directory inside the tasks tree.")]
    issues: list[ValidationIssue] = []
    path = candidate / FILE_TASK_JSON
    text = _read_text(path, issues)
    if text is None:
        return issues
    try:
        data = _json_object(text)
    except (ValueError, RecursionError) as exc:
        issues.append(ValidationIssue(path, None, f"Invalid source task JSON: {exc}", "Restore the source task's JSON object."))
        return issues
    # Same MM-DD-slug identity convention as create/rename, without importing task_store.
    parts = name.split("-", 2)
    slug = name
    if (len(parts) == 3 and len(parts[0]) == len(parts[1]) == 2
            and parts[0].isdecimal() and parts[1].isdecimal()
            and 1 <= int(parts[0]) <= 12 and 1 <= int(parts[1]) <= 31):
        slug = parts[2]
    if data.get("id") != slug or data.get("name") != slug:
        issues.append(ValidationIssue(path, None, f"Source task identity does not match directory {name}.",
                                      f"Restore id and name to {slug!r}; do not rewrite archived planning documents."))
    return issues


def _decisions(repo_root: Path, related_files: list[str], task_json: Path) -> list[ValidationIssue]:
    directory = repo_root / DIR_WORKFLOW / "decisions"
    issues: list[ValidationIssue] = []
    roots: set[str] = set()
    try:
        boundary = directory.resolve()
        for entry in related_files:
            parts = PurePosixPath(entry.replace("\\", "/")).parts
            is_decision = any(parts[i:i + 2] == (DIR_WORKFLOW, "decisions") for i in range(len(parts) - 1))
            if not is_decision:
                continue
            path = Path(entry.replace("\\", "/"))
            if not path.is_absolute():
                path = repo_root / path
            if path.suffix != ".md" or path.stem.casefold() == "readme" or not _is_segment(path.stem):
                issues.append(ValidationIssue(task_json, None, f"Invalid related decision: {entry}.",
                                              "Register .trellis/decisions/<id>.md, excluding README.md."))
            elif path.resolve().parent != boundary:
                issues.append(ValidationIssue(task_json, None, f"Related decision escapes the flat directory: {entry}.",
                                              "Use a decision file directly inside .trellis/decisions/."))
            else:
                roots.add(path.stem)
        if not roots:
            return issues
        paths = sorted(path for path in directory.iterdir() if path.suffix == ".md" and path.name != "README.md")
    except (OSError, RuntimeError, ValueError) as exc:
        issues.append(ValidationIssue(directory, None, f"Cannot resolve or enumerate related decisions: {exc}",
                                      "Restore the registered records and directory access."))
        return issues

    records = {path.stem: _read_decision(path, boundary) for path in paths}
    folded: dict[str, list[str]] = {}
    neighbors: dict[str, set[str]] = {name: set() for name in records}
    predecessors: dict[str, str] = {}
    for name, record in records.items():
        folded.setdefault(name.casefold(), []).append(name)
        predecessor = record.metadata.get("reconsiders") if record.metadata is not None else None
        if isinstance(predecessor, str) and _is_segment(predecessor):
            predecessors[name] = predecessor
            neighbors[name].add(predecessor)
            neighbors.setdefault(predecessor, set()).add(name)
    for names in folded.values():
        if len(names) > 1:
            for name in names:
                neighbors[name].update(names)
                records[name].issues.append(ValidationIssue(records[name].path, None, "Case-folded decision ID collision.",
                                                            f"Give these records distinct IDs: {', '.join(sorted(names))}."))

    connected: set[str] = set()
    pending = list(roots)
    while pending:
        name = pending.pop()
        if name not in connected:
            connected.add(name)
            pending.extend(neighbors.get(name, set()) - connected)
    for name in sorted(connected - records.keys()):
        issues.append(ValidationIssue(directory / f"{name}.md", None, "Registered or referenced decision missing.",
                                      "Restore the record or correct relatedFiles/reconsiders to an exact filename ID."))

    for name, record in records.items():
        if name not in connected:
            issues.extend(replace(issue, severity="warning", hint=issue.hint +
                                  " Unrelated record: invalid metadata can conceal unknown links; those links were not checked.")
                          for issue in record.issues)
            continue
        issues.extend(record.issues)
        metadata = record.metadata
        required: tuple[str, ...] = _DECISION_SECTIONS
        if metadata is not None and metadata.get("reconsiders") is not None:
            required += ("Reconsideration",)
        if record.text is not None:
            issues.extend(_markdown_sections(record.text, record.path, required))
        if metadata is not None and _is_segment(metadata.get("source_task")):
            issues.extend(_source_task(repo_root, str(metadata["source_task"]), record.path))
        predecessor = predecessors.get(name)
        if predecessor is not None and predecessor in records:
            previous = records[predecessor].metadata
            if predecessor == name or previous is None or previous.get("status") not in ("accepted", "rejected"):
                issues.append(ValidationIssue(record.path, None, "Reconsideration must reference another finalized decision.",
                                              "Reference an accepted/rejected predecessor, never itself or a proposal."))

    accepted: dict[str, list[str]] = {}
    for name in sorted(connected & records.keys()):
        metadata = records[name].metadata
        predecessor = predecessors.get(name)
        if predecessor is not None and metadata is not None and metadata.get("status") == "accepted":
            accepted.setdefault(predecessor, []).append(name)
    for predecessor, successors in accepted.items():
        if len(successors) > 1:
            issues.append(ValidationIssue(directory / f"{predecessor}.md", None, "Multiple accepted direct successors.",
                                          f"Resolve conflicting accepted successors: {', '.join(successors)}."))

    visited: set[str] = set()
    for name in sorted(connected & records.keys()):
        chain: set[str] = set()
        cursor: str | None = name
        while cursor is not None and cursor in records and cursor not in visited:
            if cursor in chain:
                issues.append(ValidationIssue(records[cursor].path, None, "Cycle in reconsideration references.",
                                              "Remove the cycle; reconsiderations must point to earlier finalized records."))
                break
            chain.add(cursor)
            cursor = predecessors.get(cursor)
        visited.update(chain)
    return issues


def validate_task_structure(repo_root: Path, task_dir: Path) -> list[ValidationIssue]:
    """Return deterministic diagnostics without writing task, session or Git state."""
    issues: list[ValidationIssue] = []
    if _enabled(repo_root, issues):
        path = task_dir / FILE_TASK_JSON
        text = _read_text(path, issues)
        data: dict[str, object] | None = None
        if text is not None:
            try:
                data = _json_object(text)
            except (ValueError, RecursionError) as exc:
                lineno = exc.lineno if isinstance(exc, json.JSONDecodeError) else None
                issues.append(ValidationIssue(path, lineno, f"Invalid task JSON: {exc}", "Restore a JSON object with unique keys."))
        if data is not None:
            meta = data.get("meta")
            mode = meta.get("planning_mode") if isinstance(meta, dict) else None
            if not isinstance(meta, dict):
                issues.append(ValidationIssue(path, None, "Task meta must be an object.",
                                              "Set meta.planning_mode to lightweight or complex after reviewing task scope."))
            if mode not in ("lightweight", "complex"):
                issues.append(ValidationIssue(path, None, "Missing or invalid meta.planning_mode.",
                                              "Use task.py set-meta <task> planning_mode lightweight|complex; do not infer it from missing files."))
            layout = meta.get("planning_layout", "standard") if isinstance(meta, dict) else "standard"
            if layout not in ("standard", "compact"):
                issues.append(ValidationIssue(path, None, "Invalid meta.planning_layout.",
                                              "Use task.py set-meta <task> planning_layout standard|compact; omit it for standard."))
            if layout == "compact" and mode == "lightweight":
                issues.append(ValidationIssue(path, None, "Compact layout requires a complex task.",
                                              "Use standard layout for PRD-only lightweight work; do not change classification to bypass required content."))
            compact = mode == "complex" and layout == "compact"
            for filename, sections in _PLANNING_SECTIONS.items():
                document = task_dir / filename
                if compact and filename == "design.md":
                    sections = ("Scope", "Contracts", "Ordered Steps", "Validation")
                required = filename == "prd.md" or (mode == "complex" and (not compact or filename == "design.md"))
                if required or document.exists() or document.is_symlink():
                    content = _read_text(document, issues)
                    if content is not None:
                        issues.extend(_markdown_sections(content, document, sections))
            related = data.get("relatedFiles", [])
            if not isinstance(related, list) or any(not isinstance(entry, str) for entry in related):
                issues.append(ValidationIssue(path, None, "relatedFiles must be an array of strings.",
                                              "Register decision paths as strings; keep ordinary code paths unchanged."))
            else:
                issues.extend(_decisions(repo_root, related, path))
    return sorted(issues, key=lambda issue: (str(issue.path), issue.line or 0, issue.severity, issue.message))
