from customWaveshare import *
import sys

def display_on_screen(message):
    displayOnScreen(message)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text_parameter = sys.argv[1]
        display_on_screen(text_parameter)
    else:
        try:
            with open("current.txt", "r") as file:
                text_from_file = file.read()
                displayOnScreen(text_from_file)
        except FileNotFoundError:
            print("current.txt not found.")


# from customWaveshare import *

# displayOnScreen(open("current.txt","r").read())