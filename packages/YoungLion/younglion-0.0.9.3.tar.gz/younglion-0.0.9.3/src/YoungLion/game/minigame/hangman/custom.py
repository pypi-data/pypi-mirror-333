import sys
import os

# Append the parent directory where function.py is located.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

# Import the function module.
import function


class CustomHangmanGame:
    """
    A custom interface for the Evil Hangman game intended for integration into
    non-terminal (e.g., GUI or web) environments.
    
    This class provides methods to configure the game settings (word length, maximum attempts),
    select the secret word, and process letter guesses using an Evil Hangman algorithm.
    """

    def __init__(self, set_language: str = 'en', word_dict: dict = None):
        """
        Initialize the game. If no word dictionary is provided, it loads the data
        from the local data folder using the provided language code.
        
        :param set_language: Language code (e.g., 'en', 'tr', 'ru', 'sp', 'it', 'fr').
        :param word_dict: Optional dictionary where keys are word lengths (int) and values are lists of words.
        """
        if word_dict is None:
            # Get the absolute path of the current file and then the directory.
            filename = os.path.abspath(__file__)
            dir_path = os.path.dirname(filename)
            # Build the path to the JSON data file based on the language.
            data_file = os.path.join(dir_path, 'data', f'{set_language}.json')
            # Load the word dictionary from the JSON file using function.File().
            self.word_dict = function.File().json_read(data_file)
        else:
            self.word_dict = word_dict
        
        self.possible_words = None
        self.word_length = None
        self.max_attempts = None
        self.current_pattern = None
        self.guessed_letters = set()
        self.num_wrong = 0
        self.word = None  # Final secret word will be stored here after game conclusion.
    def enter_word_length(self, length: int) -> bool:
        """
        Set the desired word length if words of that length are available.
        
        :param length: The desired word length.
        :return: True if there are words available for the given length, False otherwise.
        """
        if str(length) in self.word_dict and self.word_dict[str(length)]:
            self.word_length = length
            self.possible_words = set(self.word_dict[str(length)])
            self.current_pattern = "-" * length
            return True
        else:
            return False

    def enter_max_attempts(self, attempts: int) -> bool:
        """
        Set the maximum allowed wrong guesses.
        
        :param attempts: The maximum number of wrong guesses.
        :return: True if attempts is at least 6, False if less than 6.
        """
        if attempts < 6:
            return False
        else:
            self.max_attempts = attempts
            return True

    def find_word(self) -> bool:
        """
        Finalize the secret word selection. In Evil Hangman the word is not chosen until necessary,
        but this function randomly selects one from the remaining possible words and stores it.
        
        :return: True if a word is successfully selected, False otherwise.
        """
        if not self.possible_words or not self.current_pattern:
            return False
        import random
        self.word = random.choice(list(self.possible_words))
        return True

    def get_pattern(self, word: str, guess: str, current_pattern: str) -> str:
        """
        Generate a new pattern by revealing the guessed letter in the word.
        
        :param word: The candidate word.
        :param guess: The guessed letter.
        :param current_pattern: The current pattern (with unrevealed letters as "-").
        :return: A new pattern string with any occurrences of the guessed letter revealed.
        """
        new_pattern = ""
        for i, letter in enumerate(word):
            if letter == guess:
                new_pattern += guess
            else:
                new_pattern += current_pattern[i]
        return new_pattern

    def choose_family(self, guess: str) -> None:
        """
        Partition possible words into families based on the guessed letter and update the current pattern.
        This method selects the family with the largest number of words and, in the event of a tie,
        chooses the one that reveals the fewest new occurrences of the guessed letter.
        
        :param guess: The letter guessed.
        """
        families = {}
        for word in self.possible_words:
            pattern = self.get_pattern(word, guess, self.current_pattern)
            families.setdefault(pattern, set()).add(word)
        
        best_pattern = None
        best_family = set()
        for pattern, words in families.items():
            if len(words) > len(best_family):
                best_family = words
                best_pattern = pattern
            elif len(words) == len(best_family):
                # Tie-breaker: prefer family that reveals fewer occurrences of the guessed letter.
                current_count = best_pattern.count(guess) if best_pattern else float('inf')
                new_count = pattern.count(guess)
                if new_count < current_count:
                    best_family = words
                    best_pattern = pattern
        self.current_pattern = best_pattern
        self.possible_words = best_family

    def enter_letter(self, letter: str) -> int:
        """
        Process the guessed letter, update the game state, and return a code indicating the outcome:
        
        1 - Incorrect guess (the guessed letter did not reveal new characters).
        2 - Correct guess (the letter was found in one or more positions).
        3 - Game won (the complete word has been revealed).
        0 - Game lost (number of wrong guesses reached or exceeded maximum allowed).
        4 - Letter has already been guessed (no penalty).
        
        :param letter: The guessed letter.
        :return: An integer code representing the result of the guess.
        :raises ValueError: If game configuration is incomplete.
        """
        if not self.current_pattern or self.max_attempts is None:
            raise ValueError("Game configuration incomplete. Set word length and max attempts first.")

        # Check if the letter was already guessed.
        if letter in self.guessed_letters:
            return 4

        # Add the guessed letter.
        self.guessed_letters.add(letter)
        previous_pattern = self.current_pattern
        self.choose_family(letter)

        # If the pattern remains unchanged, the guess is incorrect.
        if self.current_pattern == previous_pattern:
            self.num_wrong += 1
            if self.num_wrong >= self.max_attempts:
                return 0  # Game lost.
            else:
                return 1  # Incorrect guess.
        else:
            # Correct guess.
            if "-" not in self.current_pattern:
                # Game won: finalize secret word.
                self.word = list(self.possible_words)[0]
                return 3
            else:
                return 2  # Correct guess.
