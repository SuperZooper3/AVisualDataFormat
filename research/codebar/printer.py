# This printer script takes in a binary list of digits and turns them into a space (0) or a bar (1) saved into a file called printed.png
from encode import encode
from PIL import Image
from math import ceil

digit_width = 16 # Pixel width of each digit
digit_height = 200 # Pixel height of each digit

typeIndicatorBits = {
    "num": [0,0],
    "ascii": [0,1],
    "utf8": [1,0],
    "raw": [1,1]
}

def codePrint(digits, filename, type = "ascii"):
    horizontal_pixels = []

    # Pad digits to the left to reach the closest byte
    digits = [0] * ((8 - len(digits)) % 8) + digits

    # Make sure the data will fit inside the max size
    assert(len(digits)//8 < 2**8)

    digitsLengthBits = [int(c) for c in bin(ceil(len(digits)/8))[2:]]

    # count the number of "1" bars in the data
    checksumValue = (digits.count(1) % digits.count(0)) % ceil(len(digits)/8)
    
    checksumBits = [int(c) for c in bin(checksumValue)[2:]]

    fullData = [1,0,1,1] + typeIndicatorBits[type] + digitsLengthBits + checksumBits + digits + [0,1,0,1]

    print("Type bits: ", typeIndicatorBits[type], "Length bits: ", digitsLengthBits, "Checksum bits: ", checksumBits, "Digits: ", digits)

    # for each digit, make digit_width copies of it in the array. Ex: [1,0] becomes [1,1,1,0,0,0]
    for digit in fullData:
        horizontal_pixels.extend([digit]*digit_width)

    # make an array of pixels for the digits
    pixels = [horizontal_pixels] * digit_height

    # invert the pixels because 1 is white and 0 is black
    pixels = [[1 - pixel for pixel in row] for row in pixels]

    im = Image.new("1", (digit_width*len(fullData), digit_height), color=1)
    im.putdata([pixel for row in pixels for pixel in row])
    im.save(filename)

data = encode(input("Enter a string: "))

codePrint(data, "printed.png")