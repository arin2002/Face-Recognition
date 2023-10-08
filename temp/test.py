from easyocr import Reader
import argparse
import cv2

# Argument parser setup
parser = argparse.ArgumentParser()
parser.add_argument("--image", required=True, help="Path to input image")
parser.add_argument("--langs", type=str, default="en",
                    help="Comma-separated list of languages for OCR")
parser.add_argument("-g", "--gpu", type=int, default=-1,
                    help="Whether or not GPU should be used")
args = parser.parse_args()

langs = args.langs.split(",")
print("[INFO] Using the following languages: {}".format(langs))

# Read input image
image = cv2.imread(args.image)
print("[INFO] Performing OCR on input image...")

reader = Reader(langs, gpu=args.gpu > 0)
results = reader.readtext(image)

for (bbox, text, prob) in results:
    print("[INFO] {:.4f}: {}".format(prob, text))
    (top_left, top_right, bottom_right, bottom_left) = bbox
    tl = (int(top_left[0]), int(top_left[1]))
    br = (int(bottom_right[0]), int(bottom_right[1]))

    cv2.rectangle(image, tl, br, (0, 0, 255), 2)
    cv2.putText(image, text, (tl[0], tl[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

# Display the processed image with bounding boxes and detected text
cv2.imshow("Processed Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
