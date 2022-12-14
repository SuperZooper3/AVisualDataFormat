# The reader script takes in an image file, and analyses it to find a barcode and return the data encoded in it.
from codebar_code.decode import decode
from PIL import Image
from math import floor, log2

# import the opencv library for webcam access
import cv2
import webbrowser

debug = False

dataTypeReverse = {
    "0,0": "num",
    "0,1": "utf8",
    "1,0": "url",
    "1,1": "raw"
}

openedUrls = []

def readCode(imgFilename):
    global openedUrls

    rotationAngles = [0, 180, 90, 270] # Counter-clockwise
    # Extra angles below make it slower, but it could read more codes
    # rotationAngles.extend(range(45, 360, 90))
    # for rotation in range(8):
    #     rotationAngles.extend(range(15+45*rotation, 45*(rotation+1), 15))
    # for rotation in range(24):
    #     rotationAngles.extend(range(5+15*rotation, 15*(rotation+1), 5))
    
    output = None
    origIm = Image.open(imgFilename).convert("L")
    for deg in rotationAngles:
        im = origIm.copy().rotate(deg, expand=True, fillcolor=(255))
        w,h = im.size
        pixels = list(im.getdata()) # The basic version only works for files with only the barcode, so taking just the first line works
        
        # Convert all pixels to their closes 0 or 1 value, inverted because 1 is a bar and 0 is a space
        pixels = [0 if pixel > 127 else 1 for pixel in pixels] # hand tested conversion threshold

        # Save the converted pixels to a new image for debugging
        im = Image.new("1", (w,h), color=1)
        im.putdata(pixels)
        im.save("converted.png")

        # Turn the full list of pixels into a 2d array
        pixels = [pixels[i:i+w] for i in range(0, len(pixels), w)]

        # Instead of just reading the top row, read the image row by row and print all data found
        for row in pixels:
            blackStarts = []
            currentBlack = False
            for index in range(len(row)):
                if row[index] == 1 and currentBlack == False:
                    blackStarts.append(index)
                    currentBlack = True
                if row[index] == 0:
                    currentBlack = False
            for start in blackStarts:
                # Measure the width of a bar
                #  The start of any barcode is 101, so we can measure the width in pixels of the 0, and then take that as the width of a bar
                blackStart = -1
                whiteStart = None
                whiteEnd = None
                reader = start

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
                    # print("Nothing")
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

                if len(data) < 18:
                    # Not enough data to be a barcode
                    continue

                # Before anything, check for the start region
                # check that it correctly starts with 1011
                if data[0:4] != [1,0,1,1]:
                    if data[-5:-1:-1] == [1,0,1,1]:
                        if debug: print("Potential backwards reading")
                        data = data[::-1]
                    else:
                        if debug: print("invalid start")
                        continue

                dataBitsString = ",".join([str(v) for v in data[4:6]])
                if dataBitsString not in dataTypeReverse:
                    # print("Invalid data type")
                    continue
                
                dataType = dataTypeReverse[dataBitsString]
                
                dataLength = int("".join([str(v) for v in data[6:14]]), 2)
                if dataLength <= 0:
                    # No data
                    continue

                checksumLength = floor(log2(dataLength))+1

                checksum = int("".join([str(v) for v in data[14:14+checksumLength]]), 2)

                dataRangeStart = 14+checksumLength
                dataRangeEnd = dataRangeStart + dataLength * 8

                outdata = data[dataRangeStart:dataRangeEnd]

                # check that it correctly ends with 0101.
                if data[dataRangeEnd:dataRangeEnd + 4] != [0,1,0,1]:
                    if debug: print("Invalid end")
                    continue
                
                # check that the checksum is correct
                checksumValue = 0
                for i in range(dataLength*8):
                    checksumValue += (i+1)**outdata[i]
                checksumValue %= 2**checksumLength

                if checksumValue != checksum:
                    if debug: print("Checksum failed")
                    continue

                # Convert the data into a string, knowing the data is ascii in binary
                if dataType != "raw":
                    output = decode(outdata, type=dataType)
                    if dataType == "url":
                        if output not in openedUrls:
                            webbrowser.open(output)
                            openedUrls.append(output)
                
                elif dataType == "raw":
                    s = "".join(map(str, outdata))
                    #b = int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')
                    output = s # TEMPORARY, RETURN JUST A STRING OF 1s AND 0s

                break
            else:
                continue
            break
        else:
            continue
        break

    if output == None:
        print("No data found")
    else:
        try:
            print(f"Extracted data: {output}")
        except TypeError:
            print(f"Extracted data may contain binary data")
    
    return output

def main():
    mode = input("Enter 'file' to read from a file, or 'webcam' to read from a webcam: ")
    if mode == "file":
        filename = input("Enter the filename: ")
        readCode(filename)
    elif mode == "webcam":
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("Barcode reader")
        print("Escape to close")
        img_counter = 0
        try:
            while True:
                ret, frame = cam.read()
                if not ret:
                    print("failed to grab frame")
                    break
                cv2.imshow("Barcode reader", frame)
                k = cv2.waitKey(1)
                if k%256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break
                cv2.imwrite("webcam.png", frame)
                readCode("webcam.png")
        finally:
            cam.release()
            cv2.destroyAllWindows()
    else:
        print("Invalid mode")
    

if __name__ == "__main__":
    main()
