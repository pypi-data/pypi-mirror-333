import random
import os

# ANSI escape sequences for colored and formatted terminal output.
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
    
    Uses 'cls' for Windows and 'clear' for Unix-based systems.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_board(board):
    """
    Display the Tic Tac Toe board with row and column labels and colored symbols.
    
    The board is printed to the console with the following symbols:
      - An empty cell is shown as a yellow blank space.
      - Player 'X' (represented by 1) is shown in red.
      - Player 'O' (represented by 2) is shown in green.
    
    :param board: A 3x3 list of lists representing the current game board.
    """
    clear_screen()
    print(BOLD + CYAN + "      Tic Tac Toe" + RESET)
    print(BOLD + CYAN + "     0    1    2" + RESET)
    print()
    for i, row in enumerate(board):
        # Start each row with the row number.
        row_str = BOLD + CYAN + f"{i}  " + RESET
        for j, cell in enumerate(row):
            if cell == 0:
                symbol = YELLOW + "   " + RESET
            elif cell == 1:
                symbol = RED + " X " + RESET
            elif cell == 2:
                symbol = GREEN + " O " + RESET
            row_str += symbol
            if j < 2:
                row_str += BOLD + CYAN + "|" + RESET
        print(row_str)
        if i < 2:
            print(BOLD + CYAN + "    ---+---+---" + RESET)
    print()

def check_win(board, player):
    """
    Check whether the specified player has won the game.
    
    The function checks all rows, columns, and both diagonals to see if the player
    has three of their marks in a row.
    
    :param board: A 3x3 list of lists representing the game board.
    :param player: The player's marker (1 or 2) to check for a win.
    :return: True if the player has a winning combination; otherwise, False.
    """
    for i in range(3):
        # Check rows and columns.
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
    Check if the game is tied.
    
    The game is a tie if there are no empty spaces left on the board and
    no player has won.
    
    :param board: A 3x3 list of lists representing the game board.
    :return: True if the board is full (tie), otherwise False.
    """
    for row in board:
        if 0 in row:
            return False
    return True

def minimax(board, depth, is_maximizing, computer_player, opponent):
    """
    Evaluate the board state using the minimax algorithm.
    
    This recursive function simulates all possible moves for both players
    and returns a score representing the desirability of the board state
    for the computer.
    
    :param board: A 3x3 list of lists representing the game board.
    :param depth: The current depth of recursion. Lower depth scores are preferred.
    :param is_maximizing: True if the current turn is for the computer; otherwise, False.
    :param computer_player: The marker (1 or 2) used by the computer.
    :param opponent: The marker (1 or 2) used by the opponent.
    :return: An integer score representing the evaluation of the board.
    """
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
    
    The function evaluates each possible move and selects the one with the highest score.
    
    :param board: A 3x3 list of lists representing the game board.
    :param computer_player: The marker (1 or 2) used by the computer.
    :return: The updated game board after the computer's move.
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
    
    if best_move:
        y, x = best_move
        board[y][x] = computer_player
    return board

def get_human_move(board, human_player):
    """
    Prompt the human player for their move and validate the input.
    
    This function repeatedly asks for input until a valid move is provided.
    
    :param board: A 3x3 list of lists representing the game board.
    :param human_player: The marker (1 or 2) used by the human.
    :return: A tuple (row, column) indicating the chosen move.
    """
    while True:
        try:
            move = input("Enter row and column (e.g., 0 2): ").strip().split()
            if len(move) != 2:
                print(RED + "Please enter two numbers separated by a space." + RESET)
                continue
            y, x = map(int, move)
            if y not in (0, 1, 2) or x not in (0, 1, 2):
                print(RED + "Numbers must be between 0 and 2." + RESET)
                continue
            if board[y][x] != 0:
                print(RED + "That space is already taken. Try another." + RESET)
                continue
            return (y, x)
        except ValueError:
            print(RED + "Invalid input. Please try again." + RESET)

def main():
    """
    Run the main game loop for Tic Tac Toe.
    
    The game randomly assigns markers to the computer and the human, then
    alternates turns until either a win or tie is detected. After the game ends,
    the user is given the option to start a new game or exit.
    """
    while True:
        # Randomly assign markers: computer is either 1 (X) or 2 (O).
        comp_player = random.choice([1, 2])
        human_player = 1 if comp_player == 2 else 2
        
        print(MAGENTA + BOLD + f"New game: Computer will play as {'X' if comp_player == 1 else 'O'}." + RESET)
        input("Press Enter to start the game...")
        
        # Initialize the board as a 3x3 grid filled with 0's.
        board = [[0, 0, 0] for _ in range(3)]
        game_over = False
        
        # Player 1 always starts. Thus, the turn variable determines whose turn it is.
        turn = 1  

        while not game_over:
            draw_board(board)
            if turn == human_player:
                print(BOLD + "Your turn." + RESET)
                y, x = get_human_move(board, human_player)
                board[y][x] = human_player
                if check_win(board, human_player):
                    draw_board(board)
                    print(GREEN + BOLD + "Congratulations, you won!" + RESET)
                    game_over = True
                elif check_tie(board):
                    draw_board(board)
                    print(YELLOW + BOLD + "It's a tie!" + RESET)
                    game_over = True
                else:
                    turn = comp_player
            else:
                print(BOLD + "Computer is thinking..." + RESET)
                board = computer_move(board, comp_player)
                if check_win(board, comp_player):
                    draw_board(board)
                    print(RED + BOLD + "Computer wins. Better luck next time!" + RESET)
                    game_over = True
                elif check_tie(board):
                    draw_board(board)
                    print(YELLOW + BOLD + "It's a tie!" + RESET)
                    game_over = True
                else:
                    turn = human_player

        # Ask the user if they want to play again or exit.
        choice = input(MAGENTA + "Press Enter for a new game or type 'exit' to quit: " + RESET).strip().lower()
        if choice == 'exit':
            print(CYAN + "Thanks for playing! Goodbye." + RESET)
            break

def init():
    """
    Initialize the Tic Tac Toe module and start the game.
    
    This function serves as the module's entry point. It allows the game to be run 
    by calling init() from another script.
    """
    main()