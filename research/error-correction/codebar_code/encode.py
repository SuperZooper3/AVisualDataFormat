# Encoder function for the codebar data

def encode(value, type = "utf8"):
    if type == "utf8" or type == "url":
        return encode_string(value)
    if type == "num":
        return encode_number(value)
    if type == "raw":
        return encode_raw(value)

def encode_string(value):
    try:
        d = []
        for l in value:
            utf8encoded = l.encode("utf-8")
            d.extend([int(n) for n in "".join([bin(b)[2:].zfill(8) for b in utf8encoded])])
        return d
    except:
        raise ValueError("Invalid string")

def encode_number(value):
    try:
        return [int(n) for n in bin(value)[2:]]
    except:
        raise ValueError("Invalid number")

def encode_raw(value):
    try:
        return [int(n) for n in value]
    except:
        raise ValueError("Invalid raw data")