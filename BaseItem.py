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
from NamespaceCache import *
from arxmlHelper import *

class BaseItem():
    def __init__(self, xml_name, view_name, view_root_node):
        self.cache = NamespaceCache()
        self.xml_name = xml_name
        self.view_root_node = QStandardItem(view_name)
        view_root_node.appendRow(self.view_root_node)
        pass

    def get_namespace_view_node(self, xml_node, file):
        namespace = getNameSpace(xml_node)
        view_namespace_node = self.cache.getViewNode(namespace)
        if not view_namespace_node:
            view_namespace_node = self.add_namespace(self.view_root_node, namespace, file, xml_node)
            self.cache.addViewNode(namespace, view_namespace_node)
        return view_namespace_node


    def parse(self, xml_root_node, file):
        itemlist = xml_root_node.getElementsByTagName(self.xml_name)
        for s in itemlist:
            view_node_namespace = self.get_namespace_view_node(s, file)
            self.add(view_node_namespace, s)

    def add_namespace(self, parent, namespace, file, xml_node):
        item = QStandardItem(namespace)
        parent.appendRow([item, QStandardItem(''), QStandardItem(''), QStandardItem(file)])
        if xml_node != None:
            item.setData(xml_node, Qt.UserRole + 1)
            pass
        return item



