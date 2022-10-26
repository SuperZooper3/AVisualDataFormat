# A simple program to randomly place a black hollow square with a white background for testing of the rectangle_detector.py program

import random
from PIL import Image
import matplotlib.pyplot as plt
import json

from standard_settings import *


def printDataSquare(data, filename, pxSize=1):
    assert(len(data) == BITS_TOTAL)

    # The size of the image
    width = (BITS_PER_CHUNK+4)*pxSize
    height = (BITS_PER_CHUNK+4)*pxSize

    # The array of pixels
    pixels = [[1]*width for i in range(height)]

    # Chunk the data (BITS_PER_CHUNK bits per chunk)
    chunks = [data[i:i+BITS_PER_CHUNK] for i in range(0, len(data), BITS_PER_CHUNK)]

    def writePixel(x, y, value):
        for i in range(x, x+pxSize):
            for j in range(y, y+pxSize):
                pixels[j][i] = value

    # Add the bits to the pixels
    for i in range(BITS_PER_CHUNK):
        for j in range(BITS_PER_CHUNK):
            writePixel((i+2)*pxSize, (j+2)*pxSize, chunks[i][j])

    # Add the bottom of the black square
    for i in range(BITS_PER_CHUNK+4):
        writePixel(i*pxSize, (BITS_PER_CHUNK+3)*pxSize, 0)

    # Add the top of the black square
    for i in range(BITS_PER_CHUNK+4):
        writePixel(i*pxSize, 0, 0)

    # Add the left side of the black square
    for i in range(BITS_PER_CHUNK+4):
        writePixel(0, i*pxSize, 0)

    # Add the right side of the black square
    for i in range(BITS_PER_CHUNK+4):
        writePixel((BITS_PER_CHUNK+3)*pxSize, i*pxSize, 0)

    # Save the image to printed.png
    im = Image.new("1", (width, height), color=1)
    im.putdata([pixel for row in pixels for pixel in row])
    im.save(filename)

if __name__ == "__main__":
    # Generate a random 25-bit string
    data = [random.randint(0, 1) for i in range(BITS_TOTAL)]
    printDataSquare(data, "printed.png", pxSize=10)