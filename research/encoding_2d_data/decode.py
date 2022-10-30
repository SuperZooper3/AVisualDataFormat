import os

width = int(os.getenv("QR_BITS_PER_CHUNK", 5))

def decode(bits):
    bits = bits[0]

    # Flip bits
    bits = list(map(lambda x: x[::-1], bits))
    
    # Correct rotation
    while not (bits[0][0] == 1 and bits[0][-1] == 1):
        bits = list(zip(*bits[::-1]))

    # Remove rotation bits
    data = [b for row in bits for b in row]
    data.pop(width**2 - 1)
    data.pop(width**2 - width)
    data.pop(width-1)
    data.pop(0)

    binary = "".join(map(str, data))
    return int(binary, 2)
