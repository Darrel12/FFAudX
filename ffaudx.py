# /usr/bin/python3

import sys
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import tkinter as tk
from tkinter import filedialog
import ffmpy
import inspect
from EventFilters import clickable

import savedData as sd
from MyListWidget import *
from youtubeScraper import scrape, convertItem

from pprint import pprint

from gui import Ui_MainWindow   # this imports some functionality
                                # for the ui created by running
                                # "pyuic4 FFAudX.ui > gui.py"
                                # in the directory containing the ui


# print the names and signals of all QObjects because there isn't a list anywhere #
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
class MyWindowClass(QMainWindow):
    # variables global to this class
    fName = "none"
    videoStatus = "Video: none"
    audioStatus = "Audio: none"

    #  Modifications and initializations of the QObjects in the UI go here #
    def __init__(self, parent=None):
        super(MyWindowClass, self).__init__(parent)

        # bind this subclassed UI to the actual UI made with Qt Designer 4
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Window is fixed size
        self.setFixedSize(self.size())

        # extract existing defaults
        save, vid, aud = sd.updateUserData()
        # load default save directory
        self.ui.txt_save.setText(save)
        # find and load the saved video format
        i = self.ui.combo_video.findText(vid, Qt.MatchFixedString)
        self.ui.combo_video.setCurrentIndex(i)
        # find and load the saved audio format
        i = self.ui.combo_audio.findText(aud, Qt.MatchFixedString)
        self.ui.combo_audio.setCurrentIndex(i)

        # Bind standard event handlers
        # if the function being bound to has user-defined parameters you must use lambda:
        # ex - lambda: self.btn_convert_clicked(self.fName, self.videoStatus, self.audioStatus)
        self.ui.btn_convert.clicked.connect(self.beginConverting)
        self.ui.chk_video.stateChanged.connect(self.chk_video_checked)
        self.ui.chk_audio.stateChanged.connect(self.chk_audio_checked)
        self.ui.combo_audio.currentIndexChanged.connect(self.combo_audio_format_changed)
        self.ui.combo_video.currentIndexChanged.connect(self.combo_video_format_changed)

        # bind custom event handlers (such as clickability to non-clickable QObjects)
        clickable(self.ui.txt_save).connect(self.txt_save_clicked)

        # enable the right-click context menu
        self.ui.queue_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.queue_list.connect(self.ui.queue_list,
                                   QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                                   self.listItemRightClicked)

        # Allow multiple selection on the queue list - ExtendedSelection:
        # - Shift + click selects additional contiguous segments of items
        # - Ctrl + click selects additional individual files
        self.ui.queue_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Manually set the progress bar range and create the thread that will run it
        self.ui.progress_bar.setRange(0, 100)
        # self.conversion_task = TaskThreadObject(self.processQueue, self.ui.queue_list)
        # self.conversion_task.progress.connect(self.onProgress)

        self.mainThread = QThread()
        self.mainThread.start()

        self.conversion_task = TaskThread(self.processQueue, self.ui.queue_list)
        self.conversion_task.moveToThread(self.mainThread)
        self.conversion_task.notifyProgress.connect(self.progressBarGrowth)

        self.connect(self.conversion_task, SIGNAL('updateStatusBar'), self.updateStatus)

        pprint(MyListWidget.__mro__)

    def updateStatus(self, fName, video, audio):
        self.statusBar().showMessage(
            "Converting {} - {} and {}".format(fName, video, audio))

    def beginConverting(self):
        if self.ui.btn_convert.text() == "Convert":
            self.conversion_task.start()
            self.ui.btn_convert.setText("Cancel")
        else:
            self.ui.btn_convert.setText("Convert")
            self.conversion_task.stop()
            self.mainThread.quit()
            self.mainThread.wait()


    def progressBarGrowth(self, i):
        self.ui.progress_bar.setValue(i)

    # right-click context menu functionality #
    def listItemRightClicked(self, QPos):
        self.listMenu = QtGui.QMenu()

        # add menu items for the right-click context menu
        menu_item_add = self.listMenu.addAction("Add Item")
        menu_item_remove = self.listMenu.addAction("Remove Item")

        # connect menu items to their respective signal handler
        # add item handler
        self.connect(menu_item_add, QtCore.SIGNAL("triggered()"), self.menu_item_add_clicked)
        # add remove item handler - only allow item removal if an item is selected
        if not self.ui.queue_list.selectedItems():  # empty list evaluates to boolean false
            menu_item_remove.setEnabled(False)
        else:
            self.connect(menu_item_remove, QtCore.SIGNAL("triggered()"), self.menu_item_remove_clicked)

        # enable right-click context menu pop-up functionality
        parentPosition = self.ui.queue_list.mapToGlobal(QtCore.QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()

    def menu_item_remove_clicked(self):
        # remove the highlighted items in the queue #
        for SelectedItem in self.ui.queue_list.selectedItems():
            self.ui.queue_list.takeItem(self.ui.queue_list.row(SelectedItem))

    # add an item to the list
    def menu_item_add_clicked(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilenames(initialdir=sd.initLoadDir)
        print(type(file_path), file_path)
        if type(file_path) == tuple:
            for item in file_path:
                if item:
                    newItem = MyListWidgetItem(item, sd.initLoadDir)
                    self.ui.queue_list.addItem(newItem)
                    print(self.ui.queue_list.count())
                    self.ui.queue_list.item(self.ui.queue_list.count() - 1).setText(newItem.getData())
                    self.ui.queue_list.item(self.ui.queue_list.count() - 1).setSelected(True)
                    sd.updateUserData(loadDir=newItem.path)

    def txt_save_clicked(self):
        root = tk.Tk()
        root.withdraw()
        save_path = filedialog.askdirectory(initialdir=sd.initSaveDir)
        if type(save_path) == str:
            self.ui.txt_save.setText(save_path)
            sd.updateUserData(saveDir=self.ui.txt_save.text())


    # when the user checks the video box it saves the format as default
    # and updates the conversion format of the selected items
    def chk_video_checked(self):
        if self.ui.chk_video.isChecked():
            sd.updateUserData(vidFmt=self.ui.combo_video.currentText())
            for item in self.ui.queue_list.selectedItems():
                print("item:", item)
                print(item.getFileType())
                self.ui.queue_list.item(self.ui.queue_list.row(item)).getVideo(self.ui.combo_video.currentText())
            self.videoStatus = "Video: " + str(self.ui.queue_list.item(0).getFileType())\
                               + " to " + self.ui.combo_video.currentText()
        else:
            self.videoStatus = "Video: none"

    # when the user checks the audio box it saves the format as default
    # and updates the conversion format of the selected items
    def chk_audio_checked(self):
        if self.ui.chk_audio.isChecked():
            sd.updateUserData(audFmt=self.ui.combo_audio.currentText())
            for item in self.ui.queue_list.selectedItems():
                print("item:", item)
                print(item.fType)
                self.ui.queue_list.item(self.ui.queue_list.row(item)).getAudio(self.ui.combo_audio.currentText())
            self.audioStatus = "Audio: " + "<insert previous format here>" + " to " + self.ui.combo_audio.currentText()
        else:
            self.audioStatus = "Audio: none"

    def combo_audio_format_changed(self):
        sd.updateUserData(audFmt=self.ui.combo_audio.currentText())

    def combo_video_format_changed(self):
        sd.updateUserData(vidFmt=self.ui.combo_video.currentText())

    # currently this makes 1 item dictionaries and processes entries individually -- TODO fix this
    def processQueue(self, queue_list, item_index):

        queue_item = queue_list.item(item_index)

        # update status bar - emit a signal to be handled by GUI
        # This prevents QPixmap error by not handling UI objects outside the UI class
        self.emit(QtCore.SIGNAL('updateStatusBar'), queue_item.fName, queue_item.video, queue_item.audio)

        if 'youtube' in queue_item.fType[0]:
            print("Scraping:", queue_item.path)
            scrape(queue_list, queue_item)
        else:
            self.convertItem(queue_list, item_index)


# subclassed QThread to run the conversion and monitor the progress - pretty sure doing this is wrong
# but at least I'm not using moveToThread()
class TaskThread(QThread):
    notifyProgress = pyqtSignal(int)

    def __init__(self, func, queue_list):
        super().__init__()
        self.func = func
        self.queue_list = queue_list
        self._isRunning = True

    def stop(self):
        self._isRunning = False

    def run(self):
        """
        process each item in the list and update the progress bar
        index 0 is used because the function removes completed items
        """
        list_count = self.queue_list.count()
        for i in range(list_count):
            if self._isRunning:
                self.func(self.queue_list, 0)
                self.notifyProgress.emit((i+1)/list_count * 100)  # current progress = completed / total jobs



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()

    app.exec_()
