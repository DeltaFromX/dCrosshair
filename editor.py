from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QSlider, QLabel, QColorDialog, \
    QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class ColorEditor(QWidget):
    def __init__(self, overlay, config):
        super().__init__()
        self.overlay = overlay
        self.config = config
        self.initUI()
        self.load_from_config()

    def initUI(self):
        self.setWindowTitle("dCrosshair Library")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff; font-family: Segoe UI;")
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # --- Профили ---
        profile_layout = QVBoxLayout()
        profile_layout.addWidget(QLabel("Select Crosshair Profile"))
        self.profile_selector = QComboBox()
        self.profile_selector.setStyleSheet("""
            QComboBox { background-color: #2b2b2b; border: 1px solid #555; padding: 5px; }
            QComboBox QAbstractItemView { background-color: #2b2b2b; selection-background-color: #3d3d3d; }
        """)
        self.profile_selector.addItems(self.config.get_profiles())
        self.profile_selector.currentTextChanged.connect(self.select_profile)
        profile_layout.addWidget(self.profile_selector)

        self.new_profile_btn = QPushButton("Save Current as New Profile")
        self.new_profile_btn.setStyleSheet(self.button_style())
        self.new_profile_btn.clicked.connect(self.save_new_profile)
        profile_layout.addWidget(self.new_profile_btn)
        layout.addLayout(profile_layout)

        # --- Настройка прицела ---
        settings_layout = QVBoxLayout()
        settings_layout.addWidget(QLabel("Customize Crosshair"))

        self.color_button = QPushButton("Change Color")
        self.color_button.setStyleSheet(self.button_style())
        self.color_button.clicked.connect(self.open_color_dialog)
        settings_layout.addWidget(self.color_button)

        self.crosshair_selector = QComboBox()
        self.crosshair_selector.addItems(["Dot","Crosshair","X-Crosshair"])
        self.crosshair_selector.currentTextChanged.connect(self.overlay.set_crosshair_type)
        self.crosshair_selector.setStyleSheet("""
            QComboBox { background-color: #2b2b2b; border: 1px solid #555; padding: 5px; }
            QComboBox QAbstractItemView { background-color: #2b2b2b; selection-background-color: #3d3d3d; }
        """)
        settings_layout.addWidget(self.crosshair_selector)

        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Size"))
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setMinimum(1)
        self.size_slider.setMaximum(20)
        self.size_slider.setSingleStep(1)
        self.size_slider.setPageStep(1)
        self.size_slider.valueChanged.connect(self.overlay.set_dot_size)
        self.size_slider.setStyleSheet("""
            QSlider::groove:horizontal { background: #555; height: 8px; border-radius: 4px; }
            QSlider::handle:horizontal { background: #fff; width: 14px; margin: -3px 0; border-radius: 7px; }
        """)
        size_layout.addWidget(self.size_slider)
        settings_layout.addLayout(size_layout)

        layout.addLayout(settings_layout)
        self.setLayout(layout)

    def button_style(self):
        return """
            QPushButton {
                background-color: #2b2b2b;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """

    # --- Загрузка настроек ---
    def load_from_config(self):
        cfg = self.config.get_active()
        self.overlay.set_dot_color(QColor(*cfg.get("dot_color",[255,0,0])))
        self.overlay.set_dot_size(cfg.get("dot_size",4))
        self.overlay.set_crosshair_type(cfg.get("crosshair_type","Dot"))
        self.size_slider.setValue(cfg.get("dot_size",4))
        self.crosshair_selector.setCurrentText(cfg.get("crosshair_type","Dot"))

    # --- События UI ---
    def open_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.overlay.set_dot_color(color)

    def select_profile(self, name):
        self.config.set_active(name)
        self.load_from_config()

    def save_new_profile(self):
        name, ok = QInputDialog.getText(self, "New Profile", "Enter profile name:")
        if ok and name:
            cfg = {
                "dot_size": self.overlay.dot_size,
                "dot_color": [self.overlay.dot_color.red(), self.overlay.dot_color.green(),
                              self.overlay.dot_color.blue()],
                "crosshair_type": self.overlay.crosshair_type,
                "opacity": self.overlay.opacity
            }
            self.config.add_profile(name, **cfg)
            self.profile_selector.addItem(name)
            self.profile_selector.setCurrentText(name)

