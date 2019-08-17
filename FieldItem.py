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

class FieldItem(BaseItem):
    def __init__(self, xml_name, view_name, view_root_node):
        BaseItem.__init__(self, xml_name, view_name, view_root_node)
        pass

    def add(self, parent, xml_node):
        name = getShortName(xml_node)
        item = QStandardItem(name)
        parent.appendRow([item, QStandardItem(''), QStandardItem(''), QStandardItem('')])
        self.attach_xml_node(item, xml_node)
        return item    


    def show_detail_impl(self, view, node):
        self.tree_view = view.treeView
        self.clear_detail(view)
        self.show_detail_data(node, view.model)
        view.treeView.expandAll()


    def show_detail_data(self, node, model):
        item = self.add_row_detail(model, 'TYPE-TREF', getType(node))
        item = self.add_row_detail(model, 'HAS-GETTER', getValueByName(node, 'HAS-GETTER'))
        item = self.add_row_detail(model, 'HAS-NOTIFIER', getValueByName(node, 'HAS-NOTIFIER'))
        item = self.add_row_detail(model, 'HAS-SETTER', getValueByName(node, 'HAS-SETTER'))


    def clear_detail(self, view):
        view.model = QStandardItemModel(0, 2, None)
        view.model.setHeaderData(0, Qt.Horizontal, 'Name')
        view.model.setHeaderData(1, Qt.Horizontal, 'Value')
        view.treeView.setModel(view.model)
        view.treeView.setColumnWidth(0, 100)
        pass     
