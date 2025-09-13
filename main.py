import sys
from PyQt5.QtWidgets import QApplication
from overlay import OverlayDot
from editor import ColorEditor
from config import ConfigManager

if __name__ == "__main__":
    app = QApplication(sys.argv)

    config_manager = ConfigManager()
    overlay = OverlayDot(config_manager)
    overlay.show()

    # Hotkeys удалены, просто показываем редактор
    color_editor = ColorEditor(overlay, config_manager)
    color_editor.show()

    sys.exit(app.exec_())
