'''
Small game for teaching semi-functional-way in Python

Rules: two players, like Tic-Tac-Toe, but after three turns by each player
you can't make new marks and you may only move placed marks on neighbors cells.
Coordinates like "2 1" or "21", where 2 is row and 1 is column,
enumerated from zero.
'''

N = 3  # You can change it in [3..9]

O = 1
X = 2

state = tuple([tuple([0 for _ in range(N)]) for _ in range(N)])


def put(state, x, y, new):
    return (state[:x] +
               ((state[x][:y] + (new,) + state[x][y + 1:]),) +
               state[x + 1:])


def print_state(state):
    print(str(state).replace('((', '(').replace('))', ')')
          .replace('), ', ')\n')
          .replace('0', '.').replace('2', 'X')
          .replace('1', 'O').replace(', ', ' '))


def toggle(figure):
    return O if figure == X else X


def figure_to_str(figure):
    return 'O' if figure == O else 'X'


def count(state, target):
    return len(list(filter(lambda x: x == target, sum(state, ()))))


def get(state, x, y):
    return state[x][y]


def is_free(state, x, y):
    return is_exist(x, y) and get(state, x, y) == 0


def is_exist(x, y):
    return x in range(N) and y in range(N)


def get_neighbors(state, x, y):
    return filter(lambda c: is_exist(*c), [(x + dx, y + dy)
                  for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                  if not (dx == dy == 0)])


def get_free_neighbors(state, x, y):
    return tuple(filter(lambda c: is_free(state, *c),
                        get_neighbors(state, x, y)))


def move(state, fr, to):
    fig = get(state, *fr)
    return put(put(state, fr[0], fr[1], 0), to[0], to[1], fig)


def turn_again(state, figure):
    print('\nError, try again')
    turn(state, figure)


def input_tuple(str):
    t = input(str)
    return (int(t[0]), int(t[-1]),)


def check_row(state, row, figure):
    return all(map(lambda f: f == figure, [state[row][i] for i in range(N)]))


def check_col(state, col, figure):
    return all(map(lambda f: f == figure, [state[i][col] for i in range(N)]))


def check_diag(state, n, figure):
    return all(map(lambda f: f == figure,
               [state[x][x if n else N - x - 1] for x in range(N)]))


def check_winner(state, figure):
    return (any([check_col(state, col, figure) for col in range(N)]) or
            any([check_row(state, row, figure) for row in range(N)]) or
            any([check_diag(state, n, figure) for row in range(N)
                for n in range(2)]))


def turn(state, figure):
    print()
    print_state(state)
    if check_winner(state, toggle(figure)):
        print('Winner is ' + figure_to_str(toggle(figure)) + ' !')

    elif count(state, figure) < N:
        p = input_tuple('Your turn, ' + figure_to_str(figure) + ': ')
        if is_free(state, *p):
            turn(put(state, p[0], p[1], figure), toggle(figure))
        else:
            turn_again(state, figure)
    else:
        fr = input_tuple('Your turn, ' + figure_to_str(figure) + ', from: ')
        if get(state, *fr) == figure:
            print('Possible moves: ', get_free_neighbors(state, *fr))
            to = input_tuple('To: ')
            if to in get_free_neighbors(state, *fr):
                turn(move(state, fr, to), toggle(figure))
            else:
                turn_again(state, figure)
        else:
            turn_again(state, figure)


if __name__ == '__main__':
    turn(state, X)
