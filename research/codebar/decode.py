# Decoder function for the codebar

def decode(data):
    return [chr(int("".join([str(m) for m in data[i:i+8]]),2)) for i in range(0, len(data), 8)]