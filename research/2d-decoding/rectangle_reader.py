# An interface to detect rectangles in images (webcam or file)

# import the opencv library for webcam access
import cv2
from .rectangle_detector import readImage
from .rectangle_deformer import squarifyRectangle
from .square_decoder import decode_square
import numpy as np


def process(filename, tryAgain = True):
    corners = readImage(filename)
    squarifyRectangle(filename, corners)
    out_data = decode_square(directory="2d-decoding/deformed")
    if len(out_data) == 0 and tryAgain:
        # If data isn't found, mabye the rectangle algorithm failed, try again with a 45 degree rotation
        # Taken from https://pyimagesearch.com/2017/01/02/rotate-images-correctly-with-opencv-and-python/
        img = cv2.imread(filename)
        (h, w) = img.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        # grab the rotation matrix (applying the negative of the
        # angle to rotate clockwise), then grab the sine and cosine
        # (i.e., the rotation components of the matrix)
        M = cv2.getRotationMatrix2D((cX, cY), -45, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        # compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))
        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY
        # perform the actual rotation and return the image
        img =  cv2.warpAffine(img, M, (nW, nH))
        cv2.imwrite("rotated.png", img)
        process("rotated.png", tryAgain=False)


def main():
    mode = input(
        "Enter 'file' to read from a file, or 'webcam' to read from a webcam: ")
    if mode == "file":
        filename = input("Enter the filename: ")
        process(filename)
    elif mode == "webcam":
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("Square reader")
        print("Escape to close. Space to take a picture and process it.")
        try:
            while True:
                ret, frame = cam.read()
                if not ret:
                    print("failed to grab frame")
                    break
                cv2.imshow("Square reader", frame)
                k = cv2.waitKey(1)
                if k % 256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break
                if k % 256 == 32:
                    # Space pressed
                    cv2.imwrite("webcam.png", frame)
                    print("Capture taken, processing...")
                    process("webcam.png")
        finally:
            cam.release()
            cv2.destroyAllWindows()
    else:
        print("Invalid mode")


if __name__ == "__main__":
    main()
