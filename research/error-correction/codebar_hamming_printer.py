# This is a small test to see how hamming coding is useful in the codebar system
from codebar_code import printer, reader, encode
import random
import hamming

value = input("Number to print: ")
if value.isdigit():
    value = int(value)
    assert value < printer.max_data_size**8
    assert value >= 0
    
    data = encode.encode(value,type="num")
    payload = hamming.hamming_encode(data)
    while len(payload) % 8 != 0:
        data = [0] + data
        payload = hamming.hamming_encode(data)
    # To test, change a random payload bit
    n = random.randint(0,len(payload)-1)
    payload[n] = 0 if payload[n] == 1 else 1
    
    # After encoding, we'll load it into a Hamming block
    print("Post-encode",data,payload, len(payload),n)
    printer.codePrint(payload, "printed.png", type="raw")
else:
    print("Invalid number")
    exit()

