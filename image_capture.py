import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
from picamera2 import Picamera2, Preview
import os
from io import BytesIO

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Raspberry Pi Camera App")
        
        # Initialize Picamera2
        self.picam2 = Picamera2()
        self.picam2.start_preview(Preview.QTGL)
        
        # Input fields for label and destination
        self.label_entry = tk.Entry(root, width=30)
        self.label_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(root, text="Enter Label:").grid(row=0, column=0)
        
        self.dest_entry = tk.Entry(root, width=30)
        self.dest_entry.grid(row=1, column=1, padx=10, pady=10)
        tk.Label(root, text="Save Location:").grid(row=1, column=0)
        
        self.preview_label = tk.Label(root)
        self.preview_label.grid(row=2, column=0, columnspan=2)
        
        # Button to capture the image
        self.capture_button = tk.Button(root, text="Click", command=self.capture_image)
        self.capture_button.grid(row=3, column=0, columnspan=2, pady=10)

    def capture_image(self):
        # Ensure both label and destination are filled
        label = self.label_entry.get()
        dest = self.dest_entry.get()
        
        if not label:
            messagebox.showerror("Error", "Please enter a label.")
            return
        if not dest:
            messagebox.showerror("Error", "Please enter a save location.")
            return
        
        # Capture image
        image = self.picam2.capture_array()
        pil_image = Image.fromarray(image)
        
        # Add label to image
        draw = ImageDraw.Draw(pil_image)
        font = ImageFont.load_default()
        draw.text((10, 10), label, font=font, fill="white")
        
        # Save image
        if not os.path.exists(dest):
            os.makedirs(dest)
        file_path = os.path.join(dest, f"{label}.jpg")
        pil_image.save(file_path)
        
        # Update preview
        img = ImageTk.PhotoImage(pil_image)
        self.preview_label.config(image=img)
        self.preview_label.image = img

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
