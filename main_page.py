import sys
import PyQt5
from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Stock Manager")
        self.home()

    def home(self):
        btn = QPushButton("Quit", self)
        btn.clicked.connect(self.close_application)
        self.setAlignment(Qt.AlignCenter)
        self.show()

    def close_application(self):
        print("Whoooaa!!!")
        sys.exit()


def run():
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec())


run()
