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
        input()
    elif option == '2':
        print('What do you want to show?')
        input()
    elif option == '3':
        break
    else:
        print('Invalid option please try again...')
        input()