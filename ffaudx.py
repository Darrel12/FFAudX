# /usr/bin/python3

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
import tkinter as tk
from tkinter import filedialog
from EventFilters import clickable
from MyListWidget import *
from youtubeScraper import scrape, convertItem
import copy

from pprint import pprint

from gui import Ui_MainWindow   # this imports some functionality
                                # for the ui created by running
                                # "pyuic4 FFAudX.ui > gui.py"
                                # in the directory containing the ui

from prop import Ui_Dialog


# print the names and signals of all QObjects because there isn't a list anywhere #
# import inspect
# for name in dir(QtGui):
#     obj = getattr(QtGui, name)
#     if inspect.isclass(obj) and issubclass(obj, QtCore.QObject):
#         for name2 in dir(obj):
#             obj2 = getattr(obj, name2)
#             if isinstance(obj2, QtCore.pyqtSignal):
#                 print(name, name2)


# Load the UI to be modified with the following Subclassed QMainWindow
form_class = uic.loadUiType("FFAudX.ui")[0]


# Subclass the main window #
def processQueue(queue_list, item_index):

    queue_item = queue_list.item(item_index)

    # update status bar - emit a signal to be handled by GUI
    # This prevents QPixmap error by not handling UI objects outside the UI class
    # self.emit(QtCore.SIGNAL('updateStatusBar'), queue_item.fName, queue_item.video, queue_item.audio)

    if 'youtube' in queue_item.fType[0]:
        print("Scraping:", queue_item.path)
        scrape(queue_list, queue_item)
    else:
        convertItem(queue_list, item_index)


class PropertiesDialog(QDialog):
    def __init__(self, queue_item, queue_list):

        # bind the ui
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # capture the values from the selected list item
        self.original_item = copy.deepcopy(queue_item)
        self.queue_item = queue_item
        self.queue_list = queue_list
        self.ui.combo_audio.setCurrentText(queue_item.audio)
        self.ui.combo_video.setCurrentText(queue_item.video)
        self.ui.txt_file_name.setText(queue_item.no_extension)
        self.ui.txt_save_dest.setText(queue_item.fDest)

        clickable(self.ui.txt_save_dest).connect(self.txt_save_clicked)

        # signal handlers for buttons clicked
        self.ui.btn_save.clicked.connect(lambda: self.save_values(queue_item))
        self.ui.btn_cancel.clicked.connect(self.close)  # cancel the window without making changes

    def txt_save_clicked(self):
        root = tk.Tk()
        root.withdraw()
        save_path = filedialog.askdirectory(initialdir=sd.initSaveDir)
        if type(save_path) == str:
            self.ui.txt_save_dest.setText(save_path)

    # save the values and close the window
    def save_values(self, queue_item):
        # update the items values with the fields values
        queue_item.audio = self.ui.combo_audio.currentText()
        queue_item.video = self.ui.combo_video.currentText()
        queue_item.no_extension = self.ui.txt_file_name.text()
        queue_item.fDest = self.ui.txt_save_dest.text()
        # get the item that is currently highlighted
        curr = self.queue_list.currentItem()
        # update the list item's name with whatever is in the respective text field
        # this is necessary because the custom item's display name must be manually updated
        # procedure: get the row of the item, get the item at that row, update it's text
        self.queue_list.item(self.queue_list.row(curr)).setText(queue_item.no_extension)
        self.close()


