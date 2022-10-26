# Takes in square images supposedly containing data, cleans them up and tries to extra the data from them
# TODO: Find a strategy to evaluate incorrect blocks

import cv2
import numpy as np
import os

from standard_settings import *

DECODE_TOLLERANCE = 0.2 # Between 0 and 0.5, it's the tollerance for the difference of the average pixel value of a chunk and the threshold to be considered a 1 or 0
CHUNK_MARGIN = 0.2 # Between 0 and 0.5 (0 = no cut, 0.5 = all cut) The % to be cut off from the edges of each chunk area to avoid noise and filtering artifacts 

def decode_square(imageName=None,directory=None,debug=False):
    if imageName != None:
        try:
            img = cv2.imread(imageName)
            # Turn it into a BW image (used to test that there is data in the image)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except:
            return
    else:
        for imageName in os.listdir(directory):
            if imageName.endswith(".png"):
                decode_square(directory+ "/" + imageName, debug=debug)
        return

    # Get image data
    w,h = img.shape[:2]
    
    # Start by doing a global threshold on the image to get binary data
    # Blur filter to remove minor noise
    blur = cv2.GaussianBlur(img,(3,3),0)

    # Global OTSU threshold
    otsuThold,thresholdedImage = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Show the thresholded image
    if debug: 
        cv2.imshow("Thresholded", thresholdedImage)
        cv2.waitKey(0)

    # Go over each bit in the image (diving it into BITS_PER_CHUNK + 2 evenly sized image regions)
    PIXELS_PER_CHUNK = w/(BITS_PER_CHUNK+2) # It's ok to have a decimal here, it means rounding won't compound
    MARGIN_PIXELS_CUT = int(CHUNK_MARGIN*PIXELS_PER_CHUNK)
    data = []
    for row in range(1,BITS_PER_CHUNK+1):
        for col in range(1,BITS_PER_CHUNK+1):
            # Get the chunk
            chunk = thresholdedImage[int((row)*PIXELS_PER_CHUNK)+MARGIN_PIXELS_CUT:int((row+1)*PIXELS_PER_CHUNK)-MARGIN_PIXELS_CUT,int((col)*PIXELS_PER_CHUNK)+MARGIN_PIXELS_CUT:int((col+1)*PIXELS_PER_CHUNK)-MARGIN_PIXELS_CUT]
            # Get the average pixel value of the chunk
            avg = np.average(chunk) / 255 # Normalize to 0-1

            if debug:
                print(avg)
                cv2.imshow("Chunk", chunk)
                cv2.waitKey(0)

            # If the average is withing DECODE_TOLLERANCE of 1 it's a 1, same for 0 and if it's not in the range we assume it's not data
            if avg > 1-DECODE_TOLLERANCE:
                data.append(1)
            elif avg < DECODE_TOLLERANCE:
                data.append(0)
            else:
                # It's outside the tollerance, it's not data
                data.append(None)

    # Print the data
    print("Data: "+"".join([str(i) for i in data]))

if __name__ == "__main__":
    # Decode all the images in the deformed folder
    decode_square(directory="deformed", debug=True)