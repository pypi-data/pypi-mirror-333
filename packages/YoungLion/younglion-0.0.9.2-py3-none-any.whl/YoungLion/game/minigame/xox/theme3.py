import random
import os

# ANSI escape sequences for colors and text styles.
RESET   = "\033[0m"
BOLD    = "\033[1m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
CYAN    = "\033[36m"
MAGENTA = "\033[35m"

def clear_screen():
    """
    Clear the terminal screen.
    
    Uses the appropriate command based on the operating system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """
    Print the game header using Unicode box-drawing characters.
    
    Clears the screen first, then prints a decorative header.
    """
    clear_screen()
    # Decorative header using Unicode box characters.
    print(BOLD + MAGENTA + "╔══════════════════════════╗" + RESET)
    print(BOLD + MAGENTA + "║       Tic Tac Toe        ║" + RESET)
    print(BOLD + MAGENTA + "╚══════════════════════════╝" + RESET)
    print()

def draw_board(board):
    """
    Display the current Tic Tac Toe board with row and column numbers.
    
    The board uses the following conventions:
      - Empty cells (0) are shown as blank yellow spaces.
      - Player 'X' (1) is shown in red.
      - Player 'O' (2) is shown in green.
    
    :param board: A 3x3 list of lists representing the game board.
    """
    print_header()
    print("    0   1   2")
    print("  ┌───┬───┬───┐")
    
    for i, row in enumerate(board):
        # Start each row with its number and a vertical separator.
        row_str = f"{i} │"
        for j, cell in enumerate(row):
            # Determine the symbol based on the cell's value.
            if cell == 0:
                symbol = YELLOW + "   " + RESET
            elif cell == 1:
                symbol = RED + " X " + RESET
            elif cell == 2:
                symbol = GREEN + " O " + RESET
            row_str += symbol + "│"
        print(row_str)
        if i < 2:
            print("  ├───┼───┼───┤")
    
    print("  └───┴───┴───┘")
    print()

def check_win(board, player):
    """
    Check whether the given player has won the game.
    
    The function verifies all rows, columns, and both diagonals to see if the
    player has three marks in a row.
    
    :param board: A 3x3 list of lists representing the game board.
    :param player: The marker (1 or 2) representing the player.
    :return: True if the player wins; otherwise, False.
    """
    # Check rows and columns.
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True
        if board[0][i] == board[1][i] == board[2][i] == player:
            return True
    # Check the two diagonals.
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def check_tie(board):
    """
    Check if the game has ended in a tie.
    
    The game is tied if there are no empty cells (cells with a 0) remaining.
    
    :param board: A 3x3 list of lists representing the game board.
    :return: True if there is a tie; otherwise, False.
    """
    for row in board:
        if 0 in row:
            return False
    return True

def minimax(board, depth, is_maximizing, computer_player, opponent):
    """
    Evaluate the board state using the minimax algorithm.
    
    The algorithm simulates all possible moves recursively and returns a score
    representing the board's favorability for the computer. A higher score indicates
    a better outcome for the computer.
    
    :param board: A 3x3 list of lists representing the game board.
    :param depth: The current depth of recursion.
    :param is_maximizing: True if the current move is for the computer; otherwise, False.
    :param computer_player: The marker (1 or 2) representing the computer.
    :param opponent: The marker (1 or 2) representing the human opponent.
    :return: An integer score for the board.
    """
    # Terminal condition: check if a player has won or if the board is full.
    if check_win(board, computer_player):
        return 10 - depth
    if check_win(board, opponent):
        return depth - 10
    if check_tie(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
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
    
    The function evaluates every available move and selects the one with the highest
    minimax score.
    
    :param board: A 3x3 list of lists representing the game board.
    :param computer_player: The marker (1 or 2) for the computer.
    :return: The updated game board after the move.
    """
    best_score = -float('inf')
    best_move = None
    opponent = 1 if computer_player == 2 else 2

    # Evaluate all empty cells.
    for y in range(3):
        for x in range(3):
            if board[y][x] == 0:
                board[y][x] = computer_player
                score = minimax(board, 0, False, computer_player, opponent)
                board[y][x] = 0
                if score > best_score:
                    best_score = score
                    best_move = (y, x)

    # If a move was found, update the board.
    if best_move:
        y, x = best_move
        board[y][x] = computer_player
    return board

def get_human_move(board, human_player):
    """
    Prompt the human player for a valid move.
    
    This function repeatedly asks the player for input until a valid move is provided.
    
    :param board: A 3x3 list of lists representing the game board.
    :param human_player: The marker (1 or 2) for the human.
    :return: A tuple (row, column) for the move.
    """
    while True:
        try:
            move = input("Enter row and column (e.g., 0 2): ").strip().split()
            if len(move) != 2:
                print(RED + "Enter exactly two numbers separated by a space." + RESET)
                continue
            y, x = map(int, move)
            if y not in [0, 1, 2] or x not in [0, 1, 2]:
                print(RED + "Row and column must be between 0 and 2." + RESET)
                continue
            if board[y][x] != 0:
                print(RED + "That cell is occupied. Choose another." + RESET)
                continue
            return (y, x)
        except ValueError:
            print(RED + "Invalid input. Please enter numbers only." + RESET)

def main():
    """
    Run the main game loop for Tic Tac Toe.
    
    A new game is started by randomly assigning roles (computer/human) with markers.
    The game alternates moves until there is either a win or a tie. At the end of the
    game, the player is asked whether they want to play again.
    """
    while True:
        # Randomly assign the computer's marker (1 for 'X' or 2 for 'O').
        computer_player = random.choice([1, 2])
        # Assign the human the opposite marker.
        human_player = 1 if computer_player == 2 else 2

        print(BOLD + CYAN + f"New Round: Computer is '{'X' if computer_player == 1 else 'O'}'." + RESET)
        input("Press Enter to start the game...")

        # Initialize the game board as a 3x3 grid filled with zeros.
        board = [[0, 0, 0] for _ in range(3)]
        game_over = False

        # Player 1 always starts. 'turn' indicates whose turn it is.
        turn = 1

        while not game_over:
            draw_board(board)
            if turn == human_player:
                print(BOLD + "Your move." + RESET)
                y, x = get_human_move(board, human_player)
                board[y][x] = human_player
                if check_win(board, human_player):
                    draw_board(board)
                    print(GREEN + BOLD + "Victory! You won the game!" + RESET)
                    game_over = True
                elif check_tie(board):
                    draw_board(board)
                    print(YELLOW + BOLD + "It's a draw!" + RESET)
                    game_over = True
                else:
                    turn = computer_player
            else:
                print(BOLD + "Computer is calculating its move..." + RESET)
                board = computer_move(board, computer_player)
                if check_win(board, computer_player):
                    draw_board(board)
                    print(RED + BOLD + "Defeat! Computer wins." + RESET)
                    game_over = True
                elif check_tie(board):
                    draw_board(board)
                    print(YELLOW + BOLD + "It's a draw!" + RESET)
                    game_over = True
                else:
                    turn = human_player

        # Ask the player whether to start a new game or exit.
        choice = input(MAGENTA + "Press Enter to play again or type 'exit' to quit: " + RESET).strip().lower()
        if choice == 'exit':
            print(BOLD + CYAN + "Thank you for playing! See you next time." + RESET)
            break

def init():
    """
    Initialize the Tic Tac Toe module and start the game.
    
    This function serves as the entry point for running the game when imported as a module.
    Call init() to start the game.
    """
    main()