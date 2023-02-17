import sys
from PyQt5.QtWidgets import QApplication
from webthingy_gui import WebthingyGUI


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = WebthingyGUI()
    gui.show()
    sys.exit(app.exec_())
