# Takes in square images supposedly containing data, cleans them up and tries to extra the data from them
# TODO: Find a strategy to evaluate incorrect blocks

import cv2
import numpy as np
import os

from .standard_settings import *

DECODE_TOLLERANCE = 0.2  # Between 0 and 0.5, it's the tollerance for the difference of the average pixel value of a chunk and the threshold to be considered a 1 or 0
# Between 0 and 0.5 (0 = no cut, 0.5 = all cut) The % to be cut off from the edges of each chunk area to avoid noise and filtering artifacts
CHUNK_MARGIN = 0.2


def decode_square(data_size=BITS_PER_CHUNK, imageName=None, directory=None, debug=False, ):
    if imageName != None:
        try:
            img = cv2.imread(imageName)
            # Turn it into a BW image (used to test that there is data in the image)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except:
            return
    else:
        data = []
        for imageName in os.listdir(directory):
            if imageName.endswith(".png"):
                extracted = decode_square(data_size = data_size, imageName = directory + "/" + imageName, debug=debug)

                # If it's -1 then it's garbage
                if extracted == -1:
                    continue

                # If the data is all the same (ie all 1 or 0), then it's garbage
                total_set = set()
                for l in extracted:
                    total_set = total_set.union(set(l))
                if len(total_set) == 1:
                    continue

                # Otherise it's probably real data
                data.append(extracted)
        
        print(f"Found {len(data)} images with data. Data: {data}")
        return data

    # Get image data
    w, h = img.shape[:2]

    # Start by doing a global threshold on the image to get binary data
    # Blur filter to remove minor noise
    blur = cv2.GaussianBlur(img, (3, 3), 0)

    # Global OTSU threshold
    otsuThold, thresholdedImage = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Show the thresholded image
    if debug:
        cv2.imshow("Thresholded", thresholdedImage)
        cv2.waitKey(0)

    # Go over each bit in the image (diving it into data_size + 2 evenly sized image regions)
    # It's ok to have a decimal here, it means rounding won't compound
    PIXELS_PER_CHUNK = w/(data_size+2)
    MARGIN_PIXELS_CUT = int(CHUNK_MARGIN*PIXELS_PER_CHUNK)
    data = []
    for row in range(1, data_size+1):
        rowList = []
        for col in range(1, data_size+1):
            # Get the chunk
            chunkLeftX = int((row)*PIXELS_PER_CHUNK) + MARGIN_PIXELS_CUT
            chunkRightX = int((row+1)*PIXELS_PER_CHUNK) - MARGIN_PIXELS_CUT
            chunkTopY = int((col)*PIXELS_PER_CHUNK) + MARGIN_PIXELS_CUT
            chunkBottomY = int((col+1)*PIXELS_PER_CHUNK) - MARGIN_PIXELS_CUT
            chunk = thresholdedImage[chunkLeftX:chunkRightX, chunkTopY:chunkBottomY]
            # Show each chunk
            # put points on the orignal image to show where we're looking
            # n = thresholdedImage.copy()
            # cv2.circle(n, (chunkLeftX, chunkTopY), 5, (0, 0, 255), -1)
            # cv2.circle(n, (chunkRightX, chunkBottomY), 5, (0, 0, 255), -1)
            # cv2.imshow("Thresholded", n)
            
            # cv2.imshow("Chunk", chunk)
            # cv2.waitKey(0)
            # Get the average pixel value of the chunk, normalized to 0-1
            avg = np.average(chunk) / 255

            if debug:
                print(avg)
                cv2.imshow("Chunk", chunk)
                cv2.waitKey(0)

            # If the average is withing DECODE_TOLLERANCE of 1 it's a 1, same for 0 and if it's not in the range we assume it's not data
            if avg > 1-DECODE_TOLLERANCE:
                rowList.append(1)
            elif avg < DECODE_TOLLERANCE:
                rowList.append(0)
            else:
                # It's outside the tollerance, it's not data
                return -1

        data.append(rowList)

    # Print the data
    #print(f"Data: {''.join([str(i) for i in data])}")

    return data


if __name__ == "__main__":
    # Decode all the images in the deformed folder
    decode_square(directory="deformed", debug=True)
