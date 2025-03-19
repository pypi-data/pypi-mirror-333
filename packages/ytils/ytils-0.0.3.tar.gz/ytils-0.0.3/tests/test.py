import sys
from pathlib import Path
from time import sleep

sys.path.append(str(Path(__file__).parent.parent))
from src import ytils


def test_printer():
    from src.ytils import printer

    print("Line 1")
    print("Line 2")
    sleep(1)
    printer.Cursor.up(2)
    printer.Cursor.column(3)
    print("Hello World")
    sleep(1)
    printer.Cursor.down(3)
    print("Zebra", end="")
    sleep(3)
    printer.Cursor.beginning()
    print("Bebra")
    # for i in range(20):
    #     print(f"{i}    ", end="\r")
    #     sleep(0.5)

    input("Enter a 5 letter word: ")
    printer.Cursor.up(1)
    print("words go here          ")
    # print('\x1b[1A' + 'words go here          ')


def test_json():
    import json
    from datetime import datetime

    from src.ytils.json import DateTimeEncoder, decode_datetime

    with open("data.json", "w", encoding="utf-8") as f:
        f.write(json.dumps({"datetime": datetime.now()}, cls=DateTimeEncoder, ensure_ascii=False))
    with open("data.json") as f:
        data = json.loads(f.read(), object_hook=decode_datetime)
        print(data)


if __name__ == "__main__":
    test_json()
    # test_printer()
