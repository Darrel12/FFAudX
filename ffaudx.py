import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import tkinter as tk
from tkinter import filedialog
import ffmpy
import inspect
from EventFilters import clickable

import savedData as sd
from MyListWidget import *

from gui import Ui_MainWindow   # this imports some functionality
                                # for the ui created by running
                                # "pyuic4 FFAudX.ui > gui.py"
                                # in the directory containing the ui


# print the signals of all QObjects because there isn't a list anywhere #
for name in dir(QtGui):
    obj = getattr(QtGui, name)
    if inspect.isclass(obj) and issubclass(obj, QtCore.QObject):
        for name2 in dir(obj):
            obj2 = getattr(obj, name2)
            if isinstance(obj2, QtCore.pyqtSignal):
                print(name, name2)


# Load the UI to be modified with the following Subclassed QMainWindow
form_class = uic.loadUiType("FFAudX.ui")[0]



# Subclass the main window #
class MyWindowClass(QMainWindow, form_class):
    # variables global to this class
    fName = "none"
    videoStatus = "Video: none"
    audioStatus = "Audio: none"

    #  Modifications and initializations of the QObjects in the UI go here #
    def __init__(self, parent=None):
        super().__init__(parent)

        # bind this subclassed code based UI to the actual UI made with Qt Designer 4
        self.ui = Ui_MainWindow()
        self.setupUi(self)

        # Window is fixed size
        self.setFixedSize(self.size())

        # load defaults for the user if they exist
        self.txt_save.setText(sd.updateUserData())

        # Bind standard event handlers - if the function being bound to has user-defined parameters you must use lambda as shown below
        self.btn_convert.clicked.connect(lambda: self.btn_convert_clicked(self.fName, self.videoStatus, self.audioStatus))
        self.chk_video.stateChanged.connect(self.chk_video_checked)
        self.chk_audio.stateChanged.connect(self.chk_audio_checked)

        # bind custom event handlers (such as clickability to non-clickable QObjects)
        clickable(self.txt_save).connect(self.txt_save_clicked)

        # enable the right-click context menu
        self.queue_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.queue_list.connect(self.queue_list,
                                QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                                self.listItemRightClicked)



    # right-click context menu functionality #
    def listItemRightClicked(self, QPos):
        self.listMenu = QtGui.QMenu()

        # add menu items here
        menu_item_add = self.listMenu.addAction("Add Item")
        menu_item_remove = self.listMenu.addAction("Remove Item")

        # connect menu items to their respective signal handler
        # add item handler
        self.connect(menu_item_add, QtCore.SIGNAL("triggered()"), self.menu_item_add_clicked)
        # add remove item handler - only allow item removal if an item is selected
        if self.queue_list.selectedItems() == []:
            menu_item_remove.setEnabled(False)
        else:
            self.connect(menu_item_remove, QtCore.SIGNAL("triggered()"), self.menu_item_remove_clicked)

        # enable right-click context menu pop-up functionality
        parentPosition = self.queue_list.mapToGlobal(QtCore.QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()


    # remove the highlighted items in the queue #
    def menu_item_remove_clicked(self):
        for SelectedItem in self.queue_list.selectedItems():
            self.queue_list.takeItem(self.queue_list.row(SelectedItem))



    # add an item to the list
    def menu_item_add_clicked(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(initialdir=sd.initLoadDir)
        if type(file_path) == str:
            newItem = MyListWidgetItem(file_path, sd.initLoadDir)
            self.queue_list.addItem(newItem)
            self.queue_list.item(0).setText(newItem.getData())
            sd.updateUserData(loadDir=newItem.path)

    def txt_save_clicked(self):
        root = tk.Tk()
        root.withdraw()
        save_path = filedialog.askdirectory(initialdir=sd.initSaveDir)
        if type(save_path) == str:
            self.txt_save.setText(save_path)
            sd.updateUserData(saveDir=self.txt_save.text())

    def btn_convert_clicked(self, fName, videoStatus, audioStatus):
        print("---Items in Conversion Queue---")
        print([str(self.queue_list.item(i).text()) for i in range(self.queue_list.count())])
        self.statusBar().showMessage("Converting {} - {} and {}".format(fName, videoStatus, audioStatus))

    def chk_video_checked(self):
        if self.chk_video.isChecked():
            self.videoStatus = "Video: " + str(self.queue_list.item(0).getFileType()) + " to " + self.combo_video.currentText()
        else:
            self.videoStatus = "Video: none"

    def chk_audio_checked(self):
        if self.chk_audio.isChecked():
            self.audioStatus = "Audio: " + "<insert previous format here>" + " to " + self.combo_audio.currentText()
        else:
            self.audioStatus = "Audio: none"



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    app.exec_()
