# The reader script takes in an image file, and analyses it to find a barcode and return the data encoded in it.
from decode import decode
from PIL import Image
from math import floor, log2

dataTypeReverse = {
    "0,0": "num",
    "0,1": "ascii",
    "1,0": "utf8",
    "1,1": "raw"
}


def readCode(imgFilename):
    im = Image.open(imgFilename).convert("L")
    w,h = im.size
    pixels = list(im.getdata()) # The basic version only works for files with only the barcode, so taking just the first line works
    
    # Convert all pixels to their closes 0 or 1 value, inverted because 1 is a bar and 0 is a space
    pixels = [0 if pixel > 128 else 1 for pixel in pixels]

    # Save the converted pixels to a new image for debugging
    im = Image.new("1", (w,h), color=1)
    im.putdata(pixels)
    im.save("converted.png")

    # Turn the full list of pixels into a 2d array
    pixels = [pixels[i:i+w] for i in range(0, len(pixels), w)]

    output = "No data found"

    # Insatead of just reading the top row, read the image row by row and print all data found
    for row in pixels:
        # Measure the width of a bar
        #  The start of any barcode is 101, so we can measure the width in pixels of the 0, and then take that as the width of a bar
        blackStart = -1
        whiteStart = None
        whiteEnd = None
        reader = 0

        doubleBreak = False
        while whiteEnd == None:
            if reader >= len(row):
                doubleBreak = True
                break
            if row[reader] == 1 and blackStart == -1:
                blackStart = reader
            if blackStart != -1 and row[reader] == 0 and whiteStart == None:
                whiteStart = reader
            
            if blackStart != -1 and row[reader] == 1 and whiteStart != None:
                whiteEnd = reader

            reader += 1

        if doubleBreak:
            #print("Nothing")
            continue

        barWidth = whiteEnd - whiteStart

        # Read the headers
        data = []

        currentRegion = 1 # Starts with black
        regionWidth = 0
        for pixel in row[blackStart:]: # We'll read until the end, and then only interpret the data we need
            if pixel == currentRegion:
                regionWidth += 1
            else:
                # Write the region to the data
                data.extend([currentRegion] * round(regionWidth / barWidth)) # This rounding is to try and get the closest number of bars
                currentRegion = pixel
                regionWidth = 1

        # Write the final data
        data.extend([currentRegion] * round(regionWidth / barWidth))

        dataType = dataTypeReverse[",".join([str(v) for v in data[4:6]])]

        dataLength = int("".join([str(v) for v in data[6:14]]), 2)

        checksumLength = floor(log2(dataLength))+1

        checksum = int("".join([str(v) for v in data[14:14+checksumLength]]), 2)

        dataRangeStart = 14+checksumLength
        dataRangeEnd = dataRangeStart + dataLength * 8

        outdata = data[dataRangeStart:dataRangeEnd]
       
        # check that it correctly starts with 1011
        if data[0:4] != [1,0,1,1]:
            continue

        # check that it correctly ends with 0101.
        if data[dataRangeEnd:dataRangeEnd + 4] != [0,1,0,1]:
            print("Invalid end")
            continue

        # check that the checksum is correct
        checksumValue = 0
        for i in range(dataLength*8):
            checksumValue += (i+1)**outdata[i]
        checksumValue %= 2**checksumLength

        if checksumValue != checksum:
            print("Checksum failed")
            continue

        # Conver the data into a string, knowing the data is ascii in binary
        output = decode(outdata)

    print(f"Extracted data: {''.join(output)}")
    return int(''.join(map(str, outdata)), 2).to_bytes(len(outdata) // 8, byteorder='big')


def main():
    readCode("printed.png")

if __name__ == "__main__":
    main()
