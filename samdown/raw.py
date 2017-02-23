def split(raw_text):
    return raw_text.replace("\r\n", "\n").split("\n\n")
