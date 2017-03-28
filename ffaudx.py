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
class MyWindowClass(QMainWindow, form_class):
    # variables global to this class
    fName = "none"
    videoStatus = "Video: none"
    audioStatus = "Audio: none"

    #  Modifications and initializations of the QObjects in the UI go here #
    def __init__(self, parent=None):
        super().__init__(parent)

        # bind this subclassed code  based UI to the actual UI made with Qt Designer 4
        self.ui = Ui_MainWindow()
        self.setupUi(self)

        # Window is fixed size
        self.setFixedSize(self.size())

        # extract existing defaults
        save, vid, aud = sd.updateUserData()
        # load default save directory
        self.txt_save.setText(save)
        # find and load the saved video format
        i = self.combo_video.findText(vid, Qt.MatchFixedString)
        self.combo_video.setCurrentIndex(i)
        # find and load the saved audio format
        i = self.combo_audio.findText(aud, Qt.MatchFixedString)
        self.combo_audio.setCurrentIndex(i)

        # Bind standard event handlers
        # if the function being bound to has user-defined parameters you must use lambda:
        # ex - lambda: self.btn_convert_clicked(self.fName, self.videoStatus, self.audioStatus)
        self.btn_convert.clicked.connect(self.btn_convert_clicked)
        self.btn_convert.clicked.connect(self.beginConverting)
        self.chk_video.stateChanged.connect(self.chk_video_checked)
        self.chk_audio.stateChanged.connect(self.chk_audio_checked)
        self.combo_audio.currentIndexChanged.connect(self.combo_audio_format_changed)
        self.combo_video.currentIndexChanged.connect(self.combo_video_format_changed)

        # bind custom event handlers (such as clickability to non-clickable QObjects)
        clickable(self.txt_save).connect(self.txt_save_clicked)

        # enable the right-click context menu
        self.queue_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.queue_list.connect(self.queue_list,
                                QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                                self.listItemRightClicked)

        # Allow multiple selection on the queue list - ExtendedSelection:
        # - Shift + click selects additional contiguous segments of items
        # - Ctrl + click selects additional individual files
        self.queue_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Manually set the progress bar range and create the thread that will run it
        self.progress_bar.setRange(0, 100)
        # self.conversion_task = TaskThreadObject(self.processQueue, self.queue_list)
        # self.conversion_task.progress.connect(self.onProgress)

        self.conversion_task = TaskThread(self.processQueue, self.queue_list)
        self.conversion_task.notifyProgress.connect(self.progressBarGrowth)

        self.connect(self.conversion_task, SIGNAL('updateStatusBar'), self.updateStatus)

        pprint(MyListWidget.__mro__)

    def updateStatus(self, fName, video, audio):
        self.statusBar().showMessage(
            "Converting {} - {} and {}".format(fName, video, audio))

    def beginConverting(self):
        self.conversion_task.start()

    def progressBarGrowth(self, i):
        self.progress_bar.setValue(i)

    # right-click context menu functionality #
    def listItemRightClicked(self, QPos):

        # add menu items for the right-click context menu
        menu_item_add = self.listMenu.addAction("Add Item")
        menu_item_remove = self.listMenu.addAction("Remove Item")

        # connect menu items to their respective signal handler
        # add item handler
        self.connect(menu_item_add, QtCore.SIGNAL("triggered()"), self.menu_item_add_clicked)
        # add remove item handler - only allow item removal if an item is selected
        if not self.queue_list.selectedItems():  # empty list evaluates to boolean false
            menu_item_remove.setEnabled(False)
        else:
            self.connect(menu_item_remove, QtCore.SIGNAL("triggered()"), self.menu_item_remove_clicked)

        # enable right-click context menu pop-up functionality
        parentPosition = self.queue_list.mapToGlobal(QtCore.QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()

    def menu_item_remove_clicked(self):
        # remove the highlighted items in the queue #
        for SelectedItem in self.queue_list.selectedItems():
            self.queue_list.takeItem(self.queue_list.row(SelectedItem))

    # add an item to the list
    def menu_item_add_clicked(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilenames(initialdir=sd.initLoadDir)
        print(type(file_path), file_path)
        if type(file_path) == tuple:
            for item in file_path:
                if item != "":
                    newItem = MyListWidgetItem(item, sd.initLoadDir)
                    self.queue_list.addItem(newItem)
                    print(self.queue_list.count())
                    self.queue_list.item(self.queue_list.count() - 1).setText(newItem.getData())
                    self.queue_list.item(self.queue_list.count() - 1).setSelected(True)
                    sd.updateUserData(loadDir=newItem.path)

    def txt_save_clicked(self):
        root = tk.Tk()
        root.withdraw()
        save_path = filedialog.askdirectory(initialdir=sd.initSaveDir)
        if type(save_path) == str:
            self.txt_save.setText(save_path)
            sd.updateUserData(saveDir=self.txt_save.text())

    def btn_convert_clicked(self):
        print("---Items in Conversion Queue---")
        print([str(self.queue_list.item(i).text()) for i in range(self.queue_list.count())])

    # when the user checks the video box it saves the format as default
    # and updates the conversion format of the selected items
    def chk_video_checked(self):
        if self.chk_video.isChecked():
            sd.updateUserData(vidFmt=self.combo_video.currentText())
            for item in self.queue_list.selectedItems():
                print(item.getFileType())
                self.queue_list.item(self.queue_list.row(item)).getVideo(self.combo_video.currentText())
            self.videoStatus = "Video: " + str(self.queue_list.item(0).getFileType())\
                               + " to " + self.combo_video.currentText()
        else:
            self.videoStatus = "Video: none"

    # when the user checks the audio box it saves the format as default
    # and updates the conversion format of the selected items
    def chk_audio_checked(self):
        if self.chk_audio.isChecked():
            sd.updateUserData(audFmt=self.combo_audio.currentText())
            for item in self.queue_list.selectedItems():
                print(item.getFileType())
                self.queue_list.item(self.queue_list.row(item)).getAudio(self.combo_audio.currentText())
            self.audioStatus = "Audio: " + "<insert previous format here>" + " to " + self.combo_audio.currentText()
        else:
            self.audioStatus = "Audio: none"

    def combo_audio_format_changed(self):
        sd.updateUserData(audFmt=self.combo_audio.currentText())

    def combo_video_format_changed(self):
        sd.updateUserData(vidFmt=self.combo_video.currentText())

    def processQueue(self, queue_list, item_index):

        # (re)initialize the dictionaries
        in_file_name = {}
        out_file_name = {}

        queue_item = queue_list.item(item_index)

        in_file_name[queue_item.absFilePath] = None
        # video and audio can be converted to video
        # so if the user has the video format set, make a video
        # otherwise make it audio
        if queue_item.video != "":
            out_file_name[sd.initSaveDir + "/" + queue_item.no_extension + "." + queue_item.video] = None
        else:
            out_file_name[sd.initSaveDir + "/" + queue_item.no_extension + "." + queue_item.audio] = None

            # update status bar - emit a signal to be handled by GUI - prevents QPixmap error
            self.emit(QtCore.SIGNAL('updateStatusBar'), queue_item.fName, queue_item.video, queue_item.audio)
        try:
            # -y option forces overwrite of pre-existing output files - more at https://ffmpeg.org/ffmpeg.html
            # TODO: make this optional?
            ff = ffmpy.FFmpeg(inputs=in_file_name, outputs=out_file_name, global_options="-y")
            ff.run()
            print("finished item: ", in_file_name)
            queue_list.takeItem(item_index)

        except ffmpy.FFExecutableNotFoundError as ffenf:
            print("---The FFmpeg executable was not found---\n", ffenf)

        except ffmpy.FFRuntimeError as ffre:
            print("---Runtime Error---\n",
                  "Command:", ffre.cmd,
                  "Exit Code:", ffre.exit_code,
                  "Standard Out:", ffre.stdout,
                  "Standard Error:", ffre.stderr)


# subclassed QThread to run the conversion and monitor the progress - pretty sure doing this is wrong
# but at least I'm not using moveToThread()
class TaskThread(QtCore.QThread):
    notifyProgress = QtCore.pyqtSignal(int)

    def __init__(self, func, queue_list):
        super().__init__()
        self.func = func
        self.queue_list = queue_list

    def run(self):
        """
        process each item in the list and update the progress bar
        index 0 is used because the function removes completed items
        """
        for i in range(self.queue_list.count()):
            self.func(self.queue_list, 0)
            self.notifyProgress.emit((i+1)/self.queue_list.count() * 100)  # current progress = completed / total jobs


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()

    app.exec_()
