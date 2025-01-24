import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
from picamera2 import Picamera2, Preview
import os
from io import BytesIO
import time

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Raspberry Pi Camera App")
        
        # Initialize Picamera2
        self.picam2 = Picamera2()
        self.picam2.start_preview(Preview.QTGL)
        self.picam2.start()
        
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
        
        if not label or not dest:
            messagebox.showerror("Error", "Both label and save location must be filled.")
            return
        
        # Capture the image
        image = self.picam2.capture_array()

        # Convert BGR to RGB because PIL expects RGB
    image_rgb = image[:, :, ::-1]  # This reverses the color channel order from BGR to RGB
        
        # Convert to PIL Image
        pil_image = Image.fromarray(image)
        
        # Add label to the image
        draw = ImageDraw.Draw(pil_image)
        # Use a TrueType font with a higher resolution
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Update this path to a valid TTF font on your system
        font_size = 24  # Adjust the font size as needed
        font = ImageFont.truetype(font_path, font_size)
        draw.text((10, 10), label, font=font, fill="white")
        
        # Convert image to RGB mode
        pil_image = pil_image.convert("RGB")
        
        # Save the image
        if not os.path.exists(dest):
            os.makedirs(dest)
        file_path = os.path.join(dest, f"{label}.jpg")
        pil_image.save(file_path)
        
        # Restart the preview for the next capture
        self.picam2.stop_preview()
        self.picam2.start_preview(Preview.QTGL)
        
        # Show success message
        messagebox.showinfo("Success", f"Image saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
