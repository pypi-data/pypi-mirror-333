import random

def check_win(board, player):
    """
    Check whether the specified player has won the game.

    This function iterates through each row and column as well as both diagonals
    to determine if the player has three of their marks in a row.

    :param board: A 3x3 list of lists representing the game board.
    :param player: The player number (1 or 2) whose win condition is being checked.
    :return: True if the player has a winning line, otherwise False.
    """
    for i in range(3):
        # Check each row for a win.
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True
        # Check each column for a win.
        if board[0][i] == board[1][i] == board[2][i] == player:
            return True
    # Check the main diagonal.
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    # Check the anti-diagonal.
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def check_tie(board):
    """
    Check if the game is tied.

    The game is tied when there are no empty spaces (cells with 0) left
    on the board and no player has won.

    :param board: A 3x3 list of lists representing the game board.
    :return: True if the board is full (a tie), otherwise False.
    """
    for row in board:
        if 0 in row:
            return False
    return True

def minimax(board, depth, is_maximizing, computer_player, opponent):
    """
    Use the minimax algorithm to evaluate the board state.

    This recursive function simulates all possible moves for both players and 
    returns a score for the current board state. A higher score indicates a 
    more favorable board for the computer.

    :param board: A 3x3 list of lists representing the game board.
    :param depth: The depth of the recursion, used to adjust scores to favor faster wins.
    :param is_maximizing: Boolean flag; True if the current turn is for the computer (maximizing player).
    :param computer_player: The mark (1 or 2) used by the computer.
    :param opponent: The mark (1 or 2) used by the human opponent.
    :return: An integer score evaluating the board state.
    """
    # Terminal state checks.
    if check_win(board, computer_player):
        return 10 - depth
    if check_win(board, opponent):
        return depth - 10
    if check_tie(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        # Try every empty cell.
        for y in range(3):
            for x in range(3):
                if board[y][x] == 0:
                    board[y][x] = computer_player
                    score = minimax(board, depth + 1, False, computer_player, opponent)
                    board[y][x] = 0
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for y in range(3):
            for x in range(3):
                if board[y][x] == 0:
                    board[y][x] = opponent
                    score = minimax(board, depth + 1, True, computer_player, opponent)
                    board[y][x] = 0
                    best_score = min(best_score, score)
        return best_score

def computer_move(board, computer_player):
    """
    Determine and execute the computer's move using the minimax algorithm.

    The function evaluates every available move for the computer and selects the 
    one with the highest minimax score.

    :param board: A 3x3 list of lists representing the game board.
    :param computer_player: The mark (1 or 2) representing the computer.
    :return: The board after the computer has made its move.
    """
    best_score = -float('inf')
    best_move = None
    opponent = 1 if computer_player == 2 else 2

    for y in range(3):
        for x in range(3):
            if board[y][x] == 0:
                board[y][x] = computer_player
                score = minimax(board, 0, False, computer_player, opponent)
                board[y][x] = 0
                if score > best_score:
                    best_score = score
                    best_move = (y, x)

    if best_move is not None:
        y, x = best_move
        board[y][x] = computer_player
    return board

def draw_board(board, player_assignment):
    """
    Render the game board to the console with color-coded output.

    The board is printed to the terminal with the following color scheme:
      - Yellow for empty cells.
      - Red for player X.
      - Green for player O (or vice versa, depending on the player's assignment).
    
    The terminal is cleared before drawing the board.

    :param board: A 3x3 list of lists representing the current game board.
    :param player_assignment: The player's assigned mark (1 or 2).
    """
    # Clear the terminal screen.
    print('\033[2J\033[f', end='')
    print("\033[1;34mTic Tac Toe\033[0m\n")
    
    # Display assignment: if the human is 1, then they are "X" and the computer is "O".
    if player_assignment == 1:
        print("\033[33mPlayer: X\033[0m | \033[32mComputer: O\033[0m\n")
    else:
        print("\033[33mPlayer: O\033[0m | \033[32mComputer: X\033[0m\n")
    
    for row in board:
        for cell in row:
            if cell == 0:
                print("\033[33m|-|", end=" \033[0m")
            elif cell == 1:
                print("\033[31m|X|", end=" \033[0m")
            elif cell == 2:
                print("\033[32m|O|", end=" \033[0m")
        print("\n")

def play_game():
    """
    Run the Tic Tac Toe game loop.

    The game starts with an empty board and randomly decides whether the human
    or the computer goes first. It alternates turns between the human and the 
    computer until either a win or a tie is detected. User inputs are validated
    to ensure that moves are within range and made in empty cells.
    """
    # Initialize the game board: a 3x3 grid of zeros.
    board = [[0 for _ in range(3)] for _ in range(3)]
    
    # Randomly decide the player's assignment.
    # If player_assignment is 1, the human plays as 1 (X) and goes first.
    # If player_assignment is 2, the computer goes first with mark 1 (X), and the human is 2 (O).
    player_assignment = random.choice([1, 2])
    
    while True:
        if player_assignment == 1:
            # Human's turn.
            draw_board(board, player_assignment)
            valid_move = False
            while not valid_move:
                try:
                    user_input = input("Enter row and column (0-2 separated by space): ")
                    user_row, user_col = map(int, user_input.split())
                    # Validate input range.
                    if user_row not in range(3) or user_col not in range(3):
                        print("\033[31mInvalid input. Please enter numbers between 0 and 2.\033[0m")
                        continue
                    # Check if the cell is empty.
                    if board[user_row][user_col] != 0:
                        print("\033[31mPlease choose an empty space.\033[0m")
                    else:
                        valid_move = True
                except (ValueError, IndexError):
                    print("\033[31mInvalid input. Please enter numbers between 0 and 2 separated by space.\033[0m")
            
            board[user_row][user_col] = 1
            if check_win(board, 1):
                draw_board(board, player_assignment)
                print("\033[32mCongratulations. You \033[5mWON!\033[0m")
                break
            if check_tie(board):
                draw_board(board, player_assignment)
                print("\033[33mThe game ended in a draw. Well played!\033[0m")
                break
            
            # Computer's turn: computer plays as 2.
            board = computer_move(board, 2)
            if check_win(board, 2):
                draw_board(board, player_assignment)
                print("\033[32mThe computer \033[5mWON!\033[0m")
                print("\033[1;31mYou lost. Try your luck again.\033[0m")
                break
            if check_tie(board):
                draw_board(board, player_assignment)
                print("\033[33mThe game ended in a draw. Well played!\033[0m")
                break
        else:
            # Computer's turn first: computer plays as 1.
            board = computer_move(board, 1)
            draw_board(board, player_assignment)
            if check_win(board, 1):
                draw_board(board, player_assignment)
                print("\033[32mThe computer \033[5mWON!\033[0m")
                print("\033[1;31mYou lost. Try your luck again.\033[0m")
                break
            if check_tie(board):
                draw_board(board, player_assignment)
                print("\033[33mThe game ended in a draw. Well played!\033[0m")
                break
            
            # Human's turn.
            valid_move = False
            while not valid_move:
                try:
                    user_input = input("Enter row and column (0-2 separated by space): ")
                    user_row, user_col = map(int, user_input.split())
                    if user_row not in range(3) or user_col not in range(3):
                        print("\033[31mInvalid input. Please enter numbers between 0 and 2.\033[0m")
                        continue
                    if board[user_row][user_col] != 0:
                        print("\033[31mPlease choose an empty space.\033[0m")
                    else:
                        valid_move = True
                except (ValueError, IndexError):
                    print("\033[31mInvalid input. Please enter numbers between 0 and 2 separated by space.\033[0m")
            
            board[user_row][user_col] = 2
            if check_win(board, 2):
                draw_board(board, player_assignment)
                print("\033[32mCongratulations. You \033[5mWON!\033[0m")
                break
            if check_tie(board):
                draw_board(board, player_assignment)
                print("\033[33mThe game ended in a draw. Well played!\033[0m")
                break

    input("\033[35mPress Enter to exit\033[0m")

def init():
    """
    Initialize the Tic Tac Toe module and start the game.

    This function acts as the entry point for running the game when the module
    is imported and executed using init().
    """
    play_game()
