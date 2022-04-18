# The main file for wordle game

# RULES:
# Guess the WORDLE in six tries.
# Each guess must be a valid five-letter word.
# After each guess, the color of the tiles will change to show how close your guess was to the word.
# Green color if the letter is in correct spot
# Yellow color if the letter is in the word, but incorrect spot
# Grey color if the letter is not in the word.

from turtle import color
import colorama

import utils.DB as db
from utils.errors import handle_error


# Check if the tuple doesnot contain None
def not_none(tup) -> bool:
    if tup[0] is not None and tup[1] is not None:
        return True
    
    return False


# Take user input and clean it
def input_and_clean(guess_num):
    word = input(f"\t\tEnter guess #{guess_num}: ")
    user_input = list(word)
        
    clean_input = []
    for i in range(len(user_input)):
        if user_input[i] != ' ':
            clean_input.append(user_input[i])
            
    return clean_input if len(clean_input) == 5 else None
    

# Check closeness of word and answer
def check_closeness(word, answer: str) -> list:
    cn_list = []
    
    for i in range(len(word)):
        curr = word[i]
        cnt = answer.count(curr)
        
        if cnt > 0:
            if word[i] == answer[i]:
                cn_list.append(colorama.Back.GREEN)
            else:
                cn_list.append(colorama.Back.YELLOW)
        else:
            cn_list.append(colorama.Back.LIGHTBLACK_EX)
            
    return cn_list

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
\t                                         🚀 INSIDE YOUR TERMINAL! 🚀
    """

        return colorama.Fore.GREEN + heading
    
    # Public: Attempt to connect to wordle db
    def make_connection(self, user, password, database):
        self.conn, error = db.connect_to_wordle(user, password, database)
        handle_error(error)
        
    # Public: Make a random answer from answers table
    def make_answer(self):
        last_id = db.fetch_last_id(self.conn, "answers")
        self.answer = db.fetch_random_word(self.conn, "answers", last_id)

    def run(self):
        final_input = None
        while self.rem_turns > 0:
            # take user_input and clean it
            final_input = input_and_clean(7 - self.rem_turns)        
            
            if final_input is not None:
                # check if the word exists in the DB
                word_to_check = "".join(final_input)
                
                # when input is equal to answer
                if word_to_check == self.answer[1]:
                    print(colorama.Fore.YELLOW + "\n\n\t\t\t\t\t\tYou guessed the wordle correctly! ✅\n\n")
                    exit(0)
                
                # check for existence in both tables
                check_word_alo = db.check_word_exists(self.conn, "allowed", word_to_check)
                check_word_ans = db.check_word_exists(self.conn, "answers", word_to_check)
                
                input_word = None
                if not_none(check_word_alo):
                    input_word = check_word_alo
                elif not_none(check_word_ans):
                    input_word = check_word_ans
                
                if input_word is not None:
                    word = input_word[1]

                    # TODO: Check how close is the word to the answer
                    cn_list = check_closeness(word, self.answer[1])
                    print("\n\t\t", end="")
                    for i in range(len(word)):
                        print(cn_list[i] + " " + word[i] + " ", end="")
                    print("\n")

                else:
                    print(colorama.Fore.RED + f"\n\t\t::-> The word '{word_to_check}' is not allowed as an input.\n")
                    continue
            else:
                print(colorama.Fore.RED + "\n\t\t::-> Input should be of length 5 only.\n")
                continue

            self.rem_turns -= 1
            
        print(colorama.Fore.YELLOW + "\n\n\t\t\t\t\t\t❌ Nope, the answer was",
              colorama.Fore.RED + f"{self.answer[1]}" + colorama.Fore.RESET + "!\n\n")
