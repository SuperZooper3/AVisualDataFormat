# Encoder function for the codebar data

def encode_string(value):
    d = []
    for l in value:
        d.extend([int(i) for i in f"{ord(l):08b}"])
    return d

def encode_number(value):
    return [int(n) for n in bin(value)[2:]]