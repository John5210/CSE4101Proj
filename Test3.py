import sys
import math
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window attributes
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        )  # Always on top, frameless

        # Make the window transparent (0.7 for 70% opacity)
        self.setWindowOpacity(0.7)

        # Increase the window size
        self.resize(300, 300)

        # Initialize the speed variable
        self.speed = 0

        # Initialize the braking rate
        self.braking_rate = 1  # Adjust this value to control the braking rate

        # Create UI elements
        self.label_time = QLabel(self)
        self.label_speed = QLabel(self)
        self.label_speed_value = QLabel(self)

        # Resize labels
        self.label_time.resize(200, 30)
        self.label_speed.resize(200, 30)
        self.label_speed_value.resize(200, 30)

        # Configure UI elements
        self.label_time.move(10, 10)
        self.label_speed.move(10, 40)
        self.label_speed_value.move(60, 40)

        # Set the text color of the labels to white
        self.label_time.setStyleSheet("color: red;")
        self.label_speed.setStyleSheet("color: red;")
        self.label_speed_value.setStyleSheet("color: red;")  # Set the text color of the speed value label to red

        # Start the timer to update the overlay
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_overlay)
        self.timer.start(1000)  # Update every second

        # Connect key press and release events to handler functions
        self.keyPressEvent = self.handle_key_press
        self.keyReleaseEvent = self.handle_key_release

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the speedometer background
        painter.setBrush(Qt.darkGray)
        painter.drawEllipse(50, 100, 200, 200)

        # Draw speedometer markings only outside the 4 o'clock to 8 o'clock range
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        for i in range(0, 9):
            angle = -210 + i * 30  # 7 o'clock to 5 o'clock
            if 120 <= angle <= 300:  # Skip the 4 o'clock to 8 o'clock range
                continue
            x1 = int(150 + 80 * math.cos(math.radians(angle)))
            y1 = int(200 + 80 * math.sin(math.radians(angle)))
            x2 = int(150 + 95 * math.cos(math.radians(angle)))
            y2 = int(200 + 95 * math.sin(math.radians(angle)))
            painter.drawLine(x1, y1, x2, y2)

        # Draw the speedometer pointer based on the current speed
        angle = -210 + (self.speed / 10) * 30  # 7 o'clock to 5 o'clock
        x = int(150 + 70 * math.cos(math.radians(angle)))
        y = int(200 + 70 * math.sin(math.radians(angle)))
        painter.setPen(QPen(QColor(255, 0, 0), 4))
        painter.drawLine(150, 200, x, y)

    def update_overlay(self):
        # Decrease the speed gradually
        if self.speed > 0:
            self.speed -= self.braking_rate
            self.update()  # Trigger a repaint to update the speedometer

        # Update the labels with time and speed data from CARLA (replace with actual data)
        current_time = QDateTime.currentDateTime().toString("hh:mm:ss")
        self.label_time.setText(f"Time: {current_time}")

        # Update the "Speed" label and its value
        speed_label = "Speed:"
        speed_value = f"{self.speed:.1f} mph"
        self.label_speed.setText(speed_label)
        self.label_speed_value.setText(speed_value)

    def handle_key_press(self, event):
        if event.key() == Qt.Key_W:
            # Increase the speed when 'w' key is pressed
            self.speed += 1
            self.update()  # Trigger a repaint to update the speedometer
        elif event.key() == Qt.Key_Space:
            # Increase the braking rate when spacebar is pressed
            self.braking_rate = 5  # Adjust this value for higher braking rate

    def handle_key_release(self, event):
        if event.key() == Qt.Key_Space:
            # Reset the braking rate when spacebar is released
            self.braking_rate = 2  # Adjust this value for normal braking rate
         
if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = OverlayWindow()
    overlay.show()
    sys.exit(app.exec_())
