import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QColorDialog, QPushButton, QVBoxLayout, QComboBox, QSlider,
                             QLabel, QFrame, QHBoxLayout)
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPixmap
from PyQt5.QtCore import Qt, QPoint
import ctypes

class OverlayDot(QWidget):
    def __init__(self):
        super().__init__()

        self.dot_size = 2
        self.dot_color = QColor(255, 0, 0)
        self.crosshair_type = 'Dot'
        self.custom_pixmap = None
        self.update_size()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowTransparentForInput)
        self.center_window()
        ctypes.windll.user32.SetWindowPos(int(self.winId()), -1, self.x(), self.y(), self.width(), self.height(), 0x0001)

    def update_size(self):
        if self.crosshair_type == 'Custom':
            if self.custom_pixmap:
                self.setFixedSize(self.custom_pixmap.size())
            else:
                self.setFixedSize(100, 100)
        else:
            self.setFixedSize(self.dot_size * 10, self.dot_size * 10)
        self.center_window()

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        x = int((screen.width() - self.width()) / 2)
        y = int((screen.height() - self.height()) / 2)
        self.move(x, y)

    def set_dot_color(self, color):
        self.dot_color = color
        self.update()

    def set_crosshair_type(self, crosshair_type):
        self.crosshair_type = crosshair_type
        self.update_size()
        self.update()

    def set_dot_size(self, size):
        self.dot_size = size
        self.update_size()
        self.update()

    def set_custom_crosshair(self, pixmap):
        self.custom_pixmap = pixmap
        self.crosshair_type = 'Custom'
        self.update_size()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center = QPoint(self.width() // 2, self.height() // 2)

        if self.crosshair_type == 'Dot':
            painter.setBrush(QBrush(self.dot_color, Qt.SolidPattern))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center, self.dot_size, self.dot_size)
        elif self.crosshair_type == 'Crosshair':
            pen = QPen(self.dot_color, self.dot_size)
            painter.setPen(pen)
            painter.drawLine(center.x() - 10 * self.dot_size, center.y(), center.x() + 10 * self.dot_size, center.y())
            painter.drawLine(center.x(), center.y() - 10 * self.dot_size, center.x(), center.y() + 10 * self.dot_size)
        elif self.crosshair_type == 'X-Crosshair':
            pen = QPen(self.dot_color, self.dot_size)
            painter.setPen(pen)
            painter.drawLine(center.x() - 10 * self.dot_size, center.y() - 10 * self.dot_size, center.x() + 10 * self.dot_size, center.y() + 10 * self.dot_size)
            painter.drawLine(center.x() - 10 * self.dot_size, center.y() + 10 * self.dot_size, center.x() + 10 * self.dot_size, center.y() - 10 * self.dot_size)


class CustomCrosshairEditor(QWidget):
    def __init__(self, overlay_dot):
        super().__init__()
        self.overlay_dot = overlay_dot
        self.drawing = False
        self.last_point = QPoint()
        self.pen_color = QColor(0, 0, 0)
        self.pen_size = 4
        self.bg_color = QColor(255, 255, 255)
        self.initUI()


    def open_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.pen_color = color

    def open_bg_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.bg_color = color
            self.canvas.fill(self.bg_color)
            self.update()

    def change_pen_size(self, size):
        self.pen_size = size

    def add_circle(self):
        painter = QPainter(self.canvas)
        painter.setPen(QPen(self.pen_color, self.pen_size))
        center = QPoint(self.canvas.width() // 2, self.canvas.height() // 2)
        painter.drawEllipse(center, 50, 50)
        self.update()

    def add_square(self):
        painter = QPainter(self.canvas)
        painter.setPen(QPen(self.pen_color, self.pen_size))
        rect = self.canvas.rect().adjusted(75, 75, -75, -75)
        painter.drawRect(rect)
        self.update()

    def add_cross(self):
        painter = QPainter(self.canvas)
        painter.setPen(QPen(self.pen_color, self.pen_size))
        center = QPoint(self.canvas.width() // 2, self.canvas.height() // 2)
        painter.drawLine(center.x() - 50, center.y(), center.x() + 50, center.y())
        painter.drawLine(center.x(), center.y() - 50, center.y() + 50)
        self.update()

    def activate_eraser(self):
        self.pen_color = self.bg_color

    def save_crosshair(self):
        self.overlay_dot.set_custom_crosshair(self.canvas)
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.canvas)
            painter.setPen(QPen(self.pen_color, self.pen_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.canvas)

class ColorEditor(QWidget):
    def __init__(self, overlay_dot):
        super().__init__()
        self.overlay_dot = overlay_dot
        self.custom_editor = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("dCrosshair")

        self.color_button = QPushButton("Change Color", self)
        self.color_button.clicked.connect(self.open_color_dialog)

        self.crosshair_selector = QComboBox(self)
        self.crosshair_selector.addItems(["Dot", "Crosshair", "X-Crosshair"])
        self.crosshair_selector.currentTextChanged.connect(self.overlay_dot.set_crosshair_type)

        self.size_slider = QSlider(Qt.Horizontal, self)
        self.size_slider.setMinimum(1)
        self.size_slider.setMaximum(10)
        self.size_slider.setValue(4)
        self.size_slider.valueChanged.connect(self.overlay_dot.set_dot_size)

        self.size_label = QLabel("Size", self)



        layout = QVBoxLayout()
        layout.addWidget(self.color_button)
        layout.addWidget(self.crosshair_selector)
        layout.addWidget(self.size_label)
        layout.addWidget(self.size_slider)
        self.setLayout(layout)

    def open_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.overlay_dot.set_dot_color(color)

    def open_custom_editor(self):
        if self.custom_editor is None or not self.custom_editor.isVisible():
            self.custom_editor = CustomCrosshairEditor(self.overlay_dot)
            self.custom_editor.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    overlay = OverlayDot()
    overlay.show()
    color_editor = ColorEditor(overlay)
    color_editor.show()

    sys.exit(app.exec_())
