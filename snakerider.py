import curses  # Terminal handling for character-cell displays
from random import randint

curses.initscr()
win = curses.newwin(20, 40, 0, 0)
win.keypad(True)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(True)

snake = [[4, 7], [4, 6], [4, 5]]
food = [6, 18]
win.addch(food[0], food[1], '*')

key = curses.KEY_RIGHT
score = 0


def is_opposite(dir1, dir2):
    return (
        (dir1 == curses.KEY_UP and dir2 == curses.KEY_DOWN) or
        (dir1 == curses.KEY_DOWN and dir2 == curses.KEY_UP) or
        (dir1 == curses.KEY_LEFT and dir2 == curses.KEY_RIGHT) or
        (dir1 == curses.KEY_RIGHT and dir2 == curses.KEY_LEFT)
    )


valid_keys = [curses.KEY_UP, curses.KEY_DOWN,
              curses.KEY_LEFT, curses.KEY_RIGHT]

while True:
    win.border(0)

    score_y, score_x = 1, 2
    score_text = f"Score: {score}"
    occupied_positions = [food] + snake
    score_positions = [[score_y, score_x + i] for i in range(len(score_text))]

    if not any(pos in occupied_positions for pos in score_positions):
        win.addstr(score_y, score_x, score_text)

    win.timeout(150 - (len(snake)) // 5 + len(snake) // 10 % 120)

    next_key = win.getch()

    if next_key in valid_keys and not is_opposite(key, next_key):
        key = next_key
    elif next_key == 27:
        break

    y = snake[0][0]
    x = snake[0][1]

    if key == curses.KEY_DOWN:
        y += 1
    elif key == curses.KEY_UP:
        y -= 1
    elif key == curses.KEY_LEFT:
        x -= 1
    elif key == curses.KEY_RIGHT:
        x += 1

    new_head = [y, x]

    if y == 0 or y == 19 or x == 0 or x == 39 or new_head in snake:
        break

    snake.insert(0, new_head)

    if snake[0] == food:
        score += 1
        food = None
        while food is None:
            nf = [randint(1, 18), randint(1, 38)]
            food = nf if nf not in snake else None
        win.addch(food[0], food[1], '*')
    else:
        tail = snake.pop()
        win.addch(tail[0], tail[1], ' ')

    win.addch(snake[0][0], snake[0][1], '#')

curses.endwin()
print(f'Game Over! Your final score was {score}')
