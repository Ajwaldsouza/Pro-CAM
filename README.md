# Raspberry Pi Sampling Camera App

This program allows users to capture images using a Raspberry Pi camera, add a label to the image, and save it as a JPEG file. The label text is also used as the file name, and the user can select the directory where the image is saved. The app provides a live preview of the camera feed, making it easy to frame and capture high-resolution photos.

This program was developed to sample top-down canopy images of plants.

## **Features**

-   **Live preview**: See the camera feed in real-time before capturing.

-   **High-resolution capture**: Images are saved at 2592x1944 resolution by default.

-   **Custom labeling**: Add user-defined text to the bottom-right corner of each image.

-   **JPEG output**: Save images in a widely compatible format.

-   **User-friendly GUI**: Simple interface for easy operation.


<img width="475" alt="Screenshot 2025-02-28 at 10 22 25 am" src="https://github.com/user-attachments/assets/bcbd9bb6-e56c-4bc3-82ec-68689095f3aa" />

------------------------------------------------------------------------

## Requirements

Before using this program, ensure you have the following:

-   A **Raspberry Pi** with a camera module attached and enabled.

-   **Python 3** installed on your Raspberry Pi.

-   Required Python libraries: tkinter, Pillow, and picamera2.

-   A **display** connected to the Raspberry Pi, or remote access via SSH for GUI support.

------------------------------------------------------------------------

## **Installation**

Follow these steps to set up the program:

1.  **Clone the repository or download the source code** to your Raspberry Pi.

2.  **Install the required Python libraries** using the following commands:

    bash

    ```         
    pip install pillow picamera2
    ```

    **Note**: tkinter is typically included with Python on Raspberry Pi OS. If it’s not installed, run:

    bash

    ```         
    sudo apt-get install python3-tk
    ```

------------------------------------------------------------------------

## Usage

1.  To run and use the program:

    1.  Launch the app by running the Python script:

        bash

        ```         
        python3 image_capture.py
        ```

    2.  In the GUI:

        -   Enter the **label text** in the text entry field (this will be used as both the label on the image and the file name).

        -   Click the **"Browse"** button to select the directory where the image will be saved.

        -   Click the **"Capture"** button to take a photo.

    3.  The image will be saved in the selected directory as a JPEG file, named after the label text (e.g., `label_text.jpg`), with the label displayed in the bottom-right corner.

------------------------------------------------------------------------

## **Customization**

You can tweak the program to suit your needs:

-   **Font**: By default, the app uses "DejaVu Sans Bold" for labels. To change this, edit the `font` variable in the `capture_image` method of the source code.

-   **Image Resolution**: The default resolution is 2592x1944. Adjust this by modifying the `still_config` settings in the `__init__` method.

**Note**: The program overwrites files with the same name in the save directory. To avoid this, modify the code to append a timestamp or counter to the file name (e.g., `label_text_20231010.jpg`).

------------------------------------------------------------------------

## **Troubleshooting**

Here are some common issues and their solutions:

-   **Camera not detected or enabled**: Verify the camera is connected and enabled via `sudo raspi-config.`

-   **Missing dependencies**: Ensure all required libraries are installed using `pip`.

-   **Permission issues when saving files**: Check that the chosen directory has write permissions (e.g., use `chmod` or select a user-writable folder).

-   **Font not found for labeling**: If the specified font is unavailable, the program will fall back to a default font.

------------------------------------------------------------------------

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. Feel free to use, modify, and distribute it as permitted by the license.
