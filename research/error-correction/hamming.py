from copy import copy
from math import ceil, log2
# A very basic implementation of the Hamming code function in Python

# https://stackoverflow.com/a/57025941
def power_of_two(n):
    return (n & (n-1) == 0) and n != 0 

def is_paritity_bit(i):
    return i == 0 or power_of_two(i)

def hamming_encode(payload):
    # Step 1: Load all of the payload into a data list, leaving spaces for parity bits
    data = []
    i = 0
    while i < len(payload):
        if is_paritity_bit(len(data)):
            data.append(0)
        else:
            data.append(payload[i])
            i += 1

    # Step 2: Calculate all the parity bits (except for the 0 one, we do that at the end)
    # For this, we'll XOR all of the current data, and then for each of teh 1s in the outcome, set that bit to 1
    runningXOR = 0
    for i in range(len(data)):
        if data[i] == 1:
            runningXOR = runningXOR ^ i

    bitNumber = 0 if runningXOR == 0 else ceil(log2(runningXOR))

    XORbits = [(runningXOR >> i) & 1 for i in range(bitNumber, -1, -1)]

    XORbits.reverse() # reversing beacuse the below loop goes left to right

    for i in range(len(XORbits)):
        if XORbits[i] == 1:
            data[2**i] = 1

    # Step 3: Calculate the 0 parity bit
    data[0] = data.count(1) % 2

    return data

def hamming_decode(data):
    dataCopy = copy(data)
    # Find the error location with the binary parity searches
    runningXOR = 0
    for i in range(len(dataCopy)):
        if dataCopy[i] == 1:
            runningXOR = runningXOR ^ i

    # Check the parity of the entire data (used to detect 2 bit errors)
    parity = dataCopy.count(1) % 2

    if parity == 0 and runningXOR != 0:
        print("At least two errors detected",runningXOR)
        return -1

    elif runningXOR != 0:
        print("Error detected at bit", runningXOR)
        dataCopy[runningXOR] = 0 if dataCopy[runningXOR] == 1 else 1
    
    else:
        print("No errors detected")
        pass

    # Remove the parity bits from the payload
    payload = [dataCopy[i] for i in range(len(dataCopy)) if not is_paritity_bit(i)]
    return payload

if __name__ == "__main__":
    bits = [int(i) for i in input("Enter the bits to encode: ")]
    print("Encoded bits:", hamming_encode(bits))
    print("Decoded bits:", hamming_decode(hamming_encode(bits)))