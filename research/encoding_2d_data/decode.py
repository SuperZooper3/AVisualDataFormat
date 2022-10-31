import os

width = int(os.getenv("QR_BITS_PER_CHUNK", 5))

def decode(allBits):
    output = []
    for bits in allBits:
        # Flip bits
        bits = list(map(lambda x: x[::-1], bits))
        
        # Correct rotation
        rotations = 0
        while not (bits[0][0] == 1 and bits[0][-1] == 1) and rotations < 5:
            bits = list(zip(*bits[::-1]))
            rotations += 1
        
        if rotations == 5: # if we rottated and didnt find anything, then it can't be properly encoded data
            continue

        # Remove rotation bits
        data = [b for row in bits for b in row]
        data.pop(width**2 - 1)
        data.pop(width**2 - width)
        data.pop(width-1)
        data.pop(0)

        binary = "".join(map(str, data))
        output.append(int(binary, 2))
    
    return output
