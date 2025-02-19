import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
from picamera2 import Picamera2
import os

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Raspberry Pi Camera App")

        # Initialize Picamera2 with preview and still configurations
        self.picam2 = Picamera2()
        self.preview_config = self.picam2.create_preview_configuration(main={"size": (640, 480)})
        self.still_config = self.picam2.create_still_configuration(main={"size": (2592, 1944)})  # Adjust for your camera
        self.picam2.configure(self.preview_config)
        self.picam2.start()

        # GUI elements
        # Label text entry (used for both image label and file name)
        tk.Label(root, text="Enter label text (will be used as file name):").grid(row=0, column=0, padx=10, pady=5)
        self.label_entry = tk.Entry(root, width=30)
        self.label_entry.grid(row=0, column=1, padx=10, pady=5)

        # Save directory with browse button
        tk.Label(root, text="Save directory:").grid(row=1, column=0, padx=10, pady=5)
        self.save_dir = os.getcwd()
        self.dest_label = tk.Label(root, text=self.save_dir, width=30, anchor="w")
        self.dest_label.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.browse_dest).grid(row=1, column=2, padx=10, pady=5)

        # Preview label
        self.preview_label = tk.Label(root, width=640, height=480, bg="black")
        self.preview_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Capture button
        self.capture_button = tk.Button(root, text="Capture", command=self.capture_image)
        self.capture_button.grid(row=3, column=0, columnspan=3, pady=10)

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start preview update
        self.update_preview()

    def browse_dest(self):
        """Open a dialog to select the save directory."""
        dir_path = filedialog.askdirectory(initialdir=self.save_dir)
        if dir_path:
            self.save_dir = dir_path
            self.dest_label.config(text=self.save_dir)

    def update_preview(self):
        """Update the preview label with the latest camera frame."""
        frame = self.picam2.capture_array()
        if frame is not None:
            pil_frame = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(pil_frame)
            self.preview_label.config(image=photo)
            self.preview_label.image = photo  # Keep reference to prevent garbage collection
        self.root.after(100, self.update_preview)  # Update every 100ms (10 FPS)

    def capture_image(self):
        """Capture an image, add label text, and save it as JPEG with the label text as the file name."""
        label_text = self.label_entry.get().strip()

        # Validate input
        if not label_text:
            messagebox.showerror("Error", "Please enter a label text.")
            return

        # Capture high-resolution image
        try:
            image = self.picam2.switch_mode_and_capture_array(self.still_config)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture image: {e}")
            return

        # Convert to PIL Image (Picamera2 returns RGB by default)
        pil_image = Image.fromarray(image)

        # Add label text at bottom-right with proportional font size
        draw = ImageDraw.Draw(pil_image)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", pil_image.height // 50)
        except IOError:
            font = ImageFont.load_default()
            messagebox.showwarning("Warning", "Font not found, using default font.")

        # Calculate text position (bottom-right corner)
        bbox = draw.textbbox((0, 0), label_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = pil_image.width - text_width - 10
        y = pil_image.height - text_height - 10
        draw.text((x, y), label_text, font=font, fill="white")

        # Save the image as JPEG with the label text as the file name
        file_name = f"{label_text}.jpg"
        file_path = os.path.join(self.save_dir, file_name)
        try:
            pil_image.save(file_path, format="JPEG")
            messagebox.showinfo("Success", f"Image saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")

    def on_closing(self):
        """Clean up resources when the window is closed."""
        self.picam2.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()