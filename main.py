from time import sleep
from wordle.core import WordleGame

if __name__ == "__main__":    
    # Init and run the game
    w = WordleGame()
    print(w._heading())
    w.make_connection("admin", "admin", "wordle_dbms")
    w.make_answer()

    # Wordle running...
    w.run()
    sleep(10)