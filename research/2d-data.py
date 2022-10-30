import importlib
import os
from types import GeneratorType

print("What do you want to do?")
print("[1] Encode a message")
print("[2] Decode a message")
try:
    choice = int(input("Enter your choice: "))
except ValueError:
    print("Choose a number pls")
    exit(3)

# Encode a message
if choice == 1:
    data_size = int(os.getenv("QR_BITS_PER_CHUNK", 5))

    sqr_printer = importlib.import_module("2d-decoding.square_printer")

    msg = input("Enter an integer: ")
    try:
        n = int(msg)
    except ValueError:
        print("Not an integer lol")
        exit(1)

    from encoding_2d_data import encode
    encoded_msg = encode.encode(int(msg))


    path = input("Enter file path: ")
    sqr_printer.printDataSquare(encoded_msg, path, pxSize=20, edgeData=data_size)
    print("Done!")
    print("You can check the file at", path)

elif choice == 2:
    data_size = int(os.getenv("QR_BITS_PER_CHUNK", 5))

    rect_read = importlib.import_module("2d-decoding.rectangle_reader")
    r = rect_read.main(data_size = data_size)

    if isinstance(r, GeneratorType):
        r = next(r)

    from encoding_2d_data import decode
    decoded = decode.decode(r)
    print("Decoded data:", decoded)


else:
    print("Invalid choice")
