import tkinter as tk
from tkinter import filedialog
import picamera
import time
import datetime

class ImageCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Capture and Labeling")

        # GUI Components
        self.label_frame = tk.Frame(root)
        self.label_frame.pack()
        self.label_label = tk.Label(self.label_frame, text="Enter Label:")
        self.label_label.pack(side=tk.LEFT)
        self.label_entry = tk.Entry(self.label_frame)
        self.label_entry.pack(side=tk.LEFT)

        self.dest_frame = tk.Frame(root)
        self.dest_frame.pack()
        self.dest_label = tk.Label(self.dest_frame, text="Select Destination:")
        self.dest_label.pack(side=tk.LEFT)
        self.dest_button = tk.Button(self.dest_frame, text="Browse", command=self.select_dest)
        self.dest_button.pack(side=tk.LEFT)
        self.dest_entry = tk.Entry(self.dest_frame)
        self.dest_entry.pack(side=tk.LEFT)

        self.capture_button = tk.Button(root, text="Capture", command=self.capture_image)
        self.capture_button.pack()

        self.preview_frame = tk.Frame(root)
        self.preview_frame.pack()
        self.preview_label = tk.Label(self.preview_frame)
        self.preview_label.pack()

        self.camera = picamera.PiCamera()

    def select_dest(self):
        self.dest_entry.delete(0, tk.END)
        self.dest_entry.insert(0, filedialog.askdirectory())

    def capture_image(self):
        label = self.label_entry.get()
        dest = self.dest_entry.get()

        if not label or not dest:
            tk.messagebox.showerror("Error", "Please enter a label and select a destination.")
            return

        try:
            # Capture image
            self.camera.capture('temp.jpg')

            # Load image and add label
            image = Image.open('temp.jpg')
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 24)
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
