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
from BaseItem import *

class EventItem(BaseItem):
    def __init__(self, xml_name, view_name, view_root_node):
        BaseItem.__init__(self, xml_name, view_name, view_root_node)
        pass

    def add(self, parent, xml_node):
        name = getShortName(xml_node)
        item = QStandardItem(name)
        parent.appendRow([item, QStandardItem(''), QStandardItem(''), QStandardItem('')])
        if xml_node != None:
            item.setData(xml_node, Qt.UserRole + 1)
            pass
        return item    


    def show_detail_impl(self, view, node):
        self.tree_view = view.treeView
        self.clear_detail(view)
        self.show_detail_data(node, view.model)
        view.treeView.expandAll()


    def show_detail_data(self, node, model):
        item = self.add_row_detail(model, 'TYPE-TREF', getType(node))


    def clear_detail(self, view):
        view.model = QStandardItemModel(0, 2, None)
        view.model.setHeaderData(0, Qt.Horizontal, "Name")
        view.model.setHeaderData(1, Qt.Horizontal, "Value")
        view.treeView.setModel(view.model)
        pass     
