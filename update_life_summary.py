from __future__ import annotations

import argparse
import csv
import difflib
import sys
from dataclasses import dataclass
from pathlib import Path


MARKER_START = "<!-- activity-summary-start -->"
MARKER_END = "<!-- activity-summary-end -->"


@dataclass(frozen=True)
class Dataset:
    label: str
    path: Path


def load_datasets(repo_root: Path) -> list[Dataset]:
    data = [
        ("Games beaten", repo_root / "data" / "games" / "games_beaten.csv"),
        ("Games abandoned", repo_root / "data" / "games" / "games_abandoned.csv"),
        ("Movies watched", repo_root / "data" / "movies" / "movies_watched.csv"),
        ("Movies to watch", repo_root / "data" / "movies" / "movies_to_watch.csv"),
        ("Documentaries watched", repo_root / "data" / "documentaries" / "documentaries_watched.csv"),
        ("Series watched", repo_root / "data" / "tv-series" / "series_watched.csv"),
        ("Books read", repo_root / "data" / "books" / "books_read.csv"),
        ("Books to read", repo_root / "data" / "books" / "to_read.csv"),
        ("Wine experiences", repo_root / "data" / "wine" / "wine_experiences.csv"),
    ]
    return [Dataset(label, path) for label, path in data]


def count_rows(dataset: Dataset) -> int:
    if not dataset.path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset.path}")

    # Some files contain non-UTF8 characters; fall back gracefully if needed.
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            with dataset.path.open("r", newline="", encoding=encoding) as handle:
                reader = csv.reader(handle)
                # Skip header if present.
                next(reader, None)
                return sum(1 for row in reader if any(cell.strip() for cell in row))
        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError(
        "Unable to decode file", str(dataset.path), 0, 0, "Unknown encoding"
    )


def build_summary(datasets: list[Dataset]) -> list[str]:
    summary_lines = []
    for dataset in datasets:
        total = count_rows(dataset)
        summary_lines.append(f"- {dataset.label}: {total}")
    return summary_lines


def render_summary_block(summary_lines: list[str]) -> str:
    return "\n".join([MARKER_START, *summary_lines, MARKER_END])


def extract_summary_block(content: str) -> str:
    if MARKER_START not in content or MARKER_END not in content:
        raise ValueError("Activity summary markers not found in README.md.")

    start_index = content.index(MARKER_START)
    end_index = content.index(MARKER_END) + len(MARKER_END)
    return content[start_index:end_index]


def update_readme(repo_root: Path, summary_lines: list[str]) -> None:
    readme_path = repo_root / "README.md"
    if not readme_path.exists():
        raise FileNotFoundError("README.md not found in repository root.")

    content = readme_path.read_text(encoding="utf-8")
    summary_block = render_summary_block(summary_lines)

    if MARKER_START in content and MARKER_END in content:
        start_index = content.index(MARKER_START)
        end_index = content.index(MARKER_END) + len(MARKER_END)
        new_content = content[:start_index] + summary_block + content[end_index:]
    else:
        append_block = f"\n\n## Activity Summary\n\n{summary_block}\n"
        new_content = content.rstrip() + append_block

    readme_path.write_text(new_content + ("\n" if not new_content.endswith("\n") else ""), encoding="utf-8")


def validate_readme(repo_root: Path, summary_lines: list[str]) -> None:
    readme_path = repo_root / "README.md"
    if not readme_path.exists():
        raise FileNotFoundError("README.md not found in repository root.")

    content = readme_path.read_text(encoding="utf-8")
    try:
        current_block = extract_summary_block(content)
    except ValueError as exc:
        raise RuntimeError(f"{exc} Run 'python update_life_summary.py' to create the section.") from exc

    expected_block = render_summary_block(summary_lines)
    normalized_current = current_block.replace("\r\n", "\n")
    normalized_expected = expected_block.replace("\r\n", "\n")

    if normalized_current != normalized_expected:
        diff = "\n".join(
            difflib.unified_diff(
                normalized_current.splitlines(),
                normalized_expected.splitlines(),
                fromfile="README.md (current)",
                tofile="README.md (expected)",
                lineterm="",
            )
        )
        message = [
            "Activity summary section is outdated.",
            "Run 'python update_life_summary.py' locally and commit the updated README.md.",
        ]
        if diff:
            message.append(diff)
        raise RuntimeError("\n".join(message))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update or validate the activity summary in README.md.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the activity summary without modifying README.md. "
        "Exits with status 1 if the summary is stale.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(__file__).resolve().parent
    datasets = load_datasets(repo_root)
    summary_lines = build_summary(datasets)
    if args.check:
        validate_readme(repo_root, summary_lines)
    else:
        update_readme(repo_root, summary_lines)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1) from error
