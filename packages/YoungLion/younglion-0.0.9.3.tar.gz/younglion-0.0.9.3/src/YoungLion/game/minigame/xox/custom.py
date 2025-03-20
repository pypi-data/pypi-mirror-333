import random

class CustomTicTacToe:
    """
    A custom Tic Tac Toe game class for integration into external interfaces.
    
    This class encapsulates the logic for a standard 3x3 Tic Tac Toe game.
    The human player's mark can be specified (1 for X or 2 for O); if not provided,
    it is randomly chosen. The computer opponent selects moves using the Minimax algorithm.
    
    Public Attributes:
        board (list): A 3x3 list of lists representing the game board.
        player (int): The player's mark (1 or 2).
        computer (int): The computer's mark (the opposite of player).
    
    Outcome Codes (returned by come_move):
        3 - Player wins.
        1 - Player loses (computer wins).
        2 - Game ends in a tie.
        0 - Game continues.
    """

    def __init__(self, player_mark: int = None):
        """
        Initialize the Tic Tac Toe game.
        
        :param player_mark: Optional integer representing the player's mark:
                            1 (for X) or 2 (for O). If not provided, a random assignment is made.
        """
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        if player_mark in [1, 2]:
            self.player = player_mark
        else:
            self.player = random.choice([1, 2])
        self.computer = 1 if self.player == 2 else 2
        # If the computer is assigned X (mark 1), let it make the first move automatically.
        if self.computer == 1:
            self._computer_move()

    def _check_win(self, board, player):
        """
        Check whether the specified player has won the game.
        
        This method checks each row, column, and both diagonals.
        
        :param board: A 3x3 list of lists representing the game board.
        :param player: The player's mark (1 or 2).
        :return: True if the player has a winning line, otherwise False.
        """
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] == player:
                return True
            if board[0][i] == board[1][i] == board[2][i] == player:
                return True
        if board[0][0] == board[1][1] == board[2][2] == player:
            return True
        if board[0][2] == board[1][1] == board[2][0] == player:
            return True
        return False

    def _check_tie(self, board):
        """
        Check if the game is tied.
        
        The game is tied when no empty cells (cells with 0) remain and no win has occurred.
        
        :param board: A 3x3 list of lists representing the game board.
        :return: True if the board is full (tie), otherwise False.
        """
        for row in board:
            if 0 in row:
                return False
        return True

    def _minimax(self, board, depth, is_maximizing, computer_player, opponent):
        """
        Evaluate the board state using the Minimax algorithm.
        
        This recursive method simulates all possible moves and returns a score,
        with higher scores favoring the computer.
        
        :param board: A 3x3 game board.
        :param depth: The depth of recursion, used to favor faster wins.
        :param is_maximizing: True if it is the computer's turn (maximizing), False otherwise.
        :param computer_player: The computer's mark (1 or 2).
        :param opponent: The opponent's mark.
        :return: An integer score evaluating the board state.
        """
        if self._check_win(board, computer_player):
            return 10 - depth
        if self._check_win(board, opponent):
            return depth - 10
        if self._check_tie(board):
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for y in range(3):
                for x in range(3):
                    if board[y][x] == 0:
                        board[y][x] = computer_player
                        score = self._minimax(board, depth + 1, False, computer_player, opponent)
                        board[y][x] = 0
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for y in range(3):
                for x in range(3):
                    if board[y][x] == 0:
                        board[y][x] = opponent
                        score = self._minimax(board, depth + 1, True, computer_player, opponent)
                        board[y][x] = 0
                        best_score = min(best_score, score)
            return best_score

    def _computer_move(self):
        """
        Determine and execute the computer's move using the Minimax algorithm.
        
        This method evaluates each available cell and chooses the move with the highest score.
        The board is updated with the computer's move.
        """
        best_score = -float('inf')
        best_move = None
        opponent = self.player  # human player
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == 0:
                    self.board[y][x] = self.computer
                    score = self._minimax(self.board, 0, False, self.computer, opponent)
                    self.board[y][x] = 0
                    if score > best_score:
                        best_score = score
                        best_move = (y, x)
        if best_move is not None:
            y, x = best_move
            self.board[y][x] = self.computer

    def come_move(self, row: int, col: int) -> int:
        """
        Process the player's move and then (if the game is not over) the computer's move.
        
        The method performs the following steps:
        1. Validates and places the player's mark at (row, col).
        2. Checks if the player's move wins the game (returns 3).
        3. Checks if the board is full (tie; returns 2).
        4. Executes the computer's move.
        5. Checks if the computer's move wins (returns 1) or results in a tie (returns 2).
        6. If none of the terminal conditions are met, returns 0 indicating the game continues.
        
        :param row: Row index (0-2) for the player's move.
        :param col: Column index (0-2) for the player's move.
        :return: Outcome code (3: win, 1: loss, 2: tie, 0: game continues).
        :raises ValueError: If the move is invalid (cell occupied or out of bounds).
        """
        # Validate player's move.
        if row not in range(3) or col not in range(3):
            raise ValueError("Move out of bounds. Row and column must be in the range 0-2.")
        if self.board[row][col] != 0:
            raise ValueError("Invalid move. The cell is already occupied.")

        # Place the player's move.
        self.board[row][col] = self.player
        if self._check_win(self.board, self.player):
            return 3  # Player wins.
        if self._check_tie(self.board):
            return 2  # Tie.

        # Let the computer move.
        self._computer_move()
        if self._check_win(self.board, self.computer):
            return 1  # Computer wins.
        if self._check_tie(self.board):
            return 2  # Tie.
        
        return 0  # Game continues.