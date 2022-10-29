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


def collapseEquivalences(equivalences, point, root, toResolve):
    toResolve[point] = False
    children = equivalences[point]
    equivalences[point] = [root]
    if children != []:
        for child in children:
            toResolve[child] = False
            # Remove the origin from the child's children
            try:
                equivalences[child].remove(point)
            except:
                pass
            collapseEquivalences(equivalences, child, root, toResolve)
    return toResolve

test_equivalences = {
    1: [2],
    2: [1,8],
    8: [2,7,6],
    7: [8],
    6: [8,9],
    9: [6],
    3: [],
    4: [5],
    5: [4],
    123123: [123123],
}

newResolve = collapseEquivalences(test_equivalences, 1, 1,{point:True for point in test_equivalences})

def readImage(filename):
    # Clean up the image to get a nice black and white image
    img = cv2.imread(filename)
    w, h = img.shape[:2]
    # Turn it into a BW image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur filter to remove minor noise
    blur = cv2.GaussianBlur(img, (3, 3), 0)

    # Threshold the image adaptively: this is convert to binary image in small chunks, choosing intermediate threshold values based on local statistics (avoids very white parts of the immage destroying everything else)
    
    # Justification of the noisy threshold you might see when looking at the thresholded images:
    #  You may see that in very same coloured regions of a picture, the thresholding might cause some binary noise to arrise
    #  This happens because there is very low contrast in the region
    #  This dosen't matter for our usecase since arround the edges of the white zones (where there is a hard black/white boundry), there is enough contrast to make the thresholding give us clear binary data, and the adaptive version means its locally clean with higher acuracy

    # the block size is 10% of the image min axis, 2 is the constant to subtract from the mean, not sure what it changes
    block_size = int(min(w, h)/10)
    # make block size odd (required by the function)
    block_size = block_size + 1 if block_size % 2 == 0 else block_size

    thresholdedImage = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, 2)

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

    pixel_group = [] # 2d array of each group, -1 means no group assinged
    # Populate the groups
    for y in range(h):
        pixel_group.append([])
        for x in range(w):
            pixel_group[-1].append(-1)

    group_equivallences = {}
    group_count = 0 # The number of groups taken into account
    for y, row in enumerate(pixels):
        for x, pixel in enumerate(row):
            if pixel == 1:
                continue
            indexes = set()
            # Check the pixel above and the one to the left and check their groups
            if y-1 >= 0 and pixels[y-1][x] == 0:
                indexes.add(pixel_group[y-1][x])
            if x-1 >= 0 and pixels[y][x-1] == 0:
                indexes.add(pixel_group[y][x-1])

            if len(indexes) == 1:
                # If there is only one group, assign it to this pixel
                pixel_group[y][x] = indexes.pop()

            # If the pixel connects 2 groups, merge them
            elif len(indexes) == 2:
                a,b = min(indexes), max(indexes)
                pixel_group[y][x] = a
                if a not in group_equivallences.get(b, []):
                    group_equivallences[b] = group_equivallences.get(b, []) + [a]
                if b not in group_equivallences.get(a, []):
                    group_equivallences[a] = group_equivallences.get(a, []) + [b]

            # If the pixel is in no other groups, create a new one
            else:
                pixel_group[y][x] = group_count
                group_equivallences[group_count] = []
                group_count += 1

    # Merge all the groups that are equivallent
    allGroups = list(group_equivallences.keys())
    toResolve = {group:True for group in allGroups}
    roots = []
    for group in allGroups:
        if toResolve[group] == True:
            roots.append(group)
            toResolve = collapseEquivalences(group_equivallences, group, group, toResolve)

    groups = {}
    # With the collappsed equivallence table, load each group into the groups array where everything is a list of pixels
    for y, row in enumerate(pixel_group):
        for x, group in enumerate(row):
            if group == -1:
                continue
            group = group_equivallences[group][0]
            if group not in groups:
                groups[group] = []
            groups[group].append((x,y))

    # Turn the dict into a list as expected
    groups = [groups[group] for group in groups]

    # Free all the data made for the group calculations
    del pixel_group, group_equivallences

    print(f"White zones to process: {len(groups)}")
    groupCounter = 0
    rects = set()
    for group in groups:
        print(f"Zones processed: {groupCounter}")
        groupCounter += 1
        # Check that the group is even big enough to be considered
        if len(group) < minRectSurface:
            continue

        nottaSquare = False
        # Find the pixels with the biggest and smallest x and y values, if more than 1 pixel have the smallest x, then take the one with the smallest y
        # Biggest y we take the smallest x, biggest x we take the biggest y and smallest y we take the biggest x (basically rotating clockwise)
        first = lambda a: a[0]
        last = lambda a: a[1] 
        
        minX, maxX = min(mins(group, key=first), key=last), max(
            maxs(group, key=first), key=last)
        minY, maxY = max(mins(group, key=last), key=first), min(
            maxs(group, key=last), key=first)

        # Check that all the points are different
        if not minX != maxX != minY != maxY:
            continue
        
        # The following points are on the lines matching their index
        points = [[maxY, maxX], [minX, maxY], [minX, minY], [minY, maxX]]

        # Find the cartesian line equations for all the lines representing the sides of the rectangle, in the form ax+by+c=0
        lines = [
            [maxY[1]-maxX[1], -(maxY[0]-maxX[0])], # Lower right line
            [minX[1]-maxY[1], -(minX[0]-maxY[0])], # Lower left side
            [minX[1]-minY[1], -(minX[0]-minY[0])], # Upper left side
            [minY[1]-maxX[1], -(minY[0]-maxX[0])]  # Upper right side
        ]

        # We have a and b now we need to find c, c = -(ax+by)
        for i in range(4):
            line = lines[i]
            line.append(-(points[i][0][0]*line[0]+points[i][0][1]*line[1]))

        # We check that the lines are continuous
        for i in range(4):
            line = lines[i]
            extremities = points[i]

            # Check that the line isn't vertical
            if line[1] != 0:
                for x in range(extremities[0][0], extremities[1][0]+1):
                    # y = -(ax+c)/b
                    y = round(-(line[0]*x+line[2])/line[1])
                    for offset in range(-LINE_PIXEL_TOLERANCE, LINE_PIXEL_TOLERANCE+1):
                        if y+offset < 0 or y+offset >= len(pixels):
                            continue
                        if pixels[y+offset][x] == 0:
                            break
                    else:  # If no pixels within the tolerance are white, then the line isn't continuous, so this group isn't a rectangle
                        nottaSquare = True
                        break
            else: # The line is vertical, and the x is equal to the x of one of the points on the line
                x = extremities[0][0]
                for y in range(extremities[0][1], extremities[1][1]+1):
                    for offset in range(-LINE_PIXEL_TOLERANCE, LINE_PIXEL_TOLERANCE+1):
                        if x+offset < 0 or x+offset >= len(pixels[y]):
                            continue
                        if pixels[y][x+offset] == 0:
                            break
                    else:
                        nottaSquare = True
                        break
            if nottaSquare:
                break
        else:
            # At this point, we conclude that it's a rectangle
            rects.add((minX, minY, maxX, maxY, frozenset(group)))
    
    # Add the image as a background to the plot
    # invert all the pixels
    show_pixels = [[1-pixel for pixel in row] for row in pixels]
    plt.imshow(show_pixels, cmap='gray', interpolation='nearest')
    print(f"{len(rects)} rectangles")
    #print("Plotting")
    for rect in rects:
        for i in range(4):
            plt.plot(*rect[i], marker="o", markersize=3,
                     markeredgecolor="red", markerfacecolor="red")
        #print("Rect done")
    # Flip the y axis so that the origin is in the top left
    plt.savefig("processed.png")
    # clear the plot
    plt.clf()
    #print("Done")

    # Return the list of quadrilaterals. Each quadrilateral is a list of coordinates. Each coordinate is a tuple
    # So it's a list of lists of tuples
    return [rect[:4] for rect in rects]


if __name__ == "__main__":
    readImage("printed.png")
