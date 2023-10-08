import tkinter as tk
from tkinter import filedialog
import cv2
from easyocr import Reader


class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Application")

        self.langs_label = tk.Label(root, text="Languages:")
        self.langs_label.pack()

        self.langs_entry = tk.Entry(root)
        self.langs_entry.pack()

        self.browse_button = tk.Button(
            root, text="Browse", command=self.browse_image)
        self.browse_button.pack()

        self.process_button = tk.Button(
            root, text="Process Image", command=self.process_image)
        self.process_button.pack()

    def browse_image(self):
        file_path = filedialog.askopenfilename()
        self.image = cv2.imread(file_path)

    def process_image(self):
        langs = self.langs_entry.get().split(",")
        reader = Reader(langs)
        results = reader.readtext(self.image)

        for (bbox, text, prob) in results:
            (top_left, top_right, bottom_right, bottom_left) = bbox
            tl = (int(top_left[0]), int(top_left[1]))
            br = (int(bottom_right[0]), int(bottom_right[1]))
            cv2.rectangle(self.image, tl, br, (0, 0, 255), 2)
            cv2.putText(self.image, text, (tl[0], tl[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Processed Image", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
