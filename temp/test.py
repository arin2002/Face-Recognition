from easyocr import Reader
import argparse
import cv2
from PIL import Image
import pytesseract

dire = input("Type full path to image you want to convert to text:")
im = Image.open(dire)

language = input("Type the language of the scanned document (3 letter ID):")
text = pytesseract.image_to_string(im, lang=language)
filename = input("Type output file name:")
file1 = open(filename+"-"+language+".txt", "w")
file1.write(text)
file1.close()
print("Done...")

parser = argparse.ArgumentParser()
parser.add_argument("--image", required=True,
                    help="path to input image")
parser.add_argument("--langs", type=str, default="en",
                    help="coma separated list of languages for our OCR")
parser.add_argument("-g", "--gpu", type=int, default=-1,
                    help="whether or not GPU should be used")
args = vars(parser.parse_args())
langs = args["langs"].split(",")
print("[INFO] Using the following languages: {}".format(langs))
image = cv2.imread(args["image"])
print("[INFO] Performing OCR on input image...")
reader = Reader(langs, gpu=args["gpu"] > 0)
results = reader.readtext(image)
for (bbox, text, prob) in results:
    print("[INFO] {:.4f}: {}".format(prob, text))
    (top_left, top_right, bottom_right, bottom_left) = bbox
    tl = (int(top_left[0]), int(top_left[1]))
    tr = (int(top_right[0]), int(top_right[1]))
    br = (int(bottom_right[0]), int(bottom_right[1]))
    bl = (int(bottom_left[0]), int(bottom_left[1]))

    cv2.rectangle(image, tl, br, (0, 0, 255), 2)
    cv2.putText(image, text, (tl[0], tl[1]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

cv2.imshow("Image", image)
cv2.waitKey(0)
