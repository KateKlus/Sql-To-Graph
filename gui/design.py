# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1172, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.inputBox = QtWidgets.QTextEdit(self.centralwidget)
        self.inputBox.setMaximumSize(QtCore.QSize(500, 16777215))
        self.inputBox.setObjectName("inputBox")
        self.horizontalLayout.addWidget(self.inputBox)
        self.outputBox = QtWidgets.QTextBrowser(self.centralwidget)
        self.outputBox.setMaximumSize(QtCore.QSize(500, 16777215))
        self.outputBox.setObjectName("outputBox")
        self.horizontalLayout.addWidget(self.outputBox)

        # self.label = QtWidgets.QLabel(self.centralwidget)
        # self.label.setMinimumSize(QtCore.QSize(500, 0))
        # self.label.setText("")
        # self.label.setObjectName("label")
        # self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.inputBox.setStyleSheet("QLineEdit { background-color : white; }")
        self.svgWidget = QtSvg.QSvgWidget('')
        self.horizontalLayout.addWidget(self.svgWidget)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.Buttons = QtWidgets.QHBoxLayout()
        self.Buttons.setObjectName("Buttons")
        self.buildButton = QtWidgets.QPushButton(self.centralwidget)
        self.buildButton.setObjectName("buildButton")
        self.Buttons.addWidget(self.buildButton)
        self.cleanButton = QtWidgets.QPushButton(self.centralwidget)
        self.cleanButton.setObjectName("cleanButton")
        self.Buttons.addWidget(self.cleanButton)
        self.downloadButton = QtWidgets.QPushButton(self.centralwidget)
        self.downloadButton.setObjectName("downloadButton")
        self.Buttons.addWidget(self.downloadButton)
        self.verticalLayout.addLayout(self.Buttons)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1172, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SQL to graph"))
        self.buildButton.setText(_translate("MainWindow", "Build"))
        self.cleanButton.setText(_translate("MainWindow", "Clean"))
        self.downloadButton.setText(_translate("MainWindow", "Save to"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.inputBox.setPlaceholderText(_translate("MainWindow", "Input SQL-query here"))


