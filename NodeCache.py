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

class NodeCache():
    def __init__(self):
        self.dict = {}
        pass

    def addViewNode(self, namespace, view_node):
        self.dict[namespace] = view_node

    def getViewNode(self, namespace):
        node = self.dict.get(namespace)
        return node

    def addViewSubNode(self, namespace, view_node, sub_node_name, column2=None):
        node = QStandardItem(sub_node_name)
        if column2:
            view_node.appendRow([node, QStandardItem(column2)])
        else:
            view_node.appendRow(node)

        self.dict[namespace + '::' + sub_node_name] = node
        return node

    def getViewSubNode(self, namespace, sub_node_name):
        node = self.dict.get(namespace + '::' + sub_node_name)
        return node

    def add(self, type_name, namespace, sub_node_name, node):
        d = self.dict.get(type_name)
        if not d:
            d = {}
            self.dict[type_name] = d
        d[namespace + '::' + sub_node_name] = node

    def get(self, type_name, name):
        ret = None
        d = self.dict.get(type_name)
        if d:
            ret = d.get(name)
        return ret

    def get_cache(self, type_name):
        ret = self.dict.get(type_name)
        if not ret:
            ret = {}
            self.dict[type_name] = ret
        return ret

    def add(self, cache_name, names, node):
        cache = self.get_cache(cache_name)
        if type(names) == list:
            name = names[0]
            for n in names[1:]:
                if n:
                    name = name + "::" + n
        else:
            name = names
        cache[name] = node
