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

class ViewDeploymentBase(ViewBase):
    def __init__(self, xml_name, view_name, view_root_node, cache):
        ViewBase.__init__(self, xml_name, view_name, view_root_node, cache)
        pass


    def parse2(self, xml_root_node, parent_view_node):

        itemlist = xml_root_node.getElementsByTagName(self.xml_tag_name)
        if itemlist:
            sub_item = QStandardItem(self.view_name)
            parent_view_node.appendRow([sub_item, QStandardItem(''), QStandardItem(''), QStandardItem('')])

        for s in itemlist:
            self.add(sub_item, s)


    def add(self, parent, xml_node):
        name = getShortName(xml_node)
        item = QStandardItem(name)
        parent.appendRow([item, QStandardItem(''), QStandardItem(''), QStandardItem('')])
        attach_xml_node(item, xml_node)
        return item    


    def clear_detail(self, my_tree):
        my_tree.model = QStandardItemModel(0, 2, None)
        my_tree.model.setHeaderData(0, Qt.Horizontal, 'Name')
        my_tree.model.setHeaderData(1, Qt.Horizontal, 'Value')
        my_tree.treeView.setModel(my_tree.model)
        my_tree.treeView.setColumnWidth(0, 200)
        pass     
