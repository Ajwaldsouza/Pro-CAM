import tkinter as tk
from tkinter import filedialog, messagebox
from picamera2 import Picamera2
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
import time

class CameraApp(tk.Tk):
    """
    A GUI application for capturing and annotating images using a Raspberry Pi Camera.
    """
    def __init__(self):
        """Initialize the application, set up the camera, and create the GUI."""
        super().__init__()
        self.title("Pi Camera Capture")
        self.geometry("1280x720")  # Window size to accommodate two 640x480 previews

        # Initialize the Pi Camera
        self.camera = Picamera2()
        self.preview_config = self.camera.create_preview_configuration(main={"size": (640, 480)})
        self.still_config = self.camera.create_still_configuration(main={"size": (2592, 1944)})
        self.camera.configure(self.preview_config)
        self.camera.start()

        # Set up GUI components
        # Live preview label
        self.preview_label = tk.Label(self, width=640, height=480, bg="black")
        self.preview_label.grid(row=0, column=0, padx=10, pady=10)

        # Captured image label (initially empty)
        self.captured_label = tk.Label(self, width=640, height=480, bg="black")
        self.captured_label.grid(row=0, column=1, padx=10, pady=10)

        # Control frame for input fields and buttons
        control_frame = tk.Frame(self)
        control_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Image name input
        tk.Label(control_frame, text="Enter image name with extension (e.g., image.jpg):").pack(side=tk.LEFT, padx=5)
        self.name_entry = tk.Entry(control_frame, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=5)

        # Destination folder selection
        self.dest_var = tk.StringVar(value=os.getcwd())  # Default to current directory
        tk.Label(control_frame, text="Destination:").pack(side=tk.LEFT, padx=5)
        tk.Label(control_frame, textvariable=self.dest_var, width=30).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Select Destination", command=self.select_destination).pack(side=tk.LEFT, padx=5)

        # Capture button
        tk.Button(control_frame, text="Capture", command=self.capture_image).pack(side=tk.LEFT, padx=5)

        # Start the live preview update loop
        self.update_preview()

        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_preview(self):
        """Update the live preview by capturing and displaying camera frames."""
        frame = self.camera.capture_array()
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image)
        self.preview_label.config(image=photo)
        self.preview_label.image = photo  # Keep reference to avoid garbage collection
        self.preview_label.after(33, self.update_preview)  # Schedule next update (~30 fps)

    def select_destination(self):
        """Open a file dialog to select the destination folder."""
        dest = filedialog.askdirectory(initialdir=self.dest_var.get(), title="Select Destination Folder")
        if dest:
            self.dest_var.set(dest)

    def capture_image(self):
        """Capture an image, annotate it with the provided name, save it, and display it."""
        name = self.name_entry.get().strip()
        dest = self.dest_var.get().strip()

        # Validate inputs
        if not name:
            messagebox.showerror("Error", "Please enter an image name with extension")
            return
        if not dest or not os.path.isdir(dest):
            messagebox.showerror("Error", "Please select a valid destination folder")
            return

        # Capture high-resolution image
        self.camera.switch_mode(self.still_config)
        time.sleep(0.1)  # Brief pause to allow camera adjustment
        frame = self.camera.capture_array()
        self.camera.switch_mode(self.preview_config)  # Switch back to preview mode

        # Process the captured image
        image = Image.fromarray(frame)

        # Load font for text overlay
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        except IOError:
            font = ImageFont.load_default()
            print("Warning: Default font loaded. For better quality, install DejaVuSans.ttf")

        # Add text overlay in the lower right corner
        draw = ImageDraw.Draw(image)
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = image.width - text_width - 10  # 10px margin from right
        y = image.height - text_height - 10  # 10px margin from bottom

        # Draw black outline for readability
        for offset_x, offset_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            draw.text((x + offset_x, y + offset_y), name, font=font, fill="black")
        # Draw white text
        draw.text((x, y), name, font=font, fill="white")

        # Save the annotated image
        save_path = os.path.join(dest, name)
        try:
            image.save(save_path, quality=95)  # High-quality JPEG
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {str(e)}")
            return

        # Display the captured image in the GUI
        display_image = image.resize((640, 480), Image.Resampling.LANCZOS)  # Maintain aspect ratio
        photo = ImageTk.PhotoImage(display_image)
        self.captured_label.config(image=photo)
        self.captured_label.image = photo  # Keep reference

        # Notify user of success
        messagebox.showinfo("Success", f"Image saved to {save_path}")

    def on_closing(self):
        """Clean up resources and close the application."""
        self.camera.stop()
        self.destroy()

if __name__ == "__main__":
    try:
        app = CameraApp()
        app.mainloop()
    except Exception as e:
        print(f"Failed to start application: {str(e)}")
        if "camera" in locals():
            camera.stop()  # Attempt to stop camera if initialized