import sys
from PyQt4 import QtCore, QtGui, uic
import tkinter as tk
from tkinter import filedialog

form_class = uic.loadUiType("FFAudX.ui")[0]  # Load the UI


class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btn_convert.clicked.connect(self.btn_convert_clicked)         # Bind the event handlers
       # self.btn_FtoC.clicked.connect(self.btn_FtoC_clicked)               # to the qObjects

    def btn_convert_clicked(self):
        print(sys.platform)
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        print(file_path)


app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
