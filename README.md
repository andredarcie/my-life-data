# My Life Data

This repository organizes personal data about movies, books, games and more. It is structured so that notebooks, raw data and documentation live in separate folders.

## Repository layout

- `src/` – Python scripts (e.g. `movie_stats.py`)
- `data/` – CSV and other raw data files
- `analysis/` – Jupyter notebooks for exploring the data
- `docs/` – Markdown notes and other documentation
- `tools/` – helper utilities such as `docker-compose.yml`

## Categories

### 🎬 Movies
- [To Watch](data/movies/movies_to_watch.csv)
- [Watched](data/movies/movies_watched.csv)
- [Documentaries Watched](data/documentaries/documentaries_watched.csv)

### 📺 TV Shows
- [Watched](data/tv-series/series_watched.csv)

### 📖 Books
- [My books](data/books/my-books.md)

### 🎮 Video Games
- [To Play](data/games/games_to_play.csv)
- [Beated](data/games/games_beated.csv)
- [Abandoned](data/games/games_abandoned.csv)
- [Most Played](data/games/most_played_games.csv)
- [Devices](data/games/devices.csv)

### 📅 Events
- [To Watch](data/events/events_to_watch.csv)

### 🚀 Tourism
- [Places I went](data/tourism/places_i_went.csv)

### 💡 Study
Documentation lives under [docs/](docs/)

### 🍷 Wine
- [Wine Experiences](data/wine/wine_experiences.csv)

## Development

Create a Python environment and install requirements:

```bash
pip install -r requirements.txt
```

To generate simple movie statistics run:

```bash
python src/movie_stats.py
```

Jupyter notebooks inside `analysis/` can be launched with Docker Compose:

```bash
cd tools && docker-compose up
```
