import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont
import picamera2 as picamera
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

        # Take picture using picamera
        with picamera.PiCamera() as camera:
            stream = BytesIO()
            camera.capture(stream, format='jpeg')
            stream.seek(0)
            image = Image.open(stream)

            # Add label to image
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()
            text_position = (image.width - 100, image.height - 30)  # Bottom-right corner
            draw.text(text_position, label, font=font, fill="white")
            
            # Save the image
            filename = f"{label}.jpg"
            save_path = os.path.join(dest, filename)
            image.save(save_path)
            
            # Show preview in GUI
            self.show_preview(image)

    def show_preview(self, image):
        # Convert image to Tkinter-compatible format
        image.thumbnail((400, 300))
        img_tk = ImageTk.PhotoImage(image)
        self.preview_label.config(image=img_tk)
        self.preview_label.image = img_tk

# Set up GUI
root = tk.Tk()
app = CameraApp(root)
root.mainloop()
