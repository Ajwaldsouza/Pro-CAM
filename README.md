# Raspberry Pi Camera Canopy Area App

This is a Python application designed for the Raspberry Pi that utilizes the PiCamera2 module to capture high-resolution images and perform basic image processing to calculate the projected canopy area of the plant. The application provides a graphical user interface (GUI) to preview the camera feed, capture images, and analyze the captured image to calculate the canopy area (i.e., the number of green pixels corresponding to plants). The processed images and data are saved to a user-specified directory.

## Features

- **Live Camera Preview:** Displays a real-time camera feed in the GUI.
- **Image Capture:** Captures a high-resolution image from the Raspberry Pi camera.
- **Labeling:** Adds a user-provided label to the captured image.
- **Image Processing:** 
  - Applies Gaussian blur to reduce noise.
  - Converts the image to the HSV color space and thresholds it to detect green regions.
  - Uses morphological operations to refine the segmentation.
  - Detects edges by finding contours.
- **Data Logging:** Saves the canopy area measurement to a CSV file along with the label.
- **File Management:** Allows the user to select the destination directory for saving images and data.

## Requirements

- **Hardware:**
  - Raspberry Pi with an attached camera module compatible with PiCamera2.
- **Software:**
  - Python 3.x
  - Tkinter (usually included with Python)
  - [Picamera2](https://github.com/raspberrypi/picamera2) (for interfacing with the Raspberry Pi camera)
  - [Pillow](https://python-pillow.org/) (for image processing)
  - [OpenCV](https://opencv.org/) (for advanced image processing)
  - [NumPy](https://numpy.org/) (for numerical operations)

## Installation

1. **Install Python Packages:**

   You can install the required packages using pip:
   ```bash
   pip install pillow opencv-python-headless numpy
   ```


2. **Install and Configure Picamera2:**
Follow the instructions on the Picamera2 GitHub repository to install and configure the Picamera2 library on your Raspberry Pi.


## Usage

Clone the Repository:
```bash
git clone https://github.com/yourusername/raspberry-pi-camera-app.git
cd raspberry-pi-camera-app
```
Run the Application: 
Execute the Python script:
```bash
python image_capture.py
```

3. **Using the Application:**
  - Enter a label in the provided text field (this will be used as the image file name).
  - Optionally, click the "Browse" button to select a different directory where the images and CSV file will be saved.
  - The live camera preview will appear in the window.
  - Click the "Capture" button to take an image. The program will process the image, save the labeled image and edge-detected image, and log the canopy area to a CSV file.
  - A success message will be displayed once the process is complete.

## Notes

The default image dimensions for capture and preview can be adjusted in the script.
The HSV threshold values for detecting green areas might need fine-tuning based on the lighting and the specific plant characteristics.
Ensure that the Raspberry Pi camera is properly connected and configured before running the application.
License

This project is licensed under the MIT License. See the LICENSE file for details.

