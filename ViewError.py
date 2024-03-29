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

class ViewError(ViewBase):
    def __init__(self, view_root_node, cache):
        ViewBase.__init__(self, 'APPLICATION-ERROR', 'Errors', view_root_node, cache)
        pass

    def add_to_treeview(self, tv_parent, xml_node):
        name = getShortName(xml_node)
        item = QStandardItem(name)
        tv_parent.appendRow([item, QStandardItem(getXmlErrorCode(xml_node)), QStandardItem(''), QStandardItem('')])
        attach_xml_node(item, xml_node)
        return item    
