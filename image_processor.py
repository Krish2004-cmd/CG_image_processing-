import cv2
import numpy as np
from tkinter import Tk, Label, Button, filedialog, Canvas
from PIL import Image, ImageTk

class ImageProcessor:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Processing Filters")
        
        self.label = Label(master, text="Upload an Image")
        self.label.pack()

        self.upload_button = Button(master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.gray_button = Button(master, text="Apply Grayscale", command=self.apply_grayscale)
        self.gray_button.pack()

        self.sepia_button = Button(master, text="Apply Sepia", command=self.apply_sepia)
        self.sepia_button.pack()

        self.canvas = Canvas(master, width=400, height=400)
        self.canvas.pack()

        self.image_path = None
        self.image = None

    def upload_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.image = cv2.imread(self.image_path)
            self.show_image(self.image)

    def show_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Resize image while maintaining aspect ratio
        height, width, _ = img.shape
        aspect_ratio = width / height
        
        if width > canvas_width or height > canvas_height:
            if aspect_ratio > 1:  # Wider than tall
                new_width = canvas_width
                new_height = int(canvas_width / aspect_ratio)
            else:  # Taller than wide
                new_height = canvas_height
                new_width = int(canvas_height * aspect_ratio)
        else:
            new_width = width
            new_height = height

        resized_img = cv2.resize(img, (new_width, new_height))
        img = Image.fromarray(resized_img)
        img = ImageTk.PhotoImage(img)
        
        self.canvas.create_image(0, 0, anchor='nw', image=img)
        self.canvas.image = img

    def apply_grayscale(self):
        if self.image is not None:
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.show_image(gray_image)

    def apply_sepia(self):
        if self.image is not None:
            sepia_filter = np.array([[0.272, 0.534, 0.131],
                                      [0.349, 0.686, 0.168],
                                      [0.393, 0.769, 0.189]])
            sepia_image = cv2.transform(self.image, sepia_filter)
            sepia_image = np.clip(sepia_image, 0, 255).astype(np.uint8)
            self.show_image(sepia_image)

if __name__ == "__main__":
    root = Tk()
    app = ImageProcessor(root)
    root.mainloop()
