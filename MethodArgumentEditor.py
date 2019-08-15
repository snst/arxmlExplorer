#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Stefan Schmidt
import os
import sys
from PyQt5.QtGui import QIcon, QStandardItem
from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
QTime, pyqtSlot, QObject, pyqtSignal)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
QWidget, QPushButton, QDialog, QPlainTextEdit, QTabWidget)
from xml.dom import minidom

class MethodArgumentEditor(QWidget):
    def __init__(self, parent = None):
        super(MethodArgumentEditor, self).__init__(parent)
        
        layout = QGridLayout()

        self.label_name = QLabel()
        self.label_name.setText("Name:")
        self.edit_name = QLineEdit()

        self.label_type = QLabel()
        self.label_type.setText("Type:")
        self.cb_type = QComboBox()
        


        self.label_direction = QLabel()
        self.label_direction.setText("Direction:")

        self.cb_dir = QComboBox()
        self.cb_dir.addItems(["IN", "OUT"])
        self.cb_dir.currentIndexChanged.connect(self.selectionchange)
        
        layout.addWidget(self.label_name,0,0)
        layout.addWidget(self.edit_name,0,1)
        layout.addWidget(self.label_direction)
        layout.addWidget(self.cb_dir)
        layout.addWidget(self.label_type)
        layout.addWidget(self.cb_type)

        self.setLayout(layout)
    
    def selectionchange(self,i):
        for count in range(self.cb.count()):
            print(self.cb.itemText(count))
        print("Current index",i,"selection changed ",self.cb.currentText())
    
