import os
import re


def load_dotenv(path: str = ".env"):
    to_strip = ["\n", "\t", "\r", " ", "'", '"']
    with open(path) as f:
        for line in f:
            if line != "\n" and not line.startswith("#"):
                key = re.findall(r"(.*?) ?=", line)[0]
                key = key.strip("".join(to_strip))
                value = re.findall(r".*?= ?(.*)", line)[0]
                value = value.strip("".join(to_strip))
                if key and value:
                    os.environ.update({key: value})


if __name__ == "__main__":
    load_dotenv(".env")
