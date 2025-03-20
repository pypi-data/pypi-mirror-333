import curses
import random
import time
import locale

# Set locale for proper Unicode support in the terminal
locale.setlocale(locale.LC_ALL, '')

def create_food(snake, sh, sw):
    """
    Generate a new food position that does not conflict with the snake's body.

    Parameters:
        snake (list): List of [y, x] positions representing the snake.
        sh (int): Screen height.
        sw (int): Screen width.

    Returns:
        list: [y, x] coordinates for the food.
    """
    while True:
        food = [random.randint(1, sh - 2), random.randint(1, sw - 2)]
        if food not in snake:
            return food

def process_input(win, current_direction):
    """
    Process keyboard input to update the snake's direction.

    Supports arrow keys and WASD. The snake's movement is continuous,
    and the key press only changes its direction. Reverse movement is prevented.

    Parameters:
        win (curses.window): The game window.
        current_direction (int): The current movement direction.

    Returns:
        int: The new direction.
    """
    key = win.getch()
    
    # Map WASD to arrow keys for direction control
    if key in [ord('w'), ord('W')]:
        key = curses.KEY_UP
    elif key in [ord('s'), ord('S')]:
        key = curses.KEY_DOWN
    elif key in [ord('a'), ord('A')]:
        key = curses.KEY_LEFT
    elif key in [ord('d'), ord('D')]:
        key = curses.KEY_RIGHT

    # Prevent reversing direction directly
    if key == curses.KEY_UP and current_direction != curses.KEY_DOWN:
        return curses.KEY_UP
    elif key == curses.KEY_DOWN and current_direction != curses.KEY_UP:
        return curses.KEY_DOWN
    elif key == curses.KEY_LEFT and current_direction != curses.KEY_RIGHT:
        return curses.KEY_LEFT
    elif key == curses.KEY_RIGHT and current_direction != curses.KEY_LEFT:
        return curses.KEY_RIGHT

    return current_direction

def update_snake(snake, direction, sh, sw, food, score):
    """
    Update the snake's position based on the current direction.

    Moves the snake's head, checks for border and self collisions,
    and handles food consumption by increasing score and growing the snake.

    Parameters:
        snake (list): List of snake segments.
        direction (int): Current movement direction.
        sh (int): Screen height.
        sw (int): Screen width.
        food (list): Food position.
        score (int): Current score.

    Returns:
        tuple: (snake, food, score, game_over)
            snake (list): Updated snake segments.
            food (list): New food position if consumed.
            score (int): Updated score.
            game_over (bool): True if a collision occurred.
    """
    head = snake[0].copy()
    if direction == curses.KEY_UP:
        head[0] -= 1
    elif direction == curses.KEY_DOWN:
        head[0] += 1
    elif direction == curses.KEY_LEFT:
        head[1] -= 1
    elif direction == curses.KEY_RIGHT:
        head[1] += 1

    # Check border collisions
    if head[0] <= 0 or head[0] >= sh - 1 or head[1] <= 0 or head[1] >= sw - 1:
        return snake, food, score, True

    # Check self collision
    if head in snake:
        return snake, food, score, True

    snake.insert(0, head)
    if head == food:
        score += 1
        food = create_food(snake, sh, sw)
    else:
        snake.pop()  # Remove tail if no food consumed

    return snake, food, score, False

def render(win, snake, food, score, sh, sw):
    """
    Render the game screen with borders, score, snake, and food.

    Uses ANSI colors (via curses color pairs) for a visually appealing interface.
    The snake head is drawn with "◉" and the body with "●", while the food is "★".

    Parameters:
        win (curses.window): The game window.
        snake (list): List of snake segments.
        food (list): Food position.
        score (int): Current score.
        sh (int): Screen height.
        sw (int): Screen width.
    """
    win.clear()
    win.border(0)
    
    # Display score and game instructions
    win.addstr(0, 2, f'Score: {score}', curses.color_pair(3))
    win.addstr(0, sw // 2 - 15, ' Snake Game - Use Arrow Keys or WASD ', curses.color_pair(3))
    
    # Draw the food with a fancy Unicode symbol
    win.addch(food[0], food[1], '★', curses.color_pair(2))
    
    # Draw the snake: head and body with enhanced appearance
    for idx, segment in enumerate(snake):
        if idx == 0:
            win.addch(segment[0], segment[1], '◉', curses.color_pair(1))
        else:
            win.addch(segment[0], segment[1], '●', curses.color_pair(1))
    
    win.refresh()

def game_over_screen(win, score, sh, sw):
    """
    Display the game over screen with the final score and exit instructions.

    Parameters:
        win (curses.window): The game window.
        score (int): Final score.
        sh (int): Screen height.
        sw (int): Screen width.
    """
    win.clear()
    win.border(0)
    message = " GAME OVER "
    win.addstr(sh // 2, (sw - len(message)) // 2, message, curses.color_pair(3))
    score_msg = f" Final Score: {score} "
    win.addstr(sh // 2 + 1, (sw - len(score_msg)) // 2, score_msg, curses.color_pair(3))
    win.addstr(sh // 2 + 3, (sw - 30) // 2, " Press any key to exit ", curses.color_pair(3))
    win.refresh()
    win.nodelay(False)
    win.getch()

def main(stdscr):
    """
    Main function to initialize and run the Snake game.

    Configures the curses environment, sets initial game variables,
    and runs the game loop until a collision occurs.
    """
    curses.curs_set(0)          # Hide the cursor
    stdscr.nodelay(True)        # Non-blocking input
    stdscr.timeout(100)         # Refresh timeout in milliseconds

    # Initialize color pairs for ANSI styling
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Snake color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # Food color
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Border and text color

    sh, sw = stdscr.getmaxyx()
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(True)
    win.nodelay(True)
    win.timeout(100)

    # Set initial snake state at screen center
    snake = [
        [sh // 2, sw // 2 + 1],
        [sh // 2, sw // 2],
        [sh // 2, sw // 2 - 1]
    ]
    direction = curses.KEY_RIGHT
    food = create_food(snake, sh, sw)
    score = 0

    # Main game loop: continuously update and render game state
    while True:
        direction = process_input(win, direction)
        snake, food, score, game_over = update_snake(snake, direction, sh, sw, food, score)
        if game_over:
            break
        render(win, snake, food, score, sh, sw)
        time.sleep(0.1)

    game_over_screen(win, score, sh, sw)

def init():
    """
    Entry point for initializing and running the Snake game.

    Uses curses.wrapper to ensure proper initialization and cleanup of the curses environment.
    """
    curses.wrapper(main)