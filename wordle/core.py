# The main file for wordle game
import colorama

import utils.DB as db
from utils.errors import handle_error
# import utils.DB as db
# from utils.errors import handle_error


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