class MyWindowClass(QMainWindow):
    # variables global to this class
    fName = "none"
    videoStatus = "Video: none"
    audioStatus = "Audio: none"

    #  Modifications and initializations of the QObjects in the UI go here #
    def __init__(self, parent=None):
        super(MyWindowClass, self).__init__(parent)

        # bind this subclassed UI to the actual UI made with Qt Creator
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
        self.ui.queue_list.customContextMenuRequested[QtCore.QPoint].connect(self.listItemRightClicked)

        # Allow multiple selection on the queue list - ExtendedSelection:
        # - Shift + click selects additional contiguous segments of items
        # - Ctrl + click selects additional individual files
        self.ui.queue_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Manually set the progress bar range and create the thread that will run it
        self.ui.progress_bar.setRange(0, 100)

        self.mainThread = QThread()
        self.mainThread.start()

        self.conversion_task = TaskThread(processQueue, self.ui.queue_list)
        self.conversion_task.moveToThread(self.mainThread)
        self.conversion_task.notifyProgress.connect(self.progressBarGrowth)
        self.conversion_task.revertButton.connect(self.revertButtonText)
        self.conversion_task.statusChange.connect(self.updateStatus)

        # dynamically update the drop-down combos and check boxes with the highlighted item's properties
        self.ui.queue_list.itemSelectionChanged.connect(self.update_combos)

        pprint(MyListWidget.__mro__)

    def update_combos(self):
        print("------------------------------- attempting to update")
        selected = self.ui.queue_list.selectedItems()
        if len(selected) == 1:
            selected = selected[0]
            print("------------------------------- updating")
            self.ui.combo_video.setCurrentText(selected.video)
            self.ui.combo_audio.setCurrentText(selected.audio)
            self.ui.chk_video.setChecked(True if selected.video else False)
            self.ui.chk_audio.setChecked(True if selected.audio else False)
        elif not selected:
            self.ui.chk_audio.setChecked(False)
            self.ui.chk_video.setChecked(False)

    def revertButtonText(self):
        self.ui.btn_convert.setText("Convert")

    def updateStatus(self, fName, video, audio):
        self.statusBar().showMessage("Converting {} to {}".format(fName, video if video else audio))

    def beginConverting(self):
        if self.ui.btn_convert.text() == "Convert":
            self.ui.progress_bar.setValue(0)
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
    # noinspection PyAttributeOutsideInit
    def listItemRightClicked(self, QPos):
        # noinspection PyAttributeOutsideInit
        self.listMenu = QMenu()

        # add menu items for the right-click context menu
        # noinspection PyArgumentList
        self.listMenu.addAction(QAction("Add Item", self, triggered=self.menu_item_add_clicked))
        menu_item_remove = self.listMenu.addAction("Remove Item")
        menu_item_properties = self.listMenu.addAction("Properties")

        highlighted_items = self.ui.queue_list.selectedItems()

        if not highlighted_items or len(highlighted_items) > 1:
            menu_item_properties.setEnabled(False)
        else:
            menu_item_properties.triggered.connect(self.properties_clicked)
            # TODO update the drop-downs

        # connect menu items to their respective signal handler
        # add item handler
        # add remove item handler - only allow item removal if an item is selected
        if not self.ui.queue_list.selectedItems():  # empty list evaluates to boolean false
            menu_item_remove.setEnabled(False)
        else:
            # noinspection PyUnresolvedReferences
            menu_item_remove.triggered.connect(self.menu_item_remove_clicked)

        # enable right-click context menu pop-up functionality
        parentPosition = self.ui.queue_list.mapToGlobal(QtCore.QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()

    def properties_clicked(self):
        item = PropertiesDialog(self.ui.queue_list.selectedItems()[0], self.ui.queue_list)
        item.exec_()

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
                    newItem = MyListWidgetItem(item, sd.initLoadDir,
                                               self.ui.chk_video.isChecked(), self.ui.combo_video.currentText(),
                                               self.ui.chk_audio.isChecked(), self.ui.combo_audio.currentText())
                    self.ui.queue_list.addItem(newItem)
                    print(self.ui.queue_list.count())
                    self.ui.queue_list.item(self.ui.queue_list.count() - 1).setText(newItem.no_extension)
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
        # only audio or video is allowed, not both
        if self.ui.chk_video.isChecked():
            self.ui.chk_audio.setEnabled(False)
            self.ui.combo_audio.setEnabled(False)
            sd.updateUserData(vidFmt=self.ui.combo_video.currentText())
            for item in self.ui.queue_list.selectedItems():
                print("item:", item)
                print(item.fType)
                self.ui.queue_list.item(self.ui.queue_list.row(item)).getVideo(self.ui.combo_video.currentText())
        else:
            self.ui.chk_audio.setEnabled(True)
            self.ui.combo_audio.setEnabled(True)
            for item in self.ui.queue_list.selectedItems():
                self.ui.queue_list.item(self.ui.queue_list.row(item)).video = ''

    # when the user checks the audio box it saves the format as default
    # and updates the conversion format of the selected items
    def chk_audio_checked(self):
        if self.ui.chk_audio.isChecked():
            self.ui.chk_video.setEnabled(False)
            self.ui.combo_video.setEnabled(False)
            sd.updateUserData(audFmt=self.ui.combo_audio.currentText())
            for item in self.ui.queue_list.selectedItems():
                print("item:", item)
                print(item.fType)
                self.ui.queue_list.item(self.ui.queue_list.row(item)).getAudio(self.ui.combo_audio.currentText())
        else:
            self.ui.chk_video.setEnabled(True)
            self.ui.combo_video.setEnabled(True)
            for item in self.ui.queue_list.selectedItems():
                self.ui.queue_list.item(self.ui.queue_list.row(item)).audio = ''

    def combo_audio_format_changed(self):
        sd.updateUserData(audFmt=self.ui.combo_audio.currentText())
        if self.ui.chk_audio.isChecked():
            self.chk_audio_checked()

    def combo_video_format_changed(self):
        sd.updateUserData(vidFmt=self.ui.combo_video.currentText())
        if self.ui.chk_video.isChecked():
            self.chk_video_checked()

    # currently this makes 1 item dictionaries and processes entries individually -- TODO fix this


# subclassed QThread to run the conversion and monitor the progress - pretty sure doing this is wrong
# but at least I'm not using moveToThread()
class TaskThread(QThread):
    # signals to emit that will be handled by the GUI
    notifyProgress = pyqtSignal(int)
    revertButton = pyqtSignal(str)
    statusChange = pyqtSignal(str, str, str)

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
                currentItem = self.queue_list.item(0)
                self.statusChange.emit(currentItem.fName, currentItem.video, currentItem.audio)
                self.func(self.queue_list, 0)
                self.notifyProgress.emit((i+1)/list_count * 100)  # current progress = completed / total jobs
        self.revertButton.emit("Convert")
        # self.notifyProgress.emit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    app.exec_()
