import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
from picamera2 import Picamera2
import os
import cv2
import csv
import numpy as np

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
        tk.Label(root, text="Enter label text (will be used as file name):").grid(row=0, column=0, padx=10, pady=5)
        self.label_entry = tk.Entry(root, width=30)
        self.label_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Save directory:").grid(row=1, column=0, padx=10, pady=5)
        self.save_dir = os.getcwd()
        self.dest_label = tk.Label(root, text=self.save_dir, width=30, anchor="w")
        self.dest_label.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.browse_dest).grid(row=1, column=2, padx=10, pady=5)

        self.preview_label = tk.Label(root, width=640, height=480, bg="black")
        self.preview_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.capture_button = tk.Button(root, text="Capture", command=self.capture_image)
        self.capture_button.grid(row=3, column=0, columnspan=3, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

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
            self.preview_label.image = photo
        self.root.after(100, self.update_preview)

    def capture_image(self):
        """Capture an image, process it to measure canopy area, detect edges, and save results."""
        label_text = self.label_entry.get().strip()
        if not label_text:
            messagebox.showerror("Error", "Please enter a label text.")
            return

        # Capture high-resolution image
        try:
            image_rgb = self.picam2.switch_mode_and_capture_array(self.still_config)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture image: {e}")
            return

        # Save raw image
        raw_file_path = os.path.join(self.save_dir, f"raw_{label_text}.jpg")
        try:
            pil_image = Image.fromarray(image_rgb)
            pil_image.save(raw_file_path, format="JPEG")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save raw image: {e}")
            return

        # Convert to BGR for processing
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        # Preprocessing: Apply Gaussian blur to reduce noise
        blurred_bgr = cv2.GaussianBlur(image_bgr, (5, 5), 0)

        # Segmentation: Convert to HSV and threshold for green plants
        hsv = cv2.cvtColor(blurred_bgr, cv2.COLOR_BGR2HSV)
        lower_green = (30, 40, 40)  # Adjust these values based on your plants/background
        upper_green = (90, 255, 255)
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Refine mask with morphological closing
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Area Calculation: Count plant pixels in the mask
        canopy_area = cv2.countNonZero(mask)

        # Edge Detection: Find and draw contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_img = image_bgr.copy()
        cv2.drawContours(contour_img, contours, -1, (0, 0, 255), 3)  # Green contours

        # Save edge-detected image
        edges_file_path = os.path.join(self.save_dir, f"edges_{label_text}.jpg")
        try:
            cv2.imwrite(edges_file_path, contour_img)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save edge-detected image: {e}")
            return

        # Save canopy area to CSV
        csv_file_path = os.path.join(self.save_dir, "canopy_areas.csv")
        try:
            file_exists = os.path.isfile(csv_file_path)
            with open(csv_file_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(["sample_name", "canopy_area"])
                writer.writerow([label_text, canopy_area])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to write to CSV: {e}")
            return

        # Add label text and save labeled image (original functionality)
        pil_image = Image.fromarray(image_rgb)
        draw = ImageDraw.Draw(pil_image)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", pil_image.height // 25)
        except IOError:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), label_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = pil_image.width - text_width - 10
        y = pil_image.height - text_height - 10
        draw.text((x, y), label_text, font=font, fill="white")
        labeled_file_path = os.path.join(self.save_dir, f"{label_text}.jpg")
        try:
            pil_image.save(labeled_file_path, format="JPEG")
            messagebox.showinfo("Success", f"Image saved to {labeled_file_path}\nCanopy area: {canopy_area} pixels")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save labeled image: {e}")

    def on_closing(self):
        """Clean up resources when the window is closed."""
        self.picam2.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()