import sys
import PyQt5
from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QAction,
    QMessageBox,
    QCheckBox,
    QProgressBar,
    QComboBox,
    QStyleFactory,
    QLabel,
    QLineEdit,
    QHBoxLayout,
)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Stock Manager")

        extractAction = QAction("Get to the ", self)
        extractAction.setShortcut("Ctrl+A")
        extractAction.setStatusTip("Leave The App")
        extractAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(extractAction)

        self.home()

    def home(self):
        btn = QPushButton("Quit", self)
        btn.clicked.connect(self.close_application)

        checkBox = QCheckBox("Enlarge Window", self)
        checkBox.move(0, 25)
        checkBox.stateChanged.connect(self.enlarge_window)

        btn_stock = QPushButton("Add Stock", self)
        # btn_stock.clicked.connect(self.)

        lbl_stock_percent = QLabel("Hello World: ", self)
        # lbl_stock_percent.move(5, 50)

        textbox = QLineEdit(self)
        # textbox.move(85, 50)

        btn_ok = QPushButton("OK", self)
        # btn_ok.setGeometry(190, 51, 30, 30)
        btn_ok.clicked.connect(self.change_val)

        lbl_given_value = QLabel("Nan", self)
        # lbl_given_value.move(225, 50)

        layout_1 = QHBoxLayout()
        layout_1.addWidget(btn_stock)
        layout_1.addWidget(lbl_stock_percent)
        layout_1.addWidget(textbox)
        layout_1.addWidget(btn_ok)
        layout_1.addWidget(lbl_given_value)
        self.setLayout(layout_1)
        self.show()

    def change_val(self):
        # lbl_given_value.settext
        pass

    def enlarge_window(self, state):
        if state == QtCore.Qt.Checked:
            self.setGeometry(50, 50, 1000, 600)
        else:
            self.setGeometry(50, 50, 500, 300)

    def close_application(self):
        choice = QMessageBox.question(
            self, "Extract!", "Get into the chopper?", QMessageBox.Yes | QMessageBox.No
        )
        if choice == QMessageBox.Yes:
            print("Extracting now!")
            sys.exit()
        else:
            pass


def run():
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec())


run()
