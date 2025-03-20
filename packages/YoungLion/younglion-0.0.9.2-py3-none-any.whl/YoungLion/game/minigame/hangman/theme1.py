import sys
import os

# Append the parent directory where function.py is located.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

# Import the function module.
import function


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
    Clear the terminal screen using the appropriate command for the operating system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """
    Print the Hangman game header with decorative Unicode art.
    """
    clear_screen()
    print(BOLD + MAGENTA + "╔══════════════════════════╗" + RESET)
    print(BOLD + MAGENTA + "║        Hangman Game      ║" + RESET)
    print(BOLD + MAGENTA + "╚══════════════════════════╝" + RESET)
    print()

# Hangman drawing states for wrong guesses.
HANGMAN_PICS = [
    # 0 wrong guesses.
    """
      +---+
      |   |
          |
          |
          |
          |
    =========""",
    # 1 wrong guess.
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========""",
    # 2 wrong guesses.
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========""",
    # 3 wrong guesses.
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========""",
    # 4 wrong guesses.
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========""",
    # 5 wrong guesses.
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========""",
    # 6 wrong guesses.
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    ========="""
]

def draw_hangman(num_wrong, max_wrong):
    """
    Draw the current Hangman state using ANSI colors.
    
    :param num_wrong: Number of incorrect guesses.
    :param max_wrong: Maximum allowed wrong guesses.
    """
    index = min(num_wrong, len(HANGMAN_PICS) - 1)
    art = HANGMAN_PICS[index]
    print(CYAN + art + RESET)

def display_game_state(current_pattern, guessed_letters, num_wrong, max_wrong):
    """
    Display the current game state, including the hangman drawing, the current word pattern,
    guessed letters, and the number of remaining attempts.
    
    :param current_pattern: The current pattern of the word (with letters and dashes).
    :param guessed_letters: A set of letters that have been guessed so far.
    :param num_wrong: Number of incorrect guesses made.
    :param max_wrong: Maximum number of wrong guesses allowed.
    """
    print_header()
    draw_hangman(num_wrong, max_wrong)
    print()
    spaced_pattern = ' '.join(current_pattern)
    print(BOLD + YELLOW + "Word: " + RESET + spaced_pattern)
    print()
    if guessed_letters:
        print(BOLD + "Guessed Letters: " + RESET + ", ".join(sorted(guessed_letters)))
    else:
        print(BOLD + "Guessed Letters: " + RESET + "None")
    print(BOLD + "Remaining Attempts: " + RESET + f"{max_wrong - num_wrong}")
    print()

