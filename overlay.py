# overlay.py
import ctypes
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QPoint

class OverlayDot(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config

        self.dot_size = self.config.get("dot_size", 4)
        self.dot_color = QColor(*self.config.get("dot_color", [255, 0, 0]))
        self.crosshair_type = self.config.get("crosshair_type", "Dot")
        self.opacity = self.config.get("opacity", 1.0)

        self.outline = True
        self.gap = 4
        self.length = 12
        self.line_thickness = 2
        self.dot_thickness = 6
        self.custom_pixmap = None

        self.update_size()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowTransparentForInput)
        self.setWindowOpacity(self.opacity)
        self.center_window()
        ctypes.windll.user32.SetWindowPos(int(self.winId()), -1, self.x(), self.y(), self.width(), self.height(), 0x0001)

    def update_size(self):
        if self.crosshair_type == 'Custom' and self.custom_pixmap:
            self.setFixedSize(self.custom_pixmap.size())
        else:
            self.setFixedSize(self.dot_size * 10, self.dot_size * 10)
        self.center_window()

    def center_window(self):
        screen = self.screen().geometry()
        x = int((screen.width() - self.width()) / 2)
        y = int((screen.height() - self.height()) / 2)
        self.move(x, y)

    def set_dot_color(self, color):
        self.dot_color = color
        self.config.set("dot_color", [color.red(), color.green(), color.blue()])
        self.update()

    def set_crosshair_type(self, crosshair_type):
        self.crosshair_type = crosshair_type
        self.config.set("crosshair_type", crosshair_type)
        self.update_size()
        self.update()

    def set_dot_size(self, size):
        self.dot_size = size
        self.config.set("dot_size", size)
        self.update_size()
        self.update()

    def set_custom_crosshair(self, pixmap):
        self.custom_pixmap = pixmap
        self.crosshair_type = 'Custom'
        self.update_size()
        self.update()

    def set_opacity(self, opacity):
        self.opacity = opacity
        self.config.set("opacity", opacity)
        self.setWindowOpacity(opacity)
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
            painter.drawLine(center.x() - 10*self.dot_size, center.y(),
                             center.x() + 10*self.dot_size, center.y())
            painter.drawLine(center.x(), center.y() - 10*self.dot_size,
                             center.x(), center.y() + 10*self.dot_size)
        elif self.crosshair_type == 'X-Crosshair':
            pen = QPen(self.dot_color, self.dot_size)
            painter.setPen(pen)
            painter.drawLine(center.x() - 10*self.dot_size, center.y() - 10*self.dot_size,
                             center.x() + 10*self.dot_size, center.y() + 10*self.dot_size)
            painter.drawLine(center.x() - 10*self.dot_size, center.y() + 10*self.dot_size,
                             center.x() + 10*self.dot_size, center.y() - 10*self.dot_size)
        elif self.crosshair_type == 'Custom' and self.custom_pixmap:
            painter.drawPixmap(0, 0, self.custom_pixmap)
