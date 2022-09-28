# Decoder function for the codebar

def decode(data: list, type = "utf8"):
    if type == "utf8": # if we have a string (default)
        # turn data into a string
        s = "".join(map(str, data))
        # turn the string into bytes objects
        b = int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')
        # decode the bytes object into a string
        try:
            return b.decode("utf-8")
        except:
            return "Error decoding string"

    if type == "num": # if we have a number
        return int("".join([str(m) for m in data]),2)

    raise NotImplementedError("Decode type not implemented")