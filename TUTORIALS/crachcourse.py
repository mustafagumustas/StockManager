import sys
import PyQt5
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("qtcrashcourse.ui", self)
        # button
        self.button.clicked.connect(self.buttonclicked)

        # checkbox
        self.checkbox.stateChanged.connect(self.checked)

        # Combo Box
        self.comboBox.setVisible(False)
        listocc = ["engineer", "doctor", "manager"]
        for job in listocc:
            self.comboBox.addItem(job)

        self.comboBox.currentIndexChanged.connect(self.combochanged)

        # spinbox
        self.spinBox.setMinimum(18)
        self.spinBox.setMaximum(30)
        self.spinBox.valueChanged.connect(self.spinchange)

    def buttonclicked(self):
        outputstr = self.fname.toPlainText() + " " + self.lname.toPlainText()
        self.fname.setReadOnly(True)
        self.lname.setReadOnly(True)
        self.fname.setDisabled(True)
        self.lname.setDisabled(True)
        if self.checkbox.isChecked():
            outputstr = outputstr + "is employed"
        else:
            outputstr = outputstr + "is not employed"
        print(outputstr)

    def checked(self):
        if self.checkbox.isChecked():
            self.comboBox.setVisible(True)
        else:
            self.comboBox.setVisible(False)

    def combochanged(self):
        self.joblabel.setText(self.comboBox.currentText() + " is selected")

    def spinchange(self):
        print("current value " + str(self.spinBox.value()))


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(650)
widget.setFixedWidth(1120)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
