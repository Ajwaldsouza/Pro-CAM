import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont
# import picamera  # Commented out for Mac testing
import os
from io import BytesIO
from PIL import ImageTk

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Raspberry Pi Camera App")
        
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
        
        # Mocking the camera capture for testing on Mac
        # with picamera.PiCamera() as camera:
        #     stream = BytesIO()
        #     camera.capture(stream, format='jpeg')
        #     stream.seek(0)
        #     image = Image.open(stream)
        
        # Mock image for testing
        image = Image.new('RGB', (640, 480), color = (73, 109, 137))
        
        # Add label to image
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((10, 10), label, font=font, fill=(255, 255, 255))
        
        # Save image
        image.save(os.path.join(dest, f"{label}.jpg"))
        
        # Update preview
        self.preview_image = ImageTk.PhotoImage(image)
        self.preview_label.config(image=self.preview_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()