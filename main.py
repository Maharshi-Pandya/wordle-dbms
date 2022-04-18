from wordle.core import WordleGame

# Init and run the game
w = WordleGame()
w.make_connection("admin", "admin", "wordle_dbms")
w.make_answer()
print(w._heading())

# Wordle running...
w.run()