# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'properties.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(413, 302)
        self.txt_save_dest = QtWidgets.QLineEdit(Dialog)
        self.txt_save_dest.setGeometry(QtCore.QRect(20, 120, 361, 27))
        self.txt_save_dest.setObjectName("txt_save_dest")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 100, 121, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 180, 121, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(220, 180, 121, 17))
        self.label_3.setObjectName("label_3")
        self.txt_file_name = QtWidgets.QLineEdit(Dialog)
        self.txt_file_name.setGeometry(QtCore.QRect(20, 50, 361, 27))
        self.txt_file_name.setObjectName("txt_file_name")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 30, 121, 17))
        self.label_4.setObjectName("label_4")
        self.combo_video = QtWidgets.QComboBox(Dialog)
        self.combo_video.setGeometry(QtCore.QRect(30, 200, 81, 27))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_video.sizePolicy().hasHeightForWidth())
        self.combo_video.setSizePolicy(sizePolicy)
        self.combo_video.setObjectName("combo_video")
        self.combo_video.addItem("")
        self.combo_video.setItemText(0, "")
        self.combo_video.addItem("")
        self.combo_video.addItem("")
        self.combo_video.addItem("")
        self.combo_video.addItem("")
        self.combo_video.addItem("")
        self.combo_audio = QtWidgets.QComboBox(Dialog)
        self.combo_audio.setGeometry(QtCore.QRect(220, 200, 81, 27))
        self.combo_audio.setObjectName("combo_audio")
        self.combo_audio.addItem("")
        self.combo_audio.setItemText(0, "")
        self.combo_audio.addItem("")
        self.combo_audio.addItem("")
        self.combo_audio.addItem("")
        self.btn_save = QtWidgets.QPushButton(Dialog)
        self.btn_save.setGeometry(QtCore.QRect(300, 260, 99, 27))
        self.btn_save.setObjectName("btn_save")
        self.btn_cancel = QtWidgets.QPushButton(Dialog)
        self.btn_cancel.setGeometry(QtCore.QRect(190, 260, 99, 27))
        self.btn_cancel.setObjectName("btn_cancel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Save Destination"))
        self.label_2.setText(_translate("Dialog", "Video Format"))
        self.label_3.setText(_translate("Dialog", "Audio Format"))
        self.label_4.setText(_translate("Dialog", "File Name"))
        self.combo_video.setItemText(1, _translate("Dialog", "mp4"))
        self.combo_video.setItemText(2, _translate("Dialog", "avi"))
        self.combo_video.setItemText(3, _translate("Dialog", "wma"))
        self.combo_video.setItemText(4, _translate("Dialog", "mov"))
        self.combo_video.setItemText(5, _translate("Dialog", "flv"))
        self.combo_audio.setItemText(1, _translate("Dialog", "mp3"))
        self.combo_audio.setItemText(2, _translate("Dialog", "wav"))
        self.combo_audio.setItemText(3, _translate("Dialog", "FLAC"))
        self.btn_save.setText(_translate("Dialog", "Save"))
        self.btn_cancel.setText(_translate("Dialog", "Cancel"))

