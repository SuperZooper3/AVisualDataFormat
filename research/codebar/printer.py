# This printer script takes in a binary list of digits and turns them into a space (0) or a bar (1) saved into a file called printed.png

from PIL import Image

digit_width = 5 # Pixel width of each digit
digit_height = 200 # Pixel height of each digit

def codePrint(digits, filename):
    # for each digit, make digit_width copies of it in the array. Ex: [1,0] becomes [1,1,1,0,0,0]
    horizontal_pixels = []
    for digit in digits:
        horizontal_pixels.extend([digit]*digit_width)

    # make an array of pixels for the digits
    pixels = [horizontal_pixels] * digit_height

    # invert the pixels because 1 is white and 0 is black
    pixels = [[1 - pixel for pixel in row] for row in pixels]

    im = Image.new("1", (digit_width*len(digits),digit_height), color=1)
    im.putdata([pixel for row in pixels for pixel in row])
    im.save(filename)

codePrint([1,0,1] + [int(i) for i in input("Enter a binary number: ")] + [1,0,1], "printed.png")