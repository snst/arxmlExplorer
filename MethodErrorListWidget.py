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


class MethodErrorListWidget():
    def __init__(self):
        self.groupDataTypes = QGroupBox('')
        self.treeView = QTreeView()
        self.treeView.setRootIsDecorated(False)
        self.treeView.setAlternatingRowColors(True)
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.treeView)
        self.groupDataTypes.setLayout(dataLayout)
        self.model = None
        self.clear()
        pass

    
    def add(self, name, error_number, xml_node = None):

        item = QStandardItem(error_number)
        self.model.appendRow([item, QStandardItem(name)])
        if xml_node != None:
            #print(xml_node)
            item.setData(xml_node, Qt.UserRole + 1)
            pass
        return item

    def clear(self):
        #self.model.clear()
        #self.model.setHeaderData(0, Qt.Horizontal, "POSSIBLE-ERROR-REFS")
        if self.model != None:
            self.model.clear()
        self.model = QStandardItemModel(0, 2, None)
        self.model.setHeaderData(0, Qt.Horizontal, "Error Code")
        self.model.setHeaderData(1, Qt.Horizontal, "POSSIBLE-ERROR-REFS")
        self.treeView.setModel(self.model)
        #self.treeView.setColumnWidth(0, 350)
        pass
