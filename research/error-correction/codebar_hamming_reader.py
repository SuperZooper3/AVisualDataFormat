from codebar_code import reader
import hamming
import cv2

def main():
    mode = input("Enter 'file' to read from a file, or 'webcam' to read from a webcam: ")
    if mode == "file":
        filename = input("Enter the filename: ")
        data = reader.readCode(filename)
        payload = hamming.hamming_decode([int(i) for i in data])
        assert payload != -1, "Too many errors"
        print(int("".join([str(s) for s in payload]),2))

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
                data = reader.readCode("webcam.png")
                try:
                    payload = hamming.hamming_decode([int(i) for i in data])
                    print(int("".join([str(s) for s in payload]),2))
                except:
                    pass
        finally:
            cam.release()
            cv2.destroyAllWindows()
    else:
        print("Invalid mode")

if __name__ == "__main__":
    main()