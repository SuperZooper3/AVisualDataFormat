# Encoder function for the codebar data

def encode(data):
    d = []
    for l in data:
        d.extend([int(i) for i in f"{ord(l):08b}"])
    return d