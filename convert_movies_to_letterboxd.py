import argparse
import csv
import random
import re
from datetime import date, timedelta
from pathlib import Path


DATE_YYYY_MM_DD = re.compile(r"(19|20)\d{2}-\d{2}-\d{2}")
DATE_YYYY_MM_DD_SLASH = re.compile(r"(19|20)\d{2}/\d{2}/\d{2}")


def norm_key(key: str) -> str:
    return key.strip().lower().replace(" ", "_")


def pick(row: dict, *keys: str) -> str:
    for key in keys:
        if key in row and row[key]:
            return row[key].strip()
    return ""


def normalize_list_field(value: str) -> str:
    if not value:
        return ""
    if ";" in value and "," not in value:
        return ", ".join([p.strip() for p in value.split(";") if p.strip()])
    return value.strip()


def extract_date(value: str) -> str:
    if not value:
        return ""
    value = value.strip()
    match = DATE_YYYY_MM_DD.search(value)
    if match:
        return match.group(0)
    match = DATE_YYYY_MM_DD_SLASH.search(value)
    if match:
        parts = match.group(0).split("/")
        return f"{parts[0]}-{parts[1]}-{parts[2]}"
    return ""


def watched_year_to_date(year_value: str, mode: str) -> str:
    if not year_value:
        return ""
    year_value = year_value.strip()
    if not year_value.isdigit() or len(year_value) != 4:
        return ""
    year = int(year_value)
    if mode == "blank":
        return ""
    if mode == "jan01":
        return date(year, 1, 1).isoformat()
    if mode == "jul01":
        return date(year, 7, 1).isoformat()
    if mode == "dec31":
        return date(year, 12, 31).isoformat()
    return ""


def assign_random_dates_by_year(rows: list, seed: int | None) -> None:
    rng = random.Random(seed)

    by_year: dict[int, list[dict]] = {}
    for row in rows:
        if row.get("WatchedDate"):
            continue
        year_value = (row.get("WatchedYear") or "").strip()
        if not year_value.isdigit() or len(year_value) != 4:
            continue
        year = int(year_value)
        by_year.setdefault(year, []).append(row)

    for year, items in by_year.items():
        start = date(year, 1, 1)
        days_in_year = (
            366 if date(year, 12, 31).toordinal() - start.toordinal() + 1 == 366 else 365
        )

        count = len(items)
        if count <= days_in_year:
            day_indexes = sorted(rng.sample(range(days_in_year), count))
        else:
            day_indexes = sorted(rng.randrange(days_in_year) for _ in range(count))

        for item, day_index in zip(items, day_indexes):
            day = start + timedelta(days=day_index)
            item["WatchedDate"] = day.isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Converte CSV de filmes para o formato de importacao do Letterboxd."
    )
    parser.add_argument(
        "-i",
        "--input",
        default="data/movies/movies_watched.csv",
        help="Caminho do CSV de entrada.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="data/movies/movies_watched_letterboxd.csv",
        help="Caminho do CSV de saida.",
    )
    parser.add_argument(
        "--watched-year-mode",
        choices=["blank", "jan01", "jul01", "dec31"],
        default="blank",
        help="Como converter watched_year para WatchedDate (padrao: blank).",
    )
    parser.add_argument(
        "--randomize-year-dates",
        action="store_true",
        help="Distribui datas aleatorias no ano quando houver apenas Year.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Seed para reproducao das datas aleatorias.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    with input_path.open("r", encoding="utf-8-sig", newline="") as f_in:
        reader = csv.DictReader(f_in)
        if not reader.fieldnames:
            raise SystemExit("CSV de entrada sem cabecalho.")

        normalized_rows = []
        field_map = {norm_key(k): k for k in reader.fieldnames}

        for row in reader:
            normalized_rows.append(
                {norm_key(k): (v or "").strip() for k, v in row.items()}
            )

    output_rows = []
    for row in normalized_rows:
        title = pick(row, "title", "name")
        year = pick(row, "year", "release_year")
        directors = normalize_list_field(pick(row, "director", "directors"))
        watched_date = extract_date(
            pick(row, "watched_date", "watched_on", "date_watched", "watched")
        )
        if not watched_date:
            watched_date = watched_year_to_date(
                pick(row, "watched_year"), args.watched_year_mode
            )
        rating = pick(row, "rating", "rating_5")
        rating10 = pick(row, "rating10", "rating_10")
        tags = normalize_list_field(pick(row, "tags", "tag"))
        review = pick(row, "review", "review_text")

        output_rows.append(
            {
                "Title": title,
                "Year": year,
                "Directors": directors,
                "WatchedDate": watched_date,
                "WatchedYear": pick(row, "watched_year"),
                "Rating": rating,
                "Rating10": rating10,
                "Tags": tags,
                "Review": review,
            }
        )

    if args.randomize_year_dates:
        assign_random_dates_by_year(output_rows, args.seed)

    # Drop entirely empty columns to keep the output clean.
    non_empty_columns = []
    for column in [
        "Title",
        "Year",
        "Directors",
        "WatchedDate",
        "Rating",
        "Rating10",
        "Tags",
        "Review",
        "WatchedYear",
    ]:
        if any(row.get(column) for row in output_rows):
            non_empty_columns.append(column)

    # WatchedYear is only an internal helper; drop it from output.
    if "WatchedYear" in non_empty_columns:
        non_empty_columns.remove("WatchedYear")

    with output_path.open("w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=non_empty_columns)
        writer.writeheader()
        for row in output_rows:
            writer.writerow({k: row.get(k, "") for k in non_empty_columns})

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
