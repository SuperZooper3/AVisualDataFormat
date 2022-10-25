# A simple program to randomly place a black hollow square with a white background for testing of the rectangle_detector.py program

import random
from PIL import Image
import matplotlib.pyplot as plt
import json

# The size of the image
width = 100
height = 100

# The array of pixels
pixels = [[1]*width for i in range(height)]

# K is the number of multiples of the outline to have space inside
## Ex: K = 3 gives
##  # # # # #
##  # . . . #
##  # . . . #
##  # . . . #
##  # # # # #
K = 5

# X is is the width of the edge
X = 1

square_corners = []

# The number of squares to place
numSquares = 5

for i in range(numSquares):
    # Pick a random top left corner for the square (ensure that it's going to be inside the immage so we limit the range)
    x = random.randint(0, width - X*(K+2))
    y = random.randint(0, height - X*(K+2))

    square_corners.append((x,y))

    # Place the outline of the square
    for j in range((K+1)*X): # for each pixel of the edge minus the thicness that'll be drawn by the other strokes
        for k in range(X): # for each pixel of thickness
            # draw the top row
            pixels[y+k][x+j] = 0
            # draw the bottom row
            pixels[y+k+(K+1)*X][x+j+X] = 0
            # draw the left collum
            pixels[y+j+X][x+k] = 0
            # draw the right collum
            pixels[y+j][x+k+(K+1)*X] = 0
  

# Plot the pixels in matplotlib
# plt.imshow(pixels, cmap='gray')
# plt.show()

# Save the image to printed.png
im = Image.new("1", (width, height), color=1)
im.putdata([pixel for row in pixels for pixel in row])
im.save("printed.png")

# Dump the coordinates of the corners of the squares to a json file for testing
with open("square_corners.json", "w") as f:
    json.dump(square_corners, f)