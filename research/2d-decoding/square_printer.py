# A simple program to randomly place a black hollow square with a white background for testing of the rectangle_detector.py program

import random
from PIL import Image
import matplotlib.pyplot as plt
import json


def printDataSquare(data, filename, pxSize=1):
    assert(len(data) == 25)

    # The size of the image
    width = (5+4)*pxSize
    height = (5+4)*pxSize

    # The array of pixels
    pixels = [[1]*width for i in range(height)]

    # Chunk the data (5 bits per chunk)
    chunks = [data[i:i+5] for i in range(0, len(data), 5)]

    def writePixel(x, y, value):
        for i in range(x, x+pxSize):
            for j in range(y, y+pxSize):
                pixels[j][i] = value

    # Add the bits to the pixels
    for i in range(len(chunks)):
        for j in range(len(chunks[i])):
            writePixel((i+2)*pxSize, (j+2)*pxSize, chunks[i][j])

    # Add the bottom of the black square
    for i in range(len(chunks)+4):
        writePixel(i*pxSize, 8*pxSize, 0)

    # Add the top of the black square
    for i in range(len(chunks)+4):
        writePixel(i*pxSize, 0, 0)

    # Add the left side of the black square
    for i in range(len(chunks)+4):
        writePixel(0, i*pxSize, 0)

    # Add the right side of the black square
    for i in range(len(chunks)+4):
        writePixel((len(chunks)+3)*pxSize, i*pxSize, 0)

    # Save the image to printed.png
    im = Image.new("1", (width, height), color=1)
    im.putdata([pixel for row in pixels for pixel in row])
    im.save(filename)

if __name__ == "__main__":
    # Generate a random 25-bit string
    data = [random.randint(0, 1) for i in range(25)]
    printDataSquare(data, "printed.png", pxSize=100)