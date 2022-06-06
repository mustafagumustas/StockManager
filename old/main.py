import sys
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5 import *
from PyQt5.QtWidgets import *


class Login(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("login.ui", self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()
        if len(email) and len(password) != 0:
            print(
                "Successfully logged in with email: ", email, "and password: ", password
            )

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("create_acc.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)

    def createaccfunction(self):
        email = self.email.text()
        if self.password.text() == self.confirmpass.text():
            password = self.password.text()
            print(
                "Successfully created acc with email: ", email, "and password", password
            )
            login = Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() + 1)


app = QApplication(sys.argv)


mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(400)
widget.setFixedHeight(620)
widget.show()
app.exec_()
