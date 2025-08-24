import csv

def list_high_score_games(file_path):
    """Lists games with a score of 5 from a CSV file."""
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            print("Games with a score of 5:")
            for row in reader:
                if row.get('score') == '5':
                    print(f"- {row.get('title')} ({row.get('year_played')})")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Path to the CSV file
games_file_path = 'data/games/games_beaten.csv'

# List high score games
list_high_score_games(games_file_path)
