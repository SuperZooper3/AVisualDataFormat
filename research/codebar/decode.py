# Decoder function for the codebar

def decode(data, type = "ascii"):
    if type == "ascii": # if we have a string (default)
        return "".join([chr(int("".join([str(m) for m in data[i:i+8]]),2)) for i in range(0, len(data), 8)])
    
    if type == "num": # if we have a number
        return int("".join([str(m) for m in data]),2)