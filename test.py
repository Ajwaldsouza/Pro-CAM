import tkinter as tk
from tkinter import filedialog
from picamera2 import Picamera2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time
import datetime

class ImageCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Capture and Labeling")

        # ... (Rest of the GUI setup remains the same)

        self.camera = Picamera2()
        config = self.camera.configure(picamera2.PreviewConfig())
        self.camera.start_preview(config)

    def capture_image(self):
        # ... (Label and destination input validation remains the same)

        try:
            # Capture image
            self.camera.capture_image("temp.jpg")

            # Load image and add label
            image = Image.open("temp.jpg")
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 24)
            text_width, text_height = draw.textsize(label, font=font)
            image_width, image_height = image.size
            draw.text((image_width - text_width - 10, image_height - text_height - 10), label, font=font, fill='white')

            # Display preview
            photo = ImageTk.PhotoImage(image)
            self.preview_label.config(image=photo)
            self.preview_label.image = photo

            # Save image
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{label}_{timestamp}.jpg"
            image.save(f"{dest}/{filename}")
            tk.messagebox.showinfo("Success", f"Image saved as {filename}")

        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCaptureApp(root)
    root.mainloop()