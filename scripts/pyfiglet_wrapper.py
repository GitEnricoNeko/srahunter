# pyfiglet_wrapper.py
import pyfiglet
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
        print(pyfiglet.figlet_format(text))
    else:
        print("Usage: pyfiglet_wrapper.py [text]")

