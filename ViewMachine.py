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
from ViewBase import *

class ViewMachine(ViewBase):
    def __init__(self, view_root_node):
        ViewBase.__init__(self, 'MACHINE', 'Machine', view_root_node)
        pass

    def add(self, parent, xml_node):
        item = None
        name = getShortName(xml_node)
        if parent:
            item = QStandardItem(name)
            parent.appendRow([item, QStandardItem(''), QStandardItem(''), QStandardItem('')])
            attach_xml_node(item, xml_node)
        else:
            print("Failed to add:" + name)
        return item    
