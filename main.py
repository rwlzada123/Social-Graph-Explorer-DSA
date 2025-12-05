import sys
import os

from PyQt5.QtWidgets import QApplication
from gui.MainWindow import MainWindow

# Make sure Python can find project folders
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
