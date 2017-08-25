# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(370, 240)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(120, 180, 111, 51))
        self.startButton.setObjectName("startButton")
        self.usernameLabel = QtWidgets.QLabel(self.centralwidget)
        self.usernameLabel.setGeometry(QtCore.QRect(10, 20, 101, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.usernameLabel.setFont(font)
        self.usernameLabel.setObjectName("usernameLabel")
        self.username = QtWidgets.QLineEdit(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(130, 20, 211, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.username.setFont(font)
        self.username.setObjectName("username")
        self.passwordLabel = QtWidgets.QLabel(self.centralwidget)
        self.passwordLabel.setGeometry(QtCore.QRect(10, 70, 91, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setObjectName("passwordLabel")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(130, 70, 211, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.password.setFont(font)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.editCheckedRadio = QtWidgets.QRadioButton(self.centralwidget)
        self.editCheckedRadio.setGeometry(QtCore.QRect(30, 130, 131, 19))
        self.editCheckedRadio.setObjectName("editCheckedRadio")
        self.editResearchRadio = QtWidgets.QRadioButton(self.centralwidget)
        self.editResearchRadio.setGeometry(QtCore.QRect(200, 130, 151, 19))
        self.editResearchRadio.setObjectName("editResearchRadio")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "自动点击小程序"))
        self.startButton.setText(_translate("MainWindow", "开始运行"))
        self.usernameLabel.setText(_translate("MainWindow", "用户名称"))
        self.passwordLabel.setText(_translate("MainWindow", "用户密码"))
        self.editCheckedRadio.setText(_translate("MainWindow", "更改未验证"))
        self.editResearchRadio.setText(_translate("MainWindow", "更改调查类型"))

