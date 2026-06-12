from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGAMA_DIR = ROOT / "context" / "agama"

DEFAULT_PATTERN = (
    "無我|非我|無我所|五陰|五受陰|緣起|空無我|諸法無我|色無我|苦無我想"
)

# These phrases are common keyword collisions rather than doctrinal anatta hits.
DEFAULT_FALSE_POSITIVE_PHRASES = (
    "非我宜",
    "非我所說",
)


@dataclass(frozen=True)
class AgamaMatch:
    file: str
    line: int
    juan: str | None
    passage_start_line: int
    passage_end_line: int
    text: str
    context_before: list[str]
    context_after: list[str]


@dataclass(frozen=True)
class AgamaPassage:
    file: str
    juan: str | None
    start_line: int
    end_line: int
    matched_lines: list[int]
    text: str
    context_before: list[str]
    context_after: list[str]


def iter_agama_markdown_files(root: Path = ROOT) -> Iterable[Path]:
    agama_dir = root / "context" / "agama"
    for path in sorted(agama_dir.glob("*.md")):
        if path.name == "agama-index.md":
            continue
        if "_source" in path.parts:
            continue
        yield path


def is_false_positive(line: str, phrases: Iterable[str] = DEFAULT_FALSE_POSITIVE_PHRASES) -> bool:
    return any(phrase in line for phrase in phrases)


def _line_juan_map(lines: list[str]) -> dict[int, str | None]:
    current: str | None = None
    result: dict[int, str | None] = {}
    for idx, line in enumerate(lines, start=1):
        heading = re.match(r"^##\s+(卷\s+\S+)\s*$", line)
        if heading:
            current = heading.group(1)
        result[idx] = current
    return result


def _paragraph_bounds(lines: list[str], line_number: int) -> tuple[int, int]:
    index = line_number - 1
    start = index
    while start > 0 and lines[start - 1].strip():
        start -= 1

    end = index
    while end + 1 < len(lines) and lines[end + 1].strip():
        end += 1

    return start + 1, end + 1


def _context(lines: list[str], start_line: int, end_line: int, context_lines: int) -> tuple[list[str], list[str]]:
    before_start = max(0, start_line - context_lines - 1)
    before_end = start_line - 1
    after_start = end_line
    after_end = min(len(lines), end_line + context_lines)
    before = [item.strip() for item in lines[before_start:before_end] if item.strip()]
    after = [item.strip() for item in lines[after_start:after_end] if item.strip()]
    return before, after


def search_agama(
    pattern: str = DEFAULT_PATTERN,
    *,
    root: Path = ROOT,
    limit: int = 20,
    context_lines: int = 0,
    include_false_positives: bool = False,
    false_positive_phrases: Iterable[str] = DEFAULT_FALSE_POSITIVE_PHRASES,
) -> list[AgamaMatch]:
    regex = re.compile(pattern)
    matches: list[AgamaMatch] = []

    for path in iter_agama_markdown_files(root):
        lines = path.read_text(encoding="utf-8").splitlines()
        juan_by_line = _line_juan_map(lines)
        for idx, line in enumerate(lines, start=1):
            if not regex.search(line):
                continue
            if not include_false_positives and is_false_positive(line, false_positive_phrases):
                continue

            passage_start, passage_end = _paragraph_bounds(lines, idx)
            before, after = _context(lines, idx, idx, context_lines)
            matches.append(
                AgamaMatch(
                    file=path.relative_to(root).as_posix(),
                    line=idx,
                    juan=juan_by_line.get(idx),
                    passage_start_line=passage_start,
                    passage_end_line=passage_end,
                    text=line.strip(),
                    context_before=before,
                    context_after=after,
                )
            )
            if limit and len(matches) >= limit:
                return matches

    return matches


