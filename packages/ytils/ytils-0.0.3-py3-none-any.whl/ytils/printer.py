import sys
from time import sleep


def print_all_colours():
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            body = "\033[38;5;" + code + "m "
            sys.stdout.write("\033[1m" + body + code.ljust(4))
        print("\u001b[0m")


def clr(texts: tuple, colors: tuple, bold=True) -> str:
    """Add color codes to string"""
    string = ""
    if texts.__len__() != colors.__len__():
        raise ValueError("Missiong text or color")
    if bold:
        bold = "\033[1m"
    else:
        bold = ""
    for i, text in enumerate(texts):
        body = "\033[38;5;" + str(colors[i]) + "m"
        end = "\033[0m"
        string += bold + body + f"{text} " + end
    return string


def inverse(text):
    return f"\033[;7m{text}\033[0m"


def color_bg(text, fg="", bg=""):
    if not fg:
        fg = 1
    else:
        fg = "3" + str(fg)
    if not bg:
        bg = 2
    else:
        bg = "4" + str(bg)
    return f"\033[{fg};{bg}m{text}\033[m"


def rgb(text, r, g, b, bold=True):
    if bold:
        bold = "\033[1m"
    else:
        bold = ""
    return f"{bold}\033[38;2;{r};{g};{b}m{text} \033[0m"


class Cursor:
    @staticmethod
    def up(lines: int):
        sys.stdout.write("\033[F" * lines)

    @staticmethod
    def down(lines: int):
        sys.stdout.write("\033[E" * lines)

    @staticmethod
    def column(position: int):
        sys.stdout.write(f"\033[{position}G")

    @staticmethod
    def beginning():
        sys.stdout.write("\r")


if __name__ == "__main__":
    print_all_colours()
    print(inverse("Text"))
    print(color_bg("Color BG", 1, 2))
    print(clr(("text", "bext"), (216, 3)))
    print(rgb("Hello, World", 102, 255, 178, True))

    print("Line 1")
    print("Line 2")
    sleep(1)
    Cursor.up(2)
    Cursor.column(3)
    print("Hello World")
    sleep(1)
    Cursor.down(3)
    print("Zebra", end="")
    sleep(3)
    Cursor.beginning()
    print("Bebra")
    for i in range(20):
        print(f"{i}    ", end="\r")
        sleep(0.5)

    input("Enter a 5 letter word: ")
    Cursor.up(1)
    print("words go here          ")
    # print('\x1b[1A' + 'words go here          ')
