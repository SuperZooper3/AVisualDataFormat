# Encoder function for the codebar data

def encode(value, type = "utf8"):
    if type == "utf8":
        return encode_string(value)
    if type == "num":
        return encode_number(value)

def encode_string(value):
    d = []
    for l in value:
        utf8encoded = l.encode("utf-8")
        d.extend([int(n) for n in "".join([bin(b)[2:].zfill(8) for b in utf8encoded])])
    return d

def encode_number(value):
    return [int(n) for n in bin(value)[2:]]