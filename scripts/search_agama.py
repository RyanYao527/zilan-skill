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


def search_agama(
    pattern: str = DEFAULT_PATTERN,
    *,
    root: Path = ROOT,
    limit: int = 20,
    context_lines: int = 0,
    include_false_positives: bool = False,
) -> list[AgamaMatch]:
    regex = re.compile(pattern)
    matches: list[AgamaMatch] = []

    for path in iter_agama_markdown_files(root):
        lines = path.read_text(encoding="utf-8").splitlines()
        juan_by_line = _line_juan_map(lines)
        for idx, line in enumerate(lines, start=1):
            if not regex.search(line):
                continue
            if not include_false_positives and is_false_positive(line):
                continue

            start = max(0, idx - context_lines - 1)
            end = min(len(lines), idx + context_lines)
            before = lines[start : idx - 1]
            after = lines[idx:end]
            matches.append(
                AgamaMatch(
                    file=path.relative_to(root).as_posix(),
                    line=idx,
                    juan=juan_by_line.get(idx),
                    text=line.strip(),
                    context_before=[item.strip() for item in before if item.strip()],
                    context_after=[item.strip() for item in after if item.strip()],
                )
            )
            if limit and len(matches) >= limit:
                return matches

    return matches


def _print_text(matches: list[AgamaMatch], pattern: str) -> None:
    print(f"Found {len(matches)} matches for /{pattern}/")
    for match in matches:
        juan = f" [{match.juan}]" if match.juan else ""
        print(f"{match.file}:{match.line}{juan} {match.text}")
        for line in match.context_before:
            print(f"  < {line}")
        for line in match.context_after:
            print(f"  > {line}")


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
        "--include-false-positives",
        action="store_true",
        help="Do not filter known keyword collisions.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args()

    matches = search_agama(
        args.terms,
        root=args.root.resolve(),
        limit=args.limit,
        context_lines=args.context,
        include_false_positives=args.include_false_positives,
    )
    if args.json:
        print(json.dumps([asdict(match) for match in matches], ensure_ascii=False, indent=2))
    else:
        _print_text(matches, args.terms)
    return 0 if matches else 1


if __name__ == "__main__":
    raise SystemExit(main())
