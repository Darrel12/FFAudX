from PyQt4.QtGui import QAbstractItemView, QFrame, QListWidget, QListWidgetItem
from PyQt4.QtCore import Qt
import os
from mimetypes import MimeTypes
from urllib import request
from PyQt4 import QtGui, QtCore
import savedData as sd
from pytube import YouTube


# Customized list widget item to hold more data than just the absolute path of the item #
class MyListWidgetItem(QListWidgetItem):
    def __init__(self, path, dest):
        super().__init__()

        self.absFilePath = path

        # determine if new item is a url or file path - handle accordingly
        if os.path.exists(path):
            print("path exists:", path)
            # extract the path without the filename and render it back to a string
            self.path = '/'.join(path.split('/')[0:-1]) + '/'
            # print("directory path: " + self.path)  # idk if this is useful anymore
            # extract the last part of the path to get the file name
            self.fName = path.split('/')[-1]
            # file name without the extension
            self.no_extension = self.fName.split('.')[0]
            # use MimeTypes to determine the file type
            self.fType = identifyItem(path)
            # set the save destination for when the conversion is done
            self.fDest = dest
            # the audio/video type to convert to if they have one - blank by default
            # TODO maybe make them the currently checked values? or reset checked values when adding new item?
            self.audio = ""
            self.video = ""
        else:
            print("Pathhh:", path)
            # TODO put something here? see how this corresponds to the above self.path
            self.path = path
            self.yt = YouTube(path)
            # use the youtube scraper to get the youtube video name
            self.no_extension = self.yt.filename
            self.fName = self.no_extension + "." + sd.initVidFmt

            self.fType = ('youtube/video', None)  # save a custom mime-type TODO extract the mime type from the metadata
            self.fDest = dest
            self.audio = ""
            self.video = ""
            print("fType:", self.fType)

    def __repr__(self):
        return self.fName

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
                print(url)
                path = url.toLocalFile()
                if os.path.isfile(path):
                    self.addItem(MyListWidgetItem(path, sd.initSaveDir).fName)
                else:
                    item = MyListWidgetItem(url.toString(), sd.initSaveDir)
                    print("Youtube Video:", item)
                    self.addItem(item)
                    self.item(self.count()-1).setText(item.fName)
                    self.item(self.count()-1).setSelected(True)
        else:
            # default internal drop
            super(MyListWidget, self).dropEvent(event)

    # noinspection PyArgumentList
    def keyPressEvent(self, event):
        """
        Assign the following functions to keystrokes
        delete     ->   delete the highlighted items
        ctrl + a   ->   highlight all items in the queue
        :param event: signal event to determine if it's a keyboard event
        """
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
