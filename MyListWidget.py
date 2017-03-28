from PyQt4.QtGui import QAbstractItemView, QFrame, QListWidget, QListWidgetItem
from PyQt4.QtCore import Qt
import os
from mimetypes import MimeTypes
from urllib import request
from PyQt4 import QtGui, QtCore
import savedData as sd


# Customized list widget item to hold more data than just the absolute path of the item #
class MyListWidgetItem(QListWidgetItem):
    def __init__(self, path, dest):
        super().__init__()

        self.absFilePath = path
        # extract the path without the filename and render it back to a string
        self.path = '/'.join(path.split('/')[0:-1]) + '/'
        print("directory path: " + self.path)
        # extract the last part of the path to get the file name - this will become a function once we deal with web links
        self.fName = path.split('/')[-1]
        # file name without the extension
        self.no_extension = self.fName.split('.')[0]
        # use MimeTypes to determine the file type
        self.fType = identifyItem(path)
        # set the save destination for when the conversion is done
        self.fDest = dest
        # the audio/video type to convert to if they have one
        self.audio = ""
        self.video = ""

    def getAudio(self, audio=""):
        if audio != "":
            self.audio = audio
        return self.audio

    def getVideo(self, video=""):
        if video != "":
            self.video = video
        return self.video

    def getFileType(self):
        return self.fType

    def getData(self):
        return self.fName



# identify the type of item the user is adding to the queue #
def identifyItem(path):
    """
    :param path: the file path or url the user is providing
    :return: the type of file the user is providing
    """
    mime = MimeTypes()
    url = request.pathname2url(path)
    mime_type = mime.guess_type(url)
    print("MimeType: " + str(mime_type))
    return mime_type

# Customized list widget to allow internal/external drag-and-drop actions #
class MyListWidget(QListWidget):
    def __init__(self, parent):
        super(MyListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setFrameShadow(QFrame.Plain)
        self.setFrameShape(QFrame.Box)

    # do stuff if a dragged item enters the widget #
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(MyListWidget, self).dragEnterEvent(event)

    # do stuff repeatedly if a dragged item is moving around in the widget #
    def dragMoveEvent(self, event):
        super(MyListWidget, self).dragMoveEvent(event)


    # handle internal and external drag-and-drop actions #
    def dropEvent(self, event):
        # handle external drop
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                print("url: " + str(url))
                path = url.toLocalFile()
                if os.path.isfile(path):
                    self.addItem(MyListWidgetItem(path, sd.initSaveDir).fName)
        else:
            # default internal drop
            super(MyListWidget, self).dropEvent(event)

    # Assign functions to keys:
    #   delete
    #   ctrl + a
    def keyPressEvent(self, event):
        modifiers = QtGui.QApplication.keyboardModifiers()
        if event.key() == Qt.Key_Delete:
            self._del_item()
        elif modifiers == QtCore.Qt.ControlModifier and event.key() == Qt.Key_A:
            self._highlight_all()

    # remove the selected item
    def _del_item(self):
        for item in self.selectedItems():
            self.takeItem(self.row(item))

    # highlight all items in the list
    def _highlight_all(self):
        self.selectAll()
