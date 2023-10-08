import argparse
import cv2
from easyocr import Reader

# Parse command-line arguments
parser = argparse.ArgumentParser(
    description="Extract text from an image using OCR")
parser.add_argument("--image", required=True, help="Path to input image")
parser.add_argument("--language", required=True,
                    help="Language code (3 letter ID)")
parser.add_argument("--output", required=True, help="Output file name")
args = parser.parse_args()

# Read input image using OpenCV
image_path = args.image
image = cv2.imread(image_path)

# Perform OCR using EasyOCR
langs = [args.language]
reader = Reader(langs)
results = reader.readtext(image)

# Extract and save text to the output file
output_file = args.output + "-" + args.language + ".txt"
with open(output_file, "w", encoding="utf-8") as file:
    for (bbox, text, prob) in results:
        file.write(text + "\n")
        print("[INFO] {:.4f}: {}".format(prob, text))

# Display the annotated image with bounding boxes around the detected text
for (bbox, text, prob) in results:
    (top_left, top_right, bottom_right, bottom_left) = bbox
    tl = (int(top_left[0]), int(top_left[1]))
    br = (int(bottom_right[0]), int(bottom_right[1]))
    cv2.rectangle(image, tl, br, (0, 0, 255), 2)
    cv2.putText(image, text, (tl[0], tl[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

# Display the annotated image
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
