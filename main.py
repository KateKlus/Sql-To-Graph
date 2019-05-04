import sys
import re
import os
from analysis_v2 import *
from PyQt5 import QtWidgets, QtGui, QtCore, QtSvg, QtXml
from gui.design import Ui_MainWindow
from QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from shutil import copyfile


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent=parent)
        self.setupUi(self)
        self.buildButton.clicked.connect(self.sql_to_graph)
        self.cleanButton.clicked.connect(self.clean)
        self.downloadButton.clicked.connect(self.download)
        global sql_graph
        sql_graph = ""

    def sql_to_graph(self):
        global sql_graph
        sql = self.inputBox.toPlainText()

        # Prepare string
        sql = sql.lower()
        sql = re.sub(r"\n+", " ", sql)
        sql = re.sub(r"\t+", " ", sql)
        sql = re.sub(r"\s+", " ", sql)

        sql_graph = sql_to_graph(sql)
        self.outputBox.setText(sql_graph[0])
        draw_graph(sql_graph[1])
        graph_dom = QtXml.QDomDocument('graph_gd')
        graph_svg = QtCore.QFile('graph_gd.svg')
        graph_dom.setContent(graph_svg)
        self.svgWidget.load(graph_dom.toByteArray())

    def download(self):
        global sql_graph
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save sql-graph", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
        graph_txt = open(fileName + ".txt", "w+")
        graph_txt.write(sql_graph[0])
        copyfile('graph_gd.svg', fileName + ".svg")

    def clean(self):
        global sql_graph
        sql_graph = ""
        clean()
        os.remove("graph_gd.svg")
        self.outputBox.setText("")
        self.inputBox.setText("")
        clean_dom = QtXml.QDomDocument('clean_dom')
        clean_svg = QtCore.QFile('clean.svg')
        clean_dom.setContent(clean_svg)
        self.svgWidget.load(clean_dom.toByteArray())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
