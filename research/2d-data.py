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
    sqr_printer = importlib.import_module("2d-decoding.square_printer")
    from codebar import encode

    msg = input("Enter an integer: ")
    try:
        encoded_msg = encode.encode(int(msg), type="num")
    except ValueError:
        print("Not an integer lol")
        exit(1)
    vmax = sqr_printer.BITS_TOTAL
    # Pad zeroes
    if len(encoded_msg) < vmax:
        encoded_msg = [0] * (vmax - len(encoded_msg)) + encoded_msg
    else:
        print(f"Bit limit ({sqr_printer.BITS_TOTAL}) exceeded")
        exit(2)

    path = input("Enter file path: ")
    sqr_printer.printDataSquare(encoded_msg, path, pxSize=20)
    print("Done!")
    print("You can check the file at", path)

elif choice == 2:
    rect_read = importlib.import_module("2d-decoding.rectangle_reader")
    rect_read.main()


else:
    print("Invalid choice")
