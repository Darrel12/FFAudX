# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FFAudX.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(419, 264)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../Downloads/d/ffmpeg-logo_400x400.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setEnabled(True)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.frame)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(230, 100, 171, 41))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.layout_audio = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.layout_audio.setObjectName(_fromUtf8("layout_audio"))
        self.chk_audio = QtGui.QCheckBox(self.horizontalLayoutWidget_2)
        self.chk_audio.setObjectName(_fromUtf8("chk_audio"))
        self.layout_audio.addWidget(self.chk_audio)
        self.combo_audio = QtGui.QComboBox(self.horizontalLayoutWidget_2)
        self.combo_audio.setObjectName(_fromUtf8("combo_audio"))
        self.combo_audio.addItem(_fromUtf8(""))
        self.combo_audio.addItem(_fromUtf8(""))
        self.combo_audio.addItem(_fromUtf8(""))
        self.combo_audio.addItem(_fromUtf8(""))
        self.combo_audio.addItem(_fromUtf8(""))
        self.layout_audio.addWidget(self.combo_audio)
        self.horizontalLayoutWidget_3 = QtGui.QWidget(self.frame)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(230, 60, 171, 41))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.layout_video = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.layout_video.setContentsMargins(1, 0, -1, -1)
        self.layout_video.setObjectName(_fromUtf8("layout_video"))
        self.chk_video = QtGui.QCheckBox(self.horizontalLayoutWidget_3)
        self.chk_video.setObjectName(_fromUtf8("chk_video"))
        self.layout_video.addWidget(self.chk_video)
        self.combo_video = QtGui.QComboBox(self.horizontalLayoutWidget_3)
        self.combo_video.setObjectName(_fromUtf8("combo_video"))
        self.combo_video.addItem(_fromUtf8(""))
        self.combo_video.addItem(_fromUtf8(""))
        self.combo_video.addItem(_fromUtf8(""))
        self.combo_video.addItem(_fromUtf8(""))
        self.combo_video.addItem(_fromUtf8(""))
        self.layout_video.addWidget(self.combo_video)
        self.verticalLayoutWidget = QtGui.QWidget(self.frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(230, 150, 171, 71))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.layout_save_progress = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.layout_save_progress.setObjectName(_fromUtf8("layout_save_progress"))
        self.txt_save = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.txt_save.setObjectName(_fromUtf8("txt_save"))
        self.layout_save_progress.addWidget(self.txt_save)
        self.progress_bar = QtGui.QProgressBar(self.verticalLayoutWidget)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName(_fromUtf8("progress_bar"))
        self.layout_save_progress.addWidget(self.progress_bar)
        self.btn_convert = QtGui.QPushButton(self.frame)
        self.btn_convert.setGeometry(QtCore.QRect(270, 20, 91, 31))
        self.btn_convert.setObjectName(_fromUtf8("btn_convert"))
        self.queue_list = MyListWidget(self.frame)
        self.queue_list.setGeometry(QtCore.QRect(10, 10, 211, 201))
        self.queue_list.setObjectName(_fromUtf8("queue_list"))
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 419, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "FFAudX", None))
        self.chk_audio.setText(_translate("MainWindow", "Audio", None))
        self.combo_audio.setItemText(0, _translate("MainWindow", "mp3", None))
        self.combo_audio.setItemText(1, _translate("MainWindow", "wav", None))
        self.combo_audio.setItemText(2, _translate("MainWindow", "m4a", None))
        self.combo_audio.setItemText(3, _translate("MainWindow", "ALAC", None))
        self.combo_audio.setItemText(4, _translate("MainWindow", "FLAC", None))
        self.chk_video.setText(_translate("MainWindow", "Video", None))
        self.combo_video.setItemText(0, _translate("MainWindow", "mp4", None))
        self.combo_video.setItemText(1, _translate("MainWindow", "avi", None))
        self.combo_video.setItemText(2, _translate("MainWindow", "wma", None))
        self.combo_video.setItemText(3, _translate("MainWindow", "mov", None))
        self.combo_video.setItemText(4, _translate("MainWindow", "flv", None))
        self.txt_save.setText(_translate("MainWindow", "Save Destination...", None))
        self.btn_convert.setText(_translate("MainWindow", "Convert", None))

from MyListWidget import MyListWidget