def get_user_guess(guessed_letters):
    """
    Prompt the user for a letter guess, ensuring the input is valid.
    
    :param guessed_letters: The set of letters already guessed.
    :return: A lowercase letter that has not yet been guessed.
    """
    while True:
        guess = input("Enter your guess (a single letter): ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print(RED + "Please enter a single alphabet letter." + RESET)
        elif guess in guessed_letters:
            print(RED + "You have already guessed that letter. Try another." + RESET)
        else:
            return guess

def get_word_length(word_dict: dict) -> int:
    """
    Prompt the user to choose a desired word length and return the available words of that length.
    
    :param word_dict: The dictionary containing words categorized by length.
    :return: A tuple (length, word_list) where word_list contains words of the chosen length.
    """
    while True:
        try:
            length = input("Enter desired word length: ").strip()
            if length not in word_dict:
                print(RED + f"No words of length {length} available. Please try a different length." + RESET)
            else:
                return int(length), word_dict[length]
        except ValueError:
            print(RED + "Invalid input. Please enter a valid number." + RESET)

def get_max_attempts():
    """
    Prompt the user to enter the maximum number of wrong guesses allowed.
    
    :return: The maximum allowed wrong guesses as an integer.
    """
    while True:
        try:
            max_attempts = int(input("Enter maximum number of wrong guesses allowed (e.g., 6): ").strip())
            if max_attempts < 1:
                print(RED + "The number must be at least 1." + RESET)
            else:
                return max_attempts
        except ValueError:
            print(RED + "Invalid input. Please enter a valid number." + RESET)

def get_pattern(word, guess, current_pattern):
    """
    Generate a new pattern for a word based on the current guessed letter.
    
    For each letter in the word, if it matches the guessed letter, it is revealed;
    otherwise, the character from the current pattern is retained.
    
    :param word: The word being considered.
    :param guess: The letter that was just guessed.
    :param current_pattern: The current known pattern of the word.
    :return: A new pattern string reflecting any occurrences of the guessed letter.
    """
    new_pattern = ""
    for i, letter in enumerate(word):
        if letter == guess:
            new_pattern += guess
        else:
            new_pattern += current_pattern[i]
    return new_pattern

def choose_family(possible_words, guess, current_pattern):
    """
    Partition the possible words into families based on the pattern produced by the guessed letter.
    
    The function selects the family (i.e. pattern and corresponding set of words) that:
      - Has the largest number of words.
      - In case of a tie, prefers the family that reveals the fewest new occurrences of the guessed letter.
    
    :param possible_words: A set of words currently possible.
    :param guess: The current guessed letter.
    :param current_pattern: The current pattern of the secret word.
    :return: A tuple (new_pattern, new_possible_words) for the chosen family.
    """
    families = {}
    for word in possible_words:
        pattern = get_pattern(word, guess, current_pattern)
        families.setdefault(pattern, set()).add(word)
    
    best_pattern = None
    best_family = set()
    for pattern, words in families.items():
        if len(words) > len(best_family):
            best_family = words
            best_pattern = pattern
        elif len(words) == len(best_family):
            # Tie-breaker: prefer family revealing fewer occurrences of the guessed letter.
            current_count = best_pattern.count(guess) if best_pattern else float('inf')
            new_count = pattern.count(guess)
            if new_count < current_count:
                best_family = words
                best_pattern = pattern
    return best_pattern, best_family

def play_hangman(word_dict: dict):
    """
    Play a game of Hangman using an advanced Evil Hangman algorithm.
    
    In Evil Hangman, the computer dynamically changes the secret word family to make the game more challenging.
    The user chooses the word length and maximum number of wrong guesses, and then attempts to guess the word.
    
    :param word_dict: Dictionary where keys are word lengths and values are lists of words.
    """
    print_header()
    print(BOLD + CYAN + "Welcome to Evil Hangman!" + RESET)
    print()
    
    word_length, filtered_words = get_word_length(word_dict)
    max_attempts = get_max_attempts()
    
    possible_words = set(filtered_words)
    current_pattern = "-" * word_length
    guessed_letters = set()
    num_wrong = 0
    
    while True:
        display_game_state(current_pattern, guessed_letters, num_wrong, max_attempts)
        
        if "-" not in current_pattern:
            print(GREEN + BOLD + "Congratulations! You guessed the word!" + RESET)
            break
        
        if num_wrong >= max_attempts:
            secret_word = random.choice(list(possible_words))
            print(RED + BOLD + f"Game Over! The word was: {secret_word}" + RESET)
            break
        
        guess = get_user_guess(guessed_letters)
        guessed_letters.add(guess)
        
        new_pattern, new_possible_words = choose_family(possible_words, guess, current_pattern)
        
        if new_pattern == current_pattern:
            num_wrong += 1
            print(RED + "Incorrect guess!" + RESET)
        else:
            current_pattern = new_pattern
            print(GREEN + "Good guess!" + RESET)
        
        possible_words = new_possible_words

def main(word_dict: dict):
    """
    Run the main loop for the Hangman game.
    
    After each game, the user is prompted to play again or exit.
    :param word_list: Word list. A game will be chosen from this word list.
    """
    while True:
        play_hangman(word_dict)
        choice = input(MAGENTA + "Press Enter to play again or type 'exit' to quit: " + RESET).strip().lower()
        if choice == 'exit':
            print(BOLD + CYAN + "Thank you for playing Evil Hangman! Goodbye." + RESET)
            break

def init(set_language: str = 'en'):
    """
    Initialize the Hangman module and start the game.
    
    This function serves as the entry point for the module. Call init() to launch the game.

    :param set_language: Set words language: en, tr, ru, sp, it, fr
    """
    filename = os.path.abspath(__file__)
    dir = os.path.dirname(filename)
    word_dict = function.File().json_read(f'{dir}/data/{set_language}.json') if set_language in ['en', 'tr', 'ru', 'sp', 'it', 'fr'] else function.File().json_read(f'{dir}/data/en.json')
    
    main(word_dict)