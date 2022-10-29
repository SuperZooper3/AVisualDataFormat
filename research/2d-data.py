import importlib


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
    data_size = int(input("With what edge size is the data: "))

    sqr_printer = importlib.import_module("2d-decoding.square_printer")
    from codebar import encode

    msg = input("Enter an integer: ")
    try:
        encoded_msg = encode.encode(int(msg), type="num")
    except ValueError:
        print("Not an integer lol")
        exit(1)

    vmax = data_size**2
    # Pad zeroes
    if len(encoded_msg) < vmax:
        encoded_msg = [0] * (vmax - len(encoded_msg)) + encoded_msg
    else:
        print(f"Bit limit ({data_size**2}) exceeded")
        exit(2)

    path = input("Enter file path: ")
    sqr_printer.printDataSquare(encoded_msg, path, pxSize=20, edgeData=data_size)
    print("Done!")
    print("You can check the file at", path)

elif choice == 2:
    data_size = int(input("With what edge size is the data: "))

    rect_read = importlib.import_module("2d-decoding.rectangle_reader")
    rect_read.main(data_size = data_size)


else:
    print("Invalid choice")
