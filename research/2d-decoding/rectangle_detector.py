from PIL import Image
import matplotlib.pyplot as plt

LINE_PIXEL_TOLERANCE = 1

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
    im = Image.open(filename).convert("L")
    w,h = im.size
    pixels = list(im.getdata())

    # Convert all pixels to their closes 0 or 1 value, inverted because 1 is a bar and 0 is a space
    pixels = [0 if pixel > 127 else 1 for pixel in pixels]

    im = Image.new("1", (w,h), color=1)
    im.putdata(pixels)
    im.save("converted.png")

    pixels = [pixels[i:i+w] for i in range(0, len(pixels), w)]

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
    print(len(groups), "groups")
    print(sum([len(a) for a in groups]), "pixels")

    rects = set()
    for group in groups:
        nottaSquare = False
        # Find the pixels with the biggest and smallest x and y values, if more than 1 pixel have the smallest x, then take the one with the smallest y
        # Biggest y we take the smallest x, biggest x we take the biggest y and smallest y we take the biggest x (basically rotating clockwise)
        minX, maxX = min(mins(group, key = lambda a: a[0]), key = lambda a: a[1]), max(maxs(group, key = lambda a: a[0]), key=lambda a: a[1])
        minY, maxY = max(mins(group, key = lambda a: a[1]), key=lambda a: a[0]), min(maxs(group, key = lambda a: a[1]), key = lambda a: a[0])

        # Check that all the points are different
        if not minX != maxX != minY != maxY:
            continue

        # Line equations are y = m(x-a)+b, with A(a, b) being on the line and m being the slope
        try:
            line = lambda a: (maxY[1]-maxX[1])/(maxY[0]-maxX[0])*(a - maxX[0]) + maxX[1] # Lower right side
            for x in range(maxY[0], maxX[0]+1):
                y = round(line(x))
                for offset in range(-LINE_PIXEL_TOLERANCE, LINE_PIXEL_TOLERANCE+1):
                    if y+offset < 0 or y+offset >= len(pixels):
                        continue
                    if pixels[y+offset][x] == 0:
                        break
                else: # If no pixels within the tolerance are white, then the line isn't continuous, so this group isn't a rectangle
                    nottaSquare = True
                    break
        except ZeroDivisionError:
            continue
        if nottaSquare:
            continue
        
        try:
            if minX[0]-maxY[0] != 0:
                line = lambda a: (minX[1]-maxY[1])/(minX[0]-maxY[0])*(a - minX[0]) + minX[1] # Lower left side
                for x in range(minX[0], maxY[0]+1):
                    y = round(line(x))
                    for offset in range(-LINE_PIXEL_TOLERANCE, LINE_PIXEL_TOLERANCE+1):
                        if y+offset < 0 or y+offset >= len(pixels):
                            continue
                        if pixels[y+offset][x] == 0:
                            break
                    else: # If no pixels within the tolerance are white, then the line isn't continuous, so this group isn't a rectangle
                        nottaSquare = True
                        break
            else:
                for y in range(minX[1], maxY[1]+1):
                    for offset in range(-LINE_PIXEL_TOLERANCE, LINE_PIXEL_TOLERANCE+1):
                        if minX[0]+offset < 0 or minX[0]+offset >= len(pixels[minX[0]]):
                            continue
                        if pixels[y+offset][minX[0]+offset] == 0:
                            break
                    else:
                        nottaSquare = True
                        break
        except ZeroDivisionError:
            continue
        if nottaSquare:
            continue

        try:
            line = lambda a: (minX[1]-minY[1])/(minX[0]-minY[0])*(a - minX[0]) + minX[1] # Upper left side
            for x in range(minX[0], minY[0]+1):
                y = round(line(x))
                for offset in range(-LINE_PIXEL_TOLERANCE, LINE_PIXEL_TOLERANCE+1):
                    if y+offset < 0 or y+offset >= len(pixels):
                        continue
                    if pixels[y+offset][x] == 0:
                        break
                else: # If no pixels within the tolerance are white, then the line isn't continuous, so this group isn't a rectangle
                    nottaSquare = True
                    break
        except ZeroDivisionError:
            continue
        if nottaSquare:
            continue
        
        try:
            if minY[0]-maxX[0] != 0:
                line = lambda a: (minY[1]-maxX[1])/(minY[0]-maxX[0])*(a - maxX[0]) + maxX[1] # Upper right side
                for x in range(minY[0], maxX[0]+1):
                    y = round(line(x))
                    for offset in range(-LINE_PIXEL_TOLERANCE, LINE_PIXEL_TOLERANCE+1):
                        if y+offset < 0 or y+offset >= len(pixels):
                            continue
                        if pixels[y+offset][x] == 0:
                            break
                    else: # If no pixels within the tolerance are white, then the line isn't continuous, so this group isn't a rectangle
                        nottaSquare = True
                        break
            else:
                for y in range(minY[1], maxX[1]+1):
                    for offset in range(-LINE_PIXEL_TOLERANCE, LINE_PIXEL_TOLERANCE+1):
                        if minY[0]+offset < 0 or minY[0]+offset >= len(pixels[minY[0]]):
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
    
    print(len(rects), "rectangles")
    print("Plotting")
    for rect in rects:
        for point in rect[4]:
            plt.plot(*point, marker="o", markersize=1, markeredgecolor="black", markerfacecolor="black")
        for i in range(4):
            plt.plot(*rect[i], marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
        print("Rect done")
    print("Showing")

    # Flip the y axis so that the origin is in the top left
    plt.gca().invert_yaxis()
    plt.show()
        

if __name__ == "__main__":
    readImage("printed.png")