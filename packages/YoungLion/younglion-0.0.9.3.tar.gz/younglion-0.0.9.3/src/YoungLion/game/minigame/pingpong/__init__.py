import curses
import time
import random

# Global configuration constants
PADDLE_HEIGHT = 4       # Height of each paddle in characters
PADDLE_CHAR = '|'       # Character used to draw a paddle
BALL_CHAR = 'O'         # Character used to draw the ball
FRAME_DELAY = 0.1      # Delay (in seconds) between each frame (controls game speed)

def init(ai_enabled=True):
    """
    Initializes and starts the Ping Pong game.

    Parameters:
        ai_enabled (bool): If True, the right paddle is controlled by the advanced AI.
                           If False, both paddles can be controlled via keyboard.

    This function sets up the curses environment, initializes ANSI colors,
    creates the main game window with a border, and starts the game loop.
    It initializes game objects (paddles, ball, score) and processes user input.
    For the AI-controlled paddle, the advanced prediction algorithm is used.
    """
    # Initialize curses screen and settings
    screen = curses.initscr()
    curses.cbreak()             # React to keys immediately without requiring Enter
    curses.noecho()             # Do not echo key presses on the screen
    screen.keypad(True)         # Enable special keys (e.g., arrow keys)
    curses.curs_set(0)          # Hide the cursor

    # Initialize colors if supported
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Paddle color
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Ball color
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Score and text color

    # Get terminal dimensions and create a new game window with a border
    height, width = screen.getmaxyx()
    win = curses.newwin(height, width, 0, 0)
    win.nodelay(True)  # Make getch() non-blocking
    win.timeout(int(FRAME_DELAY * 1000))  # Set the refresh rate in milliseconds

    # Initialize paddle positions: vertically centered
    left_paddle_y = height // 2 - PADDLE_HEIGHT // 2
    right_paddle_y = height // 2 - PADDLE_HEIGHT // 2
    left_paddle_x = 2             # X-position for the left paddle (from the left edge)
    right_paddle_x = width - 3    # X-position for the right paddle (from the right edge)

    # Initialize ball in the center with random direction for both axes
    ball_y = height // 2
    ball_x = width // 2
    ball_dir_y = random.choice([-1, 1])
    ball_dir_x = random.choice([-1, 1])

    # Initialize scores for both players
    score_left = 0
    score_right = 0

    # Main game loop
    try:
        while True:
            win.clear()         # Clear the screen for redrawing
            win.border()        # Draw border around the game window

            # Draw paddles and ball
            draw_paddle(win, left_paddle_y, left_paddle_x, PADDLE_HEIGHT)
            draw_paddle(win, right_paddle_y, right_paddle_x, PADDLE_HEIGHT)
            draw_ball(win, ball_y, ball_x)

            # Display score at the top center
            score_text = f"{score_left} : {score_right}"
            win.addstr(1, width // 2 - len(score_text) // 2, score_text, curses.color_pair(3))

            # Display instructions (only if AI is enabled, since only left paddle is user-controlled)
            instructions = "Press 'w'/'s' to move left paddle, 'q' to quit."
            win.addstr(height - 2, width // 2 - len(instructions) // 2, instructions, curses.color_pair(3))

            win.refresh()  # Refresh window to display changes

            # Handle user input for left paddle and quitting the game
            key = win.getch()
            if key == ord('q'):
                break  # Exit game loop if 'q' is pressed
            elif key in [ord('w'),ord("W")]:
                left_paddle_y = max(1, left_paddle_y - 1)
            elif key in [ord('s'),ord("S")]:
                left_paddle_y = min(height - PADDLE_HEIGHT - 1, left_paddle_y + 1)
            if key == curses.KEY_UP:
                left_paddle_y = max(1, left_paddle_y - 1)
            elif key == curses.KEY_DOWN:
                left_paddle_y = min(height - PADDLE_HEIGHT - 1, left_paddle_y + 1)
                    
            # If AI is disabled, allow manual control of right paddle using arrow keys.
            if not ai_enabled:
                if key == curses.KEY_UP:
                    right_paddle_y = max(1, right_paddle_y - 1)
                elif key == curses.KEY_DOWN:
                    right_paddle_y = min(height - PADDLE_HEIGHT - 1, right_paddle_y + 1)
            else:
                # Advanced AI control for the right paddle
                right_paddle_y = ai_move(right_paddle_y, ball_y, ball_dir_y, ball_x, ball_dir_x,
                                          right_paddle_x, height)

            # Update the ball's position based on its direction
            ball_y += ball_dir_y
            ball_x += ball_dir_x

            # Check collision with top and bottom walls, reverse vertical direction if needed
            if ball_y <= 1 or ball_y >= height - 2:
                ball_dir_y *= -1

            # Check collision with left paddle: if ball is adjacent and within paddle's vertical span
            if (ball_x == left_paddle_x + 1 and left_paddle_y <= ball_y < left_paddle_y + PADDLE_HEIGHT):
                ball_dir_x *= -1
            # Check collision with right paddle
            elif (ball_x == right_paddle_x - 1 and right_paddle_y <= ball_y < right_paddle_y + PADDLE_HEIGHT):
                ball_dir_x *= -1

            # Check if the ball goes out of bounds and update scores accordingly
            if ball_x <= 0:
                score_right += 1
                ball_y = height // 2
                ball_x = width // 2
                ball_dir_x = 1   # Serve towards left paddle next
                ball_dir_y = random.choice([-1, 1])
            elif ball_x >= width - 1:
                score_left += 1
                ball_y = height // 2
                ball_x = width // 2
                ball_dir_x = -1  # Serve towards right paddle next
                ball_dir_y = random.choice([-1, 1])

            # Control the frame rate of the game
            time.sleep(FRAME_DELAY)
    finally:
        # Restore terminal settings on exit
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()


def draw_paddle(win, start_y, start_x, height):
    """
    Draws a vertical paddle at a given position.

    Parameters:
        win (curses.window): The window in which to draw the paddle.
        start_y (int): The starting row for the paddle.
        start_x (int): The column where the paddle is drawn.
        height (int): The number of characters tall the paddle is.

    The paddle is drawn using the designated character and colored via an ANSI color pair.
    """
    for i in range(height):
        win.addch(start_y + i, start_x, PADDLE_CHAR, curses.color_pair(1))


def draw_ball(win, y, x):
    """
    Draws the ball at the specified coordinates.

    Parameters:
        win (curses.window): The window in which to draw the ball.
        y (int): The row for the ball.
        x (int): The column for the ball.

    The ball is represented by a character and colored using an ANSI color pair.
    """
    win.addch(y, x, BALL_CHAR, curses.color_pair(2))


def predict_ball_y(ball_y, ball_dir_y, ball_x, ball_dir_x, target_x, height):
    """
    Predicts the future y-coordinate of the ball when it reaches a specified x-coordinate.

    Parameters:
        ball_y (int): The current y-coordinate of the ball.
        ball_dir_y (int): The current vertical direction of the ball (+1 or -1).
        ball_x (int): The current x-coordinate of the ball.
        ball_dir_x (int): The horizontal direction of the ball (+1 or -1).
        target_x (int): The x-coordinate at which we want to predict the ball's y-coordinate.
        height (int): The height of the game window.

    Returns:
        int: The predicted y-coordinate of the ball when it reaches target_x.
    
    The function simulates the ball's movement (including bounces off the top and bottom walls)
    until the ball's x-coordinate equals or exceeds target_x.
    """
    # If ball is moving away from the target, return center as a default
    if (ball_dir_x > 0 and target_x < ball_x) or (ball_dir_x < 0 and target_x > ball_x):
        return height // 2

    sim_x = ball_x
    sim_y = ball_y
    sim_dy = ball_dir_y

    # Continue simulation until the ball reaches the target x-coordinate
    while (ball_dir_x > 0 and sim_x < target_x) or (ball_dir_x < 0 and sim_x > target_x):
        sim_x += ball_dir_x
        sim_y += sim_dy
        # Bounce off the top or bottom wall (keeping in mind the border)
        if sim_y <= 1 or sim_y >= height - 2:
            sim_dy *= -1
            sim_y += sim_dy  # Adjust position after bounce
    return sim_y


def ai_move(current_paddle_y, ball_y, ball_dir_y, ball_x, ball_dir_x, paddle_x, height):
    """
    Moves the AI-controlled paddle towards the predicted position of the ball using a PID controller.
    
    This advanced AI function utilizes a PID controller that continuously adjusts the paddle's movement 
    based on the error (difference) between the predicted target position (obtained via predict_ball_y()) 
    and the paddle's current center position. The PID controller uses proportional, integral, and 
    derivative terms to provide a smooth and adaptive response. The controller's persistent state 
    (integral of error and previous error) allows it to "learn" from previous corrections.
    
    Parameters:
        current_paddle_y (int): Current top y-coordinate of the AI paddle.
        ball_y (int): Current y-coordinate of the ball.
        ball_dir_y (int): Current vertical direction of the ball (+1 or -1).
        ball_x (int): Current x-coordinate of the ball.
        ball_dir_x (int): Current horizontal direction of the ball (+1 or -1).
        paddle_x (int): The x-coordinate of the AI paddle.
        height (int): The height of the game window.
        
    Returns:
        int: The updated top y-coordinate for the AI paddle.
    
    Note:
        This function assumes that the global function 'predict_ball_y()' and the constant 'PADDLE_HEIGHT' 
        are defined elsewhere in the module.
    """
    # Initialize persistent PID variables on the first call.
    if not hasattr(ai_move, "pid_integral"):
        ai_move.pid_integral = 0
        ai_move.last_error = 0

    # Determine the target y-coordinate:
    # Use the ball's predicted y-coordinate if it's moving towards the AI paddle; otherwise, default to center.
    if (paddle_x > ball_x and ball_dir_x > 0) or (paddle_x < ball_x and ball_dir_x < 0):
        target_y = predict_ball_y(ball_y, ball_dir_y, ball_x, ball_dir_x, paddle_x, height)
    else:
        target_y = height // 2

    # Calculate the center of the paddle.
    paddle_center = current_paddle_y + PADDLE_HEIGHT // 2

    # Compute error between the target and the current paddle center.
    error = target_y - paddle_center

    # PID coefficients (tuning parameters)
    Kp = 0.5   # Proportional gain: reacts proportionally to the error.
    Ki = 0.01  # Integral gain: accounts for accumulated past errors.
    Kd = 0.2   # Derivative gain: predicts future error based on the change.

    # Update integral (accumulated error) and derivative (error difference).
    ai_move.pid_integral += error
    derivative = error - ai_move.last_error
    ai_move.last_error = error

    # Compute the PID controller output.
    movement = Kp * error + Ki * ai_move.pid_integral + Kd * derivative

    # Limit the paddle to move only one character per frame for smooth movement.
    step = 0
    if movement > 1:
        step = 1
    elif movement < -1:
        step = -1
    elif movement > 0:
        step = 1
    elif movement < 0:
        step = -1

    # Update the paddle's vertical position.
    current_paddle_y += step

    # Ensure the paddle remains within the window bounds.
    current_paddle_y = max(1, min(height - PADDLE_HEIGHT - 1, current_paddle_y))
    return current_paddle_y