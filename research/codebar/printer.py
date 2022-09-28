# This printer script takes in a binary list of digits and turns them into a space (0) or a bar (1) saved into a file called printed.png
from PIL import Image
from math import ceil, floor, log2

from encode import encode

digit_width = 16 # Pixel width of each digit
digit_height = 200 # Pixel height of each digit

max_data_size = 2**8

typeIndicatorBits = {
    "num": [0,0],
    "utf8": [0,1],
    "url": [1,0],
    "raw": [1,1]
}

def codePrint(digits, filename, type = "ascii"):
    horizontal_pixels = []

    # Pad digits to the left to reach the closest byte
    digits = [0] * ((8 - len(digits)) % 8) + digits

    # Make sure the data will fit inside the max size
    assert(len(digits)//8 < max_data_size)

    digitsLengthBits = [int(c) for c in "{:08b}".format(ceil(len(digits)/8))] # Force length to be expressed in 8 bits

    checksumLength = floor(log2(len(digits)/8))+1

    # compute the checksum
    checksumValue = 0
    for i in range(len(digits)):
        checksumValue += (i+1)**digits[i]
    checksumValue %= 2**checksumLength
    
    checksumBits = [int(c) for c in bin(checksumValue)[2:]]
    checksumBits = [0] * (checksumLength - len(checksumBits)) + checksumBits

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
    return im

def main():
    type = input("Type of data to print (num, utf8, url, raw): ")
    if type == "num":
        value = input("Number to print: ")
        if value.isdigit():
            value = int(value)
            assert value < max_data_size**8
            assert value >= 0
            data = encode(value,type="num")
        else:
            print("Invalid number")
            return
    elif type == "utf8":
        value = input("String to print: ")
        data = encode(value,type = "utf8")
    else:
        print("Not supported")
        return
    
    codePrint(data, "printed.png", type=type)

if __name__ == "__main__":
    main()
