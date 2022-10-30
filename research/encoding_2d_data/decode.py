def decode(bits):
    bits = bits[0]

    # Flip bits
    bits = list(map(lambda x: x[::-1], bits))
    
    # Correct rotation
    while not (bits[0][0] == 1 and bits[0][-1] == 1):
        bits = list(zip(*bits[::-1]))
    
    data = bits[1:-1]
    data = [i[1:-1] for i in data]
    
    binary = "".join(map(str, [i for x in data for i in x]))
    return int(binary, 2)
