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

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

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

        detected_text = ""
        for (_, text, _) in results:
            detected_text += text + "\n"

        self.result_label.config(text=detected_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
