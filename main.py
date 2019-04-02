import sys, re
from analysis_v2 import *
from PyQt5 import QtWidgets, QtGui, QtCore, QtSvg
from gui.design import Ui_MainWindow


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent=parent)
        self.setupUi(self)
        self.buildButton.clicked.connect(self.sql_to_graph)

    def sql_to_graph(self):
        sql = self.inputBox.toPlainText()

        # Prepare string
        sql = sql.lower()
        sql = re.sub(r"\n+", " ", sql)
        sql = re.sub(r"\t+", " ", sql)
        sql = re.sub(r"\s+", " ", sql)

        sql_graph = sql_to_graph(sql)
        self.outputBox.setText(sql_graph[0])
        draw_graph(sql_graph[1])
        self.horizontalLayout.removeWidget(self.svgWidget)
        self.svgWidget = QtSvg.QSvgWidget('graph_gd.svg')
        self.svgWidget.setMinimumSize(QtCore.QSize(500, 0))
        self.horizontalLayout.addWidget(self.svgWidget)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
