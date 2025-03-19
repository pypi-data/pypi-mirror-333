import base64


def _obfuscate(text: bytes, mask: bytes) -> bytes:
    lmask = len(mask)
    return bytes(c ^ mask[i % lmask] for i, c in enumerate(text))


def obfuscate(text, mask):
    b64_byte_text = base64.b64encode(text.encode())
    return _obfuscate(b64_byte_text, mask.encode()).decode("ISO-8859-1")


def deobfuscate(text, mask):
    b64_byte_text = _obfuscate(text.encode("ISO-8859-1"), mask.encode())
    return base64.b64decode(b64_byte_text).decode()


if __name__ == "__main__":
    mask = "Mask"
    text = "Text123456&свсыхцёэ'іїхсвсячюбс😀"

    text = obfuscate(text, mask)
    print(text)
    print(deobfuscate(text, mask))
