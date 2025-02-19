import tkinter as tk
from tkinter import filedialog, messagebox
from picamera import PiCamera
from PIL import Image, ImageDraw, ImageFont, ImageTk
import io
import os

class CameraApp(tk.Tk):
    """A GUI application for capturing and annotating images with a Raspberry Pi Camera."""
    
    def __init__(self):
        """Initialize the application, set up the camera, and create GUI components."""
        super().__init__()
        self.title("Pi Camera Capture")
        
        # Initialize the Pi Camera
        try:
            self.camera = PiCamera()
            self.camera.resolution = (1024, 768)  # Set capture resolution
            self.camera.start_preview()  # Start live preview in a separate window
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize camera: {e}")
            self.destroy()
            return
        
        # GUI components
        # Image Name Entry
        self.name_label = tk.Label(self, text="Image Name:")
        self.name_entry = tk.Entry(self)
        
        # Destination Folder Selection
        self.folder_label = tk.Label(self, text="Destination Folder:")
        self.folder_display = tk.Label(self, text="Not selected")
        self.select_folder_btn = tk.Button(self, text="Select Folder", command=self.select_folder)
        
        # Capture Button
        self.capture_btn = tk.Button(self, text="Capture", command=self.capture_image)
        
        # Display for Captured Image
        self.image_display = tk.Label(self, text="No image captured")
        
        # Layout using grid
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.folder_label.grid(row=1, column=0, padx=5, pady=5)
        self.folder_display.grid(row=1, column=1, padx=5, pady=5)
        self.select_folder_btn.grid(row=1, column=2, padx=5, pady=5)
        self.capture_btn.grid(row=2, column=0, columnspan=3, pady=10)
        self.image_display.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
        
        # Variable to store selected folder
        self.selected_folder = None
        
        # Bind window close event to clean up resources
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def select_folder(self):
        """Open a file dialog for the user to select a destination folder."""
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder = folder
            self.folder_display.config(text=folder)
    
    def capture_image(self):
        """Capture an image, annotate it with the provided name, save it, and display a thumbnail."""
        # Get and validate user inputs
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter an image name.")
            return
        if not self.selected_folder:
            messagebox.showerror("Error", "Please select a destination folder.")
            return
        
        try:
            # Capture image to a memory stream
            stream = io.BytesIO()
            self.camera.capture(stream, format='jpeg')
            stream.seek(0)
            
            # Open the captured image with PIL
            img = Image.open(stream)
            
            # Add text overlay in the lower right corner
            draw = ImageDraw.Draw(img)
            try:
                # Attempt to load a TrueType font (common on Raspberry Pi OS)
                font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30)
            except IOError:
                # Fallback to default font if DejaVuSans is unavailable
                font = ImageFont.load_default()
            
            text = name
            width, height = img.size
            
            # Draw text with white fill and black stroke for readability
            draw.text(
                (width - 10, height - 10),  # Position with 10px padding from bottom-right
                text,
                font=font,
                fill='white',
                stroke_width=2,
                stroke_fill='black',
                anchor='rb'  # Right-bottom anchor
            )
            
            # Construct file path and save the annotated image
            file_path = os.path.join(self.selected_folder, f"{name}.jpg")
            img.save(file_path)
            
            # Create a thumbnail for GUI display
            display_img = img.copy()
            display_img.thumbnail((320, 240), Image.ANTIALIAS)  # Resize preserving aspect ratio
            self.photo = ImageTk.PhotoImage(display_img)  # Convert to Tkinter-compatible image
            self.image_display.config(image=self.photo)  # Update display label
            
            # Clear entry field for next capture
            self.name_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture or process image: {e}")
    
    def on_closing(self):
        """Clean up resources and close the application when the window is closed."""
        try:
            self.camera.stop_preview()
            self.camera.close()
        except AttributeError:
            pass  # Camera might not be initialized if init failed
        self.destroy()

if __name__ == "__main__":
    """Run the CameraApp application."""
    app = CameraApp()
    app.mainloop()