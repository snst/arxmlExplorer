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

class NamespaceCache():
    def __init__(self):
        self.dict = {}
        pass

    def addViewNode(self, namespace, view_node):
        self.dict[namespace] = view_node

    def getViewNode(self, namespace):
        node = self.dict.get(namespace)
        return node

    def addViewSubNode(self, namespace, view_node, sub_node_name):
        node = QStandardItem(sub_node_name)
        view_node.appendRow(node)
        self.dict[namespace + '&&' + sub_node_name] = node
        return node

    def getViewSubNode(self, namespace, sub_node_name):
        node = self.dict.get(namespace + '&&' + sub_node_name)
        return node
