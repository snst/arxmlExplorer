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
    def __init__(self, xml_name, view_name, view_root_node, cache):
        BaseItem.__init__(self, xml_name, view_name, view_root_node, cache)
        pass

    def add(self, parent, xml_node):
        name = getShortName(xml_node)
        item = QStandardItem(name)
        parent.appendRow([item, QStandardItem(''), QStandardItem(''), QStandardItem('')])
        self.attach_xml_node(item, xml_node)
        return item    


    def show_detail_impl(self, my_tree, xml_node):
        self.tree_view = my_tree.treeView
        self.clear_detail(my_tree)
        self.show_detail_data(my_tree.model, xml_node)
        my_tree.treeView.expandAll()


    def show_detail_data(self, view_node, xml_node):
        item = self.add_row_detail(view_node, 'TYPE-TREF', getType(xml_node))
        item = self.add_row_detail(view_node, 'HAS-GETTER', getValueByName(xml_node, 'HAS-GETTER'))
        item = self.add_row_detail(view_node, 'HAS-NOTIFIER', getValueByName(xml_node, 'HAS-NOTIFIER'))
        item = self.add_row_detail(view_node, 'HAS-SETTER', getValueByName(xml_node, 'HAS-SETTER'))


    def clear_detail(self, my_tree):
        my_tree.model = QStandardItemModel(0, 2, None)
        my_tree.model.setHeaderData(0, Qt.Horizontal, 'Name')
        my_tree.model.setHeaderData(1, Qt.Horizontal, 'Value')
        my_tree.treeView.setModel(my_tree.model)
        my_tree.treeView.setColumnWidth(0, 100)
        pass     
