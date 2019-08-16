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
from arxmlHelper import *


class MethodArgumentsTreeView():
    def __init__(self, name):
        self.groupDataTypes = QGroupBox(name)
        self.treeView = QTreeView()
        #self.treeView.setRootIsDecorated(False)
        self.treeView.setAlternatingRowColors(True)
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.treeView)
        self.groupDataTypes.setLayout(dataLayout)
        self.model = None
        self.clear_obsolete()
        pass

    def attach_xml_node(self, item, xml_node):
        if xml_node != None:
            #print(xml_node)
            item.setData(xml_node, Qt.UserRole + 1)
            pass

    
    def add(self, name, category, source, namespace, xml_node = None):
        item = QStandardItem(name)
        self.model.appendRow([item, QStandardItem(category), QStandardItem(namespace), QStandardItem(source)])
        #
        self.attach_xml_node(item, xml_node)
        return item



    def clear_obsolete(self):
        if self.model != None:
            self.model.clear()
        self.model = QStandardItemModel(0, 6, None)
        self.model.setHeaderData(0, Qt.Horizontal, "Name")
        self.model.setHeaderData(1, Qt.Horizontal, "Category")
        self.model.setHeaderData(2, Qt.Horizontal, "Size")
        self.model.setHeaderData(3, Qt.Horizontal, "Semantic")
        self.model.setHeaderData(4, Qt.Horizontal, "Ref Dest")
        self.model.setHeaderData(5, Qt.Horizontal, "Source")
        self.treeView.setModel(self.model)
        self.treeView.setColumnWidth(0, 200)
        self.treeView.setColumnWidth(1, 150)
        self.treeView.setColumnWidth(4, 250)
        pass

    def clear(self):
        if self.model != None:
            self.model.clear()
        self.model = QStandardItemModel(0, 1, None)

