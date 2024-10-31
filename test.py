import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
import picamera2
import time

class ImageCaptureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Capture App')
        self.setGeometry(300, 300, 400, 300)

        # Camera setup
        self.camera = picamera2.Picamera2()
        self.config = self.camera.configure(picamera2.PreviewConfig(), picamera2.CaptureConfig())
        self.camera.start_preview(self.config['preview'])

        # GUI elements
        self.label = QLabel(self)
        self.label.resize(320, 240)
        self.label.move(20, 20)

        self.label_input = QLineEdit(self)
        self.label_input.move(20, 260)
        self.label_input.resize(200, 20)

        self.save_button = QPushButton('Click', self)
        self.save_button.move(230, 260)
        self.save_button.clicked.connect(self.capture_and_save)

        self.show()

    def capture_and_save(self):
        label_text = self.label_input.text()
        if not label_text:
            print("Please enter a label")
            return

        # Capture image
        request = self.camera.capture_request()
        self.camera.capture(request)
        image = self.camera.capture_buffer(request)['main']
        qimage = QImage(image, 320, 240, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.label.setPixmap(pixmap)

        # Add label to image (implement your desired labeling method)
        # For example, using OpenCV or PIL:
        # import cv2
        # ... (convert QImage to OpenCV image)
        # cv2.putText(image, label_text, (10, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Save image
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'JPEG (*.jpg)')
        if file_path:
            # Save the image using OpenCV or PIL
            cv2.imwrite(file_path, image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageCaptureApp()
    sys.exit(app.exec_())
