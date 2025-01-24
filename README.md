# Raspberry Pi Camera App

This is a simple Raspberry Pi Camera application built using Python and Tkinter. The application captures images using the Raspberry Pi camera, allows the user to add a label to the image, and saves the image to a specified location.

## Features

- Capture images using the Raspberry Pi camera.
- Add a custom label to the captured image.
- Save the labeled image to a specified directory.
- Simple and intuitive GUI built with Tkinter.

## Requirements

- Python 3.x
- Tkinter
- Pillow (PIL Fork)
- Picamera2

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Ajwaldsouza/image_capture.git
    ```

2. Install the required Python packages:
    ```sh
  
    sudo apt install python3-tk 
    sudo apt install python3-pillow
    sudo apt install python3-picamera2
    sudo apt-get install python3-pil.imagetk # add all the packages properly here
    ```

## Usage

1. Run the application:
    ```sh
    python3 image_capture.py
    ```

2. Enter a label for the image in the "Enter Label" field.

3. Enter the directory where you want to save the image in the "Save Location" field.

4. Click the "Click" button to capture the image. The image will be saved with the specified label in the specified directory.

## Code Overview

- The main application logic is implemented in the `CameraApp` class in [image_capture.py](image_capture.py).
- The `capture_image` method captures the image, adds the label, and saves the image.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI.
- [Pillow](https://python-pillow.org/) for image processing.
- [Picamera2](https://github.com/raspberrypi/picamera2) for interfacing with the Raspberry Pi camera.