def search_agama_passages(
    pattern: str = DEFAULT_PATTERN,
    *,
    root: Path = ROOT,
    limit: int = 20,
    context_lines: int = 0,
    include_false_positives: bool = False,
    false_positive_phrases: Iterable[str] = DEFAULT_FALSE_POSITIVE_PHRASES,
) -> list[AgamaPassage]:
    matches = search_agama(
        pattern,
        root=root,
        limit=0,
        context_lines=0,
        include_false_positives=include_false_positives,
        false_positive_phrases=false_positive_phrases,
    )
    passages_by_key: dict[tuple[str, int, int], list[AgamaMatch]] = {}
    for match in matches:
        key = (match.file, match.passage_start_line, match.passage_end_line)
        passages_by_key.setdefault(key, []).append(match)

    passages: list[AgamaPassage] = []
    for (file, start_line, end_line), passage_matches in passages_by_key.items():
        path = root / file
        lines = path.read_text(encoding="utf-8").splitlines()
        text = "\n".join(line.strip() for line in lines[start_line - 1 : end_line] if line.strip())
        before, after = _context(lines, start_line, end_line, context_lines)
        passages.append(
            AgamaPassage(
                file=file,
                juan=passage_matches[0].juan,
                start_line=start_line,
                end_line=end_line,
                matched_lines=[match.line for match in passage_matches],
                text=text,
                context_before=before,
                context_after=after,
            )
        )
        if limit and len(passages) >= limit:
            return passages

    return passages


def _group_label(item: AgamaMatch | AgamaPassage, group_by: str) -> str | None:
    if group_by == "file":
        return item.file
    if group_by == "juan":
        juan = item.juan or "卷未标注"
        return f"{item.file} [{juan}]"
    return None


def _print_match(match: AgamaMatch) -> None:
    juan = f" [{match.juan}]" if match.juan else ""
    print(f"{match.file}:{match.line}{juan} {match.text}")
    for line in match.context_before:
        print(f"  < {line}")
    for line in match.context_after:
        print(f"  > {line}")


def _print_passage(passage: AgamaPassage) -> None:
    juan = f" [{passage.juan}]" if passage.juan else ""
    matched = ",".join(str(line) for line in passage.matched_lines)
    print(f"{passage.file}:{passage.start_line}-{passage.end_line}{juan} matches={matched}")
    for line in passage.context_before:
        print(f"  < {line}")
    for line in passage.text.splitlines():
        print(f"  | {line}")
    for line in passage.context_after:
        print(f"  > {line}")


def _print_items(items: list[AgamaMatch] | list[AgamaPassage], pattern: str, group_by: str) -> None:
    print(f"Found {len(items)} matches for /{pattern}/")
    current_group: str | None = None
    for item in items:
        group = _group_label(item, group_by)
        if group and group != current_group:
            current_group = group
            print(f"\n## {group}")
        if isinstance(item, AgamaPassage):
            _print_passage(item)
        else:
            _print_match(item)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Search the local Agama Markdown corpus with source XML excluded by default."
    )
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    parser.add_argument("--terms", default=DEFAULT_PATTERN, help="Regex pattern to search.")
    parser.add_argument("--limit", type=int, default=20, help="Maximum matches; 0 means no limit.")
    parser.add_argument("--context", type=int, default=0, help="Context lines before and after.")
    parser.add_argument(
        "--group-by",
        choices=("none", "file", "juan"),
        default="none",
        help="Group text output by file or file+juan.",
    )
    parser.add_argument(
        "--passages",
        action="store_true",
        help="Aggregate matches by paragraph-like Markdown passage.",
    )
    parser.add_argument(
        "--include-false-positives",
        action="store_true",
        help="Do not filter known keyword collisions.",
    )
    parser.add_argument(
        "--false-positive-phrase",
        action="append",
        default=[],
        help="Additional phrase to filter from matching lines. Can be passed more than once.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args()

    false_positive_phrases = (*DEFAULT_FALSE_POSITIVE_PHRASES, *args.false_positive_phrase)
    search_fn = search_agama_passages if args.passages else search_agama
    matches = search_fn(
        args.terms,
        root=args.root.resolve(),
        limit=args.limit,
        context_lines=args.context,
        include_false_positives=args.include_false_positives,
        false_positive_phrases=false_positive_phrases,
    )
    if args.json:
        print(json.dumps([asdict(match) for match in matches], ensure_ascii=False, indent=2))
    else:
        _print_items(matches, args.terms, args.group_by)
    return 0 if matches else 1


if __name__ == "__main__":
    raise SystemExit(main())
