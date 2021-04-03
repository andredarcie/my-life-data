import csv
from imdb import IMDb

ia = IMDb()

def choose_your_entertainment():
    print('''
    [1] - Books
    [2] - Documentaries
    [3] - Tv Shows
    [4] - Movies
    [5] - Talks
    [6] - Video Games
    ''')

    return input('-> ')

def start():
    while True:
        print('''\033[92m My Tracker \033[0m
        A tiny command-line utility for entertainment tracker
        Options:
        [1] - Add
        [2] - Show
        [3] - Exit''')

        option = input('-> ')
        if option == '1':
            print('What do you want to add?')
            choose_your_entertainment()
        elif option == '2':
            print('What do you want to show?')
            input()
        elif option == '3':
            break
        else:
            print('Invalid option please try again...')
            input()
            

def get_movie_director_by_title(title):
    movies = ia.search_movie(title)
    movie = ia.get_movie(movies[0].movieID)

    try: 
        return movie['directors'][0]
    except:
        return 'not found'