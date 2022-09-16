# The reader script takes in an image file, and analyses it to find a barcode and return the data encoded in it.
from decode import decode
from PIL import Image

def readCode(imgFilename):
    im = Image.open(imgFilename).convert("1")
    w,h = im.size
    pixels = list(im.getdata()) # The basic version only works for files with only the barcode, so taking just the first line works
    # Convert all pixels to their closes 0 or 1 value, inverted because 1 is a bar and 0 is a space
    pixels = [0 if pixel > 128 else 1 for pixel in pixels]

    # Turn the full list of pixels into a 2d array
    pixels = [pixels[i:i+w] for i in range(0, len(pixels), w)]

    topRow = pixels[0]

    # Measure the width of a bar
    #  The start of any barcode is 101, so we can measure the width in pixels of the 0, and then take that as the width of a bar
    blackStart = -1
    whiteStart = None
    whiteEnd = None
    reader = 0
    while whiteEnd == None:
        if topRow[reader] == 1 and blackStart == -1:
            blackStart = reader
        if blackStart != -1 and topRow[reader] == 0 and whiteStart == None:
            whiteStart = reader
        
        if blackStart != -1 and topRow[reader] == 1 and whiteStart != None:
            whiteEnd = reader

        reader += 1

    barWidth = whiteEnd - whiteStart

    # Read the entire barcode from start to finish
    #   As we read, we'll measure the width of the current region
    #   Once the region changes, add the width to the data
    data = []

    currentRegion = topRow[0]
    regionWidth = 0
    for pixel in topRow[blackStart:]:
        if pixel == currentRegion:
            regionWidth += 1
        else:
            # Write the region to the data
            data.extend([currentRegion] * (regionWidth // barWidth))
            currentRegion = pixel
            regionWidth = 1

    # Write the final data
    data.extend([currentRegion] * (regionWidth // barWidth))

    # Remove the start and end markers
    data = data[3:-3]

    # Conver the data into a string, knowing the data is ascii in binary
    output = decode(data)

    print(f"Extracted data: {''.join(output)}")

readCode("printed.png")