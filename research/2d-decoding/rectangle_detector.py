# Backend code to find the rectangles

from PIL import Image
import matplotlib.pyplot as plt
import cv2

LINE_PIXEL_TOLERANCE = 5


def mins(items, key=lambda a: a):
    items = list(items)
    minV = key(items[0])
    minItems = [items[0]]
    for i in range(1, len(items)):
        val = key(items[i])
        if val == minV:
            minItems.append(items[i])
        elif val < minV:
            minV = val
            minItems = [items[i]]
    return minItems


def maxs(items, key=lambda a: a):
    items = list(items)
    maxV = key(items[0])
    maxItems = [items[0]]
    for i in range(1, len(items)):
        val = key(items[i])
        if val == maxV:
            maxItems.append(items[i])
        elif val > maxV:
            maxV = val
            maxItems = [items[i]]
    return maxItems


def readImage(filename):
    # Clean up the image to get a nice black and white image
    img = cv2.imread(filename)
    w, h = img.shape[:2]
    # Turn it into a BW image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur filter to remove minor noise
    blur = cv2.GaussianBlur(img, (3, 3), 0)

    block_size = int(min(w, h)/10)
    # make block size odd
    block_size = block_size + 1 if block_size % 2 == 0 else block_size

    # Threshold the image adaptively: this is convert to binary image in small chunks, choosing intermediate threshold values based on local statistics (avoids very white parts of the immage destroying everything else)
    # the block size is 10% of the image min axis, 2 is the constant to subtract from the mean, not sure what it changes
    thresholdedImage = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, 2)
    # Justification of the noisy threshold:
    #  You may see that in very same coloured regions of a picture, the thresholding might cause some binary noise to arrise
    #  This happens because there is very low contrast in the region
    #  This dosen't matter for our usecase since arround the edges of the white zones (where there is a hard black/white boundry), there is enough contrast to make the thresholding give us clear binary data, and the adaptive version means its locally clean with higher acuracy

    # Invert the thresholded image because black is a 1 and white is a 0
    # FIXME: rewrite entire script to use cv2 images instead of PIL images to avoid saving
    cv2.imwrite("thresholded.png", thresholdedImage)

    im = Image.open("thresholded.png").convert("L")
    w, h = im.size
    pixels = list(im.getdata())

    # reduce them all to 0 or 1 and flipped
    pixels = [0 if pixel > 127 else 1 for pixel in pixels]

    pixels = [pixels[i:i+w] for i in range(0, len(pixels), w)]

    # A rectangle must be at least 0.3% of the image size
    minRectSurface = (w*h)*0.3/100

    groups = []
    for y, row in enumerate(pixels):
        for x, pixel in enumerate(row):
            if pixel == 1:
                continue
            indexes = set()
            # Check the pixel above and the one to the left and check their groups
            if y-1 >= 0:
                for index, group in enumerate(groups):
                    if (x, y-1) in group:
                        group.add((x, y))
                        indexes.add(index)
                        break
            if x-1 >= 0:
                for index, group in enumerate(groups):
                    if (x-1, y) in group:
                        group.add((x, y))
                        indexes.add(index)
                        break
            # If the pixel connects 2 groups, merge them
            if len(indexes) == 2:
                newGroups = [groups[i] for i in indexes]
                groups.append(newGroups[0] | newGroups[1])
                # Remove the smaller groups, starting with the highest index to avoid off by 1 errors
                groups.pop(max(indexes))
                groups.pop(min(indexes))
            # If the pixel is in no other groups, create a new one
            elif len(indexes) == 0:
                groups.append({(x, y)})
    #print(len(groups), "groups")
    #print(sum([len(a) for a in groups]), "pixels")

    rects = set()
    for group in groups:
        # Check that the group is even big enough to be considered
        if len(group) < minRectSurface:
            continue

        nottaSquare = False
        # Find the pixels with the biggest and smallest x and y values, if more than 1 pixel have the smallest x, then take the one with the smallest y
        # Biggest y we take the smallest x, biggest x we take the biggest y and smallest y we take the biggest x (basically rotating clockwise)
        minX, maxX = min(mins(group, key=lambda a: a[0]), key=lambda a: a[1]), max(
            maxs(group, key=lambda a: a[0]), key=lambda a: a[1])
        minY, maxY = max(mins(group, key=lambda a: a[1]), key=lambda a: a[0]), min(
            maxs(group, key=lambda a: a[1]), key=lambda a: a[0])

        # Check that all the points are different
        if not minX != maxX != minY != maxY:
            continue

        # Line equations are y = m(x-a)+b, with A(a, b) being on the line and m being the slope
        try:
            # Lower right side
            def line(a): return (maxY[1]-maxX[1]) / \
                (maxY[0]-maxX[0])*(a - maxX[0]) + maxX[1]
            for x in range(maxY[0], maxX[0]+1):
                y = round(line(x))
                for offset in range(-LINE_PIXEL_TOLERANCE, LINE_PIXEL_TOLERANCE+1):
                    if y+offset < 0 or y+offset >= len(pixels):
                        continue
                    if pixels[y+offset][x] == 0:
                        break
                else:  # If no pixels within the tolerance are white, then the line isn't continuous, so this group isn't a rectangle
                    nottaSquare = True
                    break
        except ZeroDivisionError:
            continue
        if nottaSquare:
            continue

        try:
            if minX[0]-maxY[0] != 0:
                def line(a): return (
                    minX[1]-maxY[1])/(minX[0]-maxY[0])*(a - minX[0]) + minX[1]  # Lower left side
                for x in range(minX[0], maxY[0]+1):
                    y = round(line(x))
                    for offset in range(-LINE_PIXEL_TOLERANCE, LINE_PIXEL_TOLERANCE+1):
                        if y+offset < 0 or y+offset >= len(pixels):
                            continue
                        if pixels[y+offset][x] == 0:
                            break
                    else:  # If no pixels within the tolerance are white, then the line isn't continuous, so this group isn't a rectangle
                        nottaSquare = True
                        break
            else:
                for y in range(minX[1], maxY[1]+1):
                    for offset in range(-LINE_PIXEL_TOLERANCE, LINE_PIXEL_TOLERANCE+1):
                        if minX[0]+offset < 0 or minX[0]+offset >= len(pixels[y]):
                            continue
                        if pixels[y][minX[0]+offset] == 0:
                            break
                    else:
                        nottaSquare = True
                        break
        except ZeroDivisionError:
            continue
        if nottaSquare:
            continue

        try:
            def line(a): return (
                minX[1]-minY[1])/(minX[0]-minY[0])*(a - minX[0]) + minX[1]  # Upper left side
            for x in range(minX[0], minY[0]+1):
                y = round(line(x))
                for offset in range(-LINE_PIXEL_TOLERANCE, LINE_PIXEL_TOLERANCE+1):
                    if y+offset < 0 or y+offset >= len(pixels):
                        continue
                    if pixels[y+offset][x] == 0:
                        break
                else:  # If no pixels within the tolerance are white, then the line isn't continuous, so this group isn't a rectangle
                    nottaSquare = True
                    break
        except ZeroDivisionError:
            continue
        if nottaSquare:
            continue

        try:
            if minY[0]-maxX[0] != 0:
                # Upper right side
                def line(a): return (minY[1]-maxX[1]) / \
                    (minY[0]-maxX[0])*(a - maxX[0]) + maxX[1]
                for x in range(minY[0], maxX[0]+1):
                    y = round(line(x))
                    for offset in range(-LINE_PIXEL_TOLERANCE, LINE_PIXEL_TOLERANCE+1):
                        if y+offset < 0 or y+offset >= len(pixels):
                            continue
                        if pixels[y+offset][x] == 0:
                            break
                    else:  # If no pixels within the tolerance are white, then the line isn't continuous, so this group isn't a rectangle
                        nottaSquare = True
                        break
            else:
                for y in range(minY[1], maxX[1]+1):
                    for offset in range(-LINE_PIXEL_TOLERANCE, LINE_PIXEL_TOLERANCE+1):
                        if minY[0]+offset < 0 or minY[0]+offset >= len(pixels[y]):
                            continue
                        if pixels[y][minY[0]+offset] == 0:
                            break
                    else:
                        nottaSquare = True
                        break
        except ZeroDivisionError:
            continue
        if nottaSquare:
            continue

        # At this point, we conclude that it's a rectangle
        rects.add((minX, minY, maxX, maxY, frozenset(group)))

    # Add the image as a background to the plot
    # invert all the pixels
    show_pixels = [[1-pixel for pixel in row] for row in pixels]
    plt.imshow(show_pixels, cmap='gray', interpolation='nearest')
    print(len(rects), "rectangles")
    print("Plotting")
    for rect in rects:
        for i in range(4):
            plt.plot(*rect[i], marker="o", markersize=3,
                     markeredgecolor="red", markerfacecolor="red")
        print("Rect done")
    # Flip the y axis so that the origin is in the top left
    plt.savefig("processed.png")
    # clear the plot
    plt.clf()
    print("Done")

    # Return the rectangles as a list of lists of tuples
    return [rect[:4] for rect in rects]


if __name__ == "__main__":
    readImage("printed.png")
