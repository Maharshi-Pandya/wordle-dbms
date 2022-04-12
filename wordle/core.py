# The main file for wordle game

# RULES:
# Guess the WORDLE in six tries.
# Each guess must be a valid five-letter word.
# After each guess, the color of the tiles will change to show how close your guess was to the word.
# Green color if the letter is in correct spot
# Yellow color if the letter is in the word, but incorrect spot
# Grey color if the letter is not in the word.

import colorama

import utils.DB as db
from utils.errors import handle_error


# Check if the tuple doesnot contain None
def not_none(tup) -> bool:
    if tup[0] is not None and tup[1] is not None:
        return True
    
    return False


# Take user input and clean it
def input_and_clean():
    word = input()
    user_input = list(word)
        
    clean_input = []
    for i in range(len(user_input)):
        if user_input[i] != ' ':
            clean_input.append(user_input[i])
            
    return clean_input if len(clean_input) == 5 else None
    
class WordleGame:
    def __init__(self) -> None:
        self.conn = None
        self.answer = (None, None)          # (id, content)
        self.rem_turns = 6
        
    # Private: ASCII heading to the screen
    def _heading(self):
        # necessary
        colorama.init(autoreset=True)
        heading = """                                                                                
\t`8.`888b                 ,8'  ,o888888o.     8 888888888o.   8 888888888o.      8 8888         8 8888888888   
\t `8.`888b               ,8'. 8888     `88.   8 8888    `88.  8 8888    `^888.   8 8888         8 8888         
\t  `8.`888b             ,8',8 8888       `8b  8 8888     `88  8 8888        `88. 8 8888         8 8888         
\t   `8.`888b     .b    ,8' 88 8888        `8b 8 8888     ,88  8 8888         `88 8 8888         8 8888         
\t    `8.`888b    88b  ,8'  88 8888         88 8 8888.   ,88'  8 8888          88 8 8888         8 888888888888 
\t     `8.`888b .`888b,8'   88 8888         88 8 888888888P'   8 8888          88 8 8888         8 8888         
\t      `8.`888b8.`8888'    88 8888        ,8P 8 8888`8b       8 8888         ,88 8 8888         8 8888         
\t       `8.`888`8.`88'     `8 8888       ,8P  8 8888 `8b.     8 8888        ,88' 8 8888         8 8888         
\t        `8.`8' `8,`'       ` 8888     ,88'   8 8888   `8b.   8 8888    ,o88P'   8 8888         8 8888         
\t         `8.`   `8'           `8888888P'     8 8888     `88. 8 888888888P'      8 888888888888 8 888888888888\n\n\n
\t        
\t                                          INSIDE YOUR TERMINAL!
    """

        return colorama.Fore.YELLOW + heading
    
    # Public: Attempt to connect to wordle db
    def make_connection(self, user, password, database):
        self.conn, error = db.connect_to_wordle(user, password, database)
        handle_error(error)
        
    # Public: Make a random answer from answers table
    def make_answer(self):
        last_id = db.fetch_last_id(self.conn, "answers")
        self.answer = db.fetch_random_word(self.conn, "answers", last_id)

    def run(self):
        while self.rem_turns > 0:
            # take user_input and clean it
            clean_input = input_and_clean()        
            
            if clean_input is not None:
                # check if the word exists in the DB
                word_to_check = "".join(clean_input)
                check_word = db.check_word_exists(self.conn, "allowed", word_to_check)
                
                if not_none(check_word):
                    word = check_word[1]

                    # TODO: DO SOMETHING WITH THIS
                    print(word)

                else:
                    raise Exception(f"::-> The word '{word_to_check}' is not allowed as an input.")
            else:
                raise Exception("::-> Input should be of length 5 only.")
            self.rem_turns -= 1