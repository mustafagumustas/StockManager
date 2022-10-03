# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Volumes/GoogleDrive/My Drive/Python/StockManager/order.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1011, 746)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setMinimumSize(QtCore.QSize(900, 650))
        self.widget.setStyleSheet("background-color: rgb(70, 70, 70);")
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setStyleSheet("background-color: rgb(128, 128, 128);")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.tableWidget, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.delete_button = QtWidgets.QPushButton(self.widget)
        self.delete_button.setMinimumSize(QtCore.QSize(150, 30))
        self.delete_button.setAutoFillBackground(False)
        self.delete_button.setStyleSheet("border-radius:16px;\n"
"border-color: rgb(199, 98, 50);\n"
"background-color: rgb(255, 255, 255);\n"
"color:rgb(0, 0, 0)")
        icon = QtGui.QIcon.fromTheme("backwardbend.png")
        self.delete_button.setIcon(icon)
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout_6.addWidget(self.delete_button)
        self.cancel_button = QtWidgets.QPushButton(self.widget)
        self.cancel_button.setMinimumSize(QtCore.QSize(150, 30))
        self.cancel_button.setAutoFillBackground(False)
        self.cancel_button.setStyleSheet("border-radius:16px;\n"
"border-color: rgb(199, 98, 50);\n"
"background-color: rgb(255, 255, 255);\n"
"color:rgb(0, 0, 0)")
        icon = QtGui.QIcon.fromTheme("backwardbend.png")
        self.cancel_button.setIcon(icon)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout_6.addWidget(self.cancel_button)
        self.ok_button = QtWidgets.QPushButton(self.widget)
        self.ok_button.setMinimumSize(QtCore.QSize(150, 30))
        self.ok_button.setStyleSheet("border-radius:16px;\n"
"border-color: rgb(199, 98, 50);\n"
"background-color: rgb(21, 115, 215);\n"
"color:rgb(255,255,255)")
        self.ok_button.setObjectName("ok_button")
        self.horizontalLayout_6.addWidget(self.ok_button)
        self.gridLayout.addLayout(self.horizontalLayout_6, 3, 2, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setStyleSheet("color:rgb(190,134,80)")
        self.label.setObjectName("label")
        self.gridLayout_6.addWidget(self.label, 1, 0, 1, 1)
        self.check = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.check.sizePolicy().hasHeightForWidth())
        self.check.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.check.setFont(font)
        self.check.setStyleSheet("color:rgb(190,134,80)")
        self.check.setObjectName("check")
        self.gridLayout_6.addWidget(self.check, 1, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem1, 1, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_6.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_6, 4, 2, 1, 1)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.order_id_label = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.order_id_label.sizePolicy().hasHeightForWidth())
        self.order_id_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.order_id_label.setFont(font)
        self.order_id_label.setStyleSheet("color:rgb(255,255,255)")
        self.order_id_label.setObjectName("order_id_label")
        self.horizontalLayout_19.addWidget(self.order_id_label)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem2)
        self.order_id = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.order_id.sizePolicy().hasHeightForWidth())
        self.order_id.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.order_id.setFont(font)
        self.order_id.setStyleSheet("color:rgb(255,255,255)")
        self.order_id.setObjectName("order_id")
        self.horizontalLayout_19.addWidget(self.order_id)
        self.gridLayout.addLayout(self.horizontalLayout_19, 0, 0, 1, 1)
        self.urunbutonlari_layout = QtWidgets.QGridLayout()
        self.urunbutonlari_layout.setObjectName("urunbutonlari_layout")
        self.b_filtercoffee = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_filtercoffee.sizePolicy().hasHeightForWidth())
        self.b_filtercoffee.setSizePolicy(sizePolicy)
        self.b_filtercoffee.setMinimumSize(QtCore.QSize(171, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.b_filtercoffee.setFont(font)
        self.b_filtercoffee.setStyleSheet("border-radius:16px;\n"
"border-color: rgb(199, 98, 50);\n"
"background-color:rgb(160, 140, 110);\n"
"color:rgb(0, 0, 0)")
        self.b_filtercoffee.setObjectName("b_filtercoffee")
        self.urunbutonlari_layout.addWidget(self.b_filtercoffee, 0, 0, 1, 1)
        self.b_espresso = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_espresso.sizePolicy().hasHeightForWidth())
        self.b_espresso.setSizePolicy(sizePolicy)
        self.b_espresso.setMinimumSize(QtCore.QSize(171, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.b_espresso.setFont(font)
        self.b_espresso.setStyleSheet("border-radius:16px;\n"
"border-color: rgb(199, 98, 50);\n"
"background-color:rgb(160, 140, 110);\n"
"color:rgb(0, 0, 0)")
        self.b_espresso.setObjectName("b_espresso")
        self.urunbutonlari_layout.addWidget(self.b_espresso, 4, 0, 1, 1)
        self.b_americano = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_americano.sizePolicy().hasHeightForWidth())
        self.b_americano.setSizePolicy(sizePolicy)
        self.b_americano.setMinimumSize(QtCore.QSize(171, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.b_americano.setFont(font)
        self.b_americano.setStyleSheet("border-radius:16px;\n"
"border-color: rgb(199, 98, 50);\n"
"background-color:rgb(160, 140, 110);\n"
"color:rgb(0, 0, 0)")
        self.b_americano.setObjectName("b_americano")
        self.urunbutonlari_layout.addWidget(self.b_americano, 1, 0, 1, 1)
        self.b_latte = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_latte.sizePolicy().hasHeightForWidth())
        self.b_latte.setSizePolicy(sizePolicy)
        self.b_latte.setMinimumSize(QtCore.QSize(171, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.b_latte.setFont(font)
        self.b_latte.setStyleSheet("border-radius:16px;\n"
"border-color: rgb(199, 98, 50);\n"
"background-color:rgb(160, 140, 110);\n"
"color:rgb(0, 0, 0)\n"
"")
        self.b_latte.setObjectName("b_latte")
        self.urunbutonlari_layout.addWidget(self.b_latte, 5, 0, 1, 1)
        self.gridLayout.addLayout(self.urunbutonlari_layout, 1, 0, 2, 1)
        self.gridLayout_2.addWidget(self.widget, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "orders"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "cost"))
        self.delete_button.setText(_translate("Dialog", "Sil"))
        self.cancel_button.setText(_translate("Dialog", "Siparis Iptal"))
        self.ok_button.setText(_translate("Dialog", "Siparisi Onayla"))
        self.label.setText(_translate("Dialog", "Total:"))
        self.check.setText(_translate("Dialog", "0.00"))
        self.order_id_label.setText(_translate("Dialog", "ORDER"))
        self.order_id.setText(_translate("Dialog", "0001"))
        self.b_filtercoffee.setText(_translate("Dialog", "Filter Coffee"))
        self.b_espresso.setText(_translate("Dialog", "Espresso"))
        self.b_americano.setText(_translate("Dialog", "Americano"))
        self.b_latte.setText(_translate("Dialog", "Latte"))
