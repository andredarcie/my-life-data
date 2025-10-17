from __future__ import annotations

import csv
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


def update_readme(repo_root: Path, summary_lines: list[str]) -> None:
    readme_path = repo_root / "README.md"
    if not readme_path.exists():
        raise FileNotFoundError("README.md not found in repository root.")

    content = readme_path.read_text(encoding="utf-8")
    summary_block = "\n".join([MARKER_START, *summary_lines, MARKER_END])

    if MARKER_START in content and MARKER_END in content:
        start_index = content.index(MARKER_START)
        end_index = content.index(MARKER_END) + len(MARKER_END)
        new_content = content[:start_index] + summary_block + content[end_index:]
    else:
        append_block = f"\n\n## Activity Summary\n\n{summary_block}\n"
        new_content = content.rstrip() + append_block

    readme_path.write_text(new_content + ("\n" if not new_content.endswith("\n") else ""), encoding="utf-8")


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    datasets = load_datasets(repo_root)
    summary_lines = build_summary(datasets)
    update_readme(repo_root, summary_lines)


if __name__ == "__main__":
    main()
