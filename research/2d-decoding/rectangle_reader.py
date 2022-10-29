# An interface to detect rectangles in images (webcam or file)

# import the opencv library for webcam access
import cv2
from .rectangle_detector import readImage
from .rectangle_deformer import squarifyRectangle
from .square_decoder import decode_square


def process(filename):
    corners = readImage(filename)
    squarifyRectangle(filename, corners)
    decode_square(directory="2d-decoding/deformed")


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
