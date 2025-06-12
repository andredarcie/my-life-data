import pandas as pd
from pathlib import Path

# Load the CSV data
csv_path = Path(__file__).resolve().parents[2] / 'data' / 'games' / 'games_beated.csv'

# Read the CSV, ignoring extra spaces
_df = pd.read_csv(csv_path, skipinitialspace=True)

# Fix possible swapped columns in the CSV
def _fix_row(row):
    year_str = str(row['year_I_played'])
    plat_str = str(row['plataform'])
    # If the year column does not contain a 4 digit year but platform does, swap
    if not year_str.isdigit() and plat_str.isdigit():
        row['year_I_played'], row['plataform'] = plat_str, year_str
    return row

_df = _df.apply(_fix_row, axis=1)

# Clean year_I_played column and ensure numeric type
_df['year_I_played'] = pd.to_numeric(_df['year_I_played'].astype(str).str.extract('(\d{4})')[0], errors='coerce')

# Parse beat_date column to datetime when possible
_df['beat_date_parsed'] = pd.to_datetime(_df['beat_date'], dayfirst=True, errors='coerce')

# Basic stats
num_games = len(_df)
unique_platforms = _df['plataform'].nunique()

# Games per platform
games_per_platform = _df['plataform'].value_counts().sort_values(ascending=False)

# Games per year played
games_per_year = _df['year_I_played'].value_counts().sort_index()

# Average score by platform
avg_score_platform = _df.groupby('plataform')['score'].mean().sort_values(ascending=False)

# Average score by year
avg_score_year = _df.groupby('year_I_played')['score'].mean().sort_index()

# Score distribution
score_counts = _df['score'].value_counts().sort_index()

# Highest scoring games (score 5)
highest_score_games = _df[_df['score'] == 5][['title','plataform','year_I_played']]

# Print results
print(f"Total games beat: {num_games}")
print(f"Unique platforms: {unique_platforms}")
print("\nGames per platform:\n" + games_per_platform.to_string())
print("\nGames per year played:\n" + games_per_year.to_string())
print("\nAverage score by platform:\n" + avg_score_platform.round(2).to_string())
print("\nAverage score by year:\n" + avg_score_year.round(2).to_string())
print("\nScore distribution:\n" + score_counts.to_string())
print("\nHighest scoring games (score = 5):")
print(highest_score_games.to_string(index=False))
