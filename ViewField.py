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

class ViewField(ViewBase):
    def __init__(self,  view_root_node, cache):
        ViewBase.__init__(self, 'FIELD', 'Fields',  view_root_node, cache)
        pass

    def show_detail_default(self, view_node, xml_node):
        item = self.add_tv_row_detail(view_node, ['TYPE-TREF', getType(xml_node)])
        item = self.add_tv_row_detail(view_node, ['HAS-GETTER', getValueByNameT(xml_node, 'HAS-GETTER')])
        item = self.add_tv_row_detail(view_node, ['HAS-NOTIFIER', getValueByNameT(xml_node, 'HAS-NOTIFIER')])
        item = self.add_tv_row_detail(view_node, ['HAS-SETTER', getValueByNameT(xml_node, 'HAS-SETTER')])


    def clear_detail(self, my_tree):
        my_tree.model = QStandardItemModel(0, 2, None)
        my_tree.model.setHeaderData(0, Qt.Horizontal, 'Name')
        my_tree.model.setHeaderData(1, Qt.Horizontal, 'Value')
        my_tree.treeView.setModel(my_tree.model)
        my_tree.treeView.setColumnWidth(0, 100)
        pass     
