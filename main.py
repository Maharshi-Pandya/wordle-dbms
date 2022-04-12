# Testing
from wordle.core import WordleGame

w = WordleGame()

w.make_connection("admin", "admin", "wordle_dbms")
w.make_answer()

print(w._heading())
print("Answer created:", w.answer, "\n")

w.run()