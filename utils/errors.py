# For handling errors
import sys

# for now, just printing the error
def handle_error(err) -> None:
    if err is not None:
        print("Error ::->", err)
        sys.exit()
