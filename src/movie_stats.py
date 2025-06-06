import csv
from collections import Counter

file_path = 'data/movies/movies_watched.csv'

def main():
    directors = Counter()
    years = Counter()
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                director = row.get('director') or row.get('Director')
                year = row.get('year_watched') or row.get('Year')
                if director:
                    directors[director.strip()] += 1
                if year:
                    years[year.strip()] += 1
    except Exception as e:
        print(f'Erro ao ler o arquivo: {e}')
        return

    print('Contagem de diretores:')
    for director, count in directors.most_common():
        print(f'{director}: {count}')

    print('\nAnos em que mais assisti filmes:')
    for year, count in years.most_common():
        print(f'{year}: {count}')

if __name__ == '__main__':
    main()
