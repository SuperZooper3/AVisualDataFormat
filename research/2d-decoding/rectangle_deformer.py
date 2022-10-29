# Used to transform dectected rectangles into single output images

import cv2
import numpy as np
import os

# The size of the ouput square immage
outputSize = 200


# Where rectangleCoordinates is a list of lists of 2-tuples for coordinates (list of corners)
def squarifyRectangle(imageName, rectangleCoordinates):
    # Random filename slug
    filenameSlug = str(np.random.randint(1000000000))

    # Load the image
    img = cv2.imread(imageName)

    # Convert all the coordinates to a list of numpy matrices
    adjustedCoordinates = []
    for rectangle in rectangleCoordinates:
        # The order of the corners is not important as long as they are in a rectangular shape (like not a self intersecting shape)
        # This is important because otherise the transformations make very distorted images

        # Strategy: take the middle point of the polygon, calculate the angle of each point from the horizontal, and sort them by angle (smallest to largest)
        # This will give us the order of the points in the polygon. Inspired by https://math.stackexchange.com/a/978648.

        # The middle point is the average of the x and y coordinates of all the points
        middlePoint = np.mean(rectangle, axis=0)

        # Calculate the angle of each point from the vertical
        angles = []
        for point in rectangle:
            # Get the angle from the vertical
            angle = np.arctan2(point[1] - middlePoint[1],
                               point[0] - middlePoint[0])
            # Convert to degrees
            angle = np.rad2deg(angle)
            # Make it positive (0 to 360)
            angle = (angle + 360) % 360
            # Append it to the list
            angles.append(angle)

        # Sort the points by angle
        sortedPoints = [x for _, x in sorted(zip(angles, rectangle))]

        # Reorder it to be in the order: 1 2 4 3 (this just somehow apeard in my head).
        sortedPoints = [sortedPoints[0], sortedPoints[1],
                        sortedPoints[3], sortedPoints[2]]

        # Append it to the list
        adjustedCoordinates.append(np.array(sortedPoints, dtype=np.float32))

    # Make the mapped coordinates matrix (where the corners will be mapped to in the output image)
    mappedCoordinates = np.float32(
        [[0, 0], [outputSize, 0], [0, outputSize], [outputSize, outputSize]])

    # Clear out the deformed folder
    for filename in os.listdir("2d-decoding/deformed"):
        if filename.endswith(".png"):
            os.remove("2d-decoding/deformed/" + filename)

    # Transform each rectangle
    for i, rectangle in enumerate(adjustedCoordinates):
        # Get the transformation matrix (some magic stuff right here)
        transformationMatrix = cv2.getPerspectiveTransform(
            rectangle, mappedCoordinates)

        # Transform the image
        transformedImage = cv2.warpPerspective(
            img, transformationMatrix, (outputSize, outputSize))

        # Save the image
        cv2.imwrite(f"2d-decoding/deformed/deformed{i}.png", transformedImage)
        print("Saved image")
        #cv2.imwrite(f"deformed.png", transformedImage)

    # TODO: pass this on in a better way than just saving a file :/
