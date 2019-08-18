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
        self.attach_xml_node(item, xml_node)
        self.attach_type(item, 'NS')
        return item

    def attach_type(self, item, str):
        item.setData(str, Qt.UserRole + 2)

    def attach_xml_node(self, item, xml_node):
        if xml_node != None:
            item.setData(xml_node, Qt.UserRole + 1)
            pass

    def show_detail(self, my_tree, xml_node):
        if xml_node.localName != self.xml_name:
            return False
        self.show_detail_impl(my_tree, xml_node)
        return True

    def add_row_detail(self, parent, name, a, b=None, xml_node = None):
        item = QStandardItem(name)
        row = [item, QStandardItem(a)]
        if b:
            row.append(QStandardItem(b))
        parent.appendRow(row)
        self.attach_xml_node(item, xml_node)
        return item

    def show_detail_impl(self, my_tree, xml_node):
        pass


    def add_row_detail2(self, parent, arg_list, xml_node = None):
        row = []
        first_item = None
        item = None
        for arg in arg_list:
            if type(arg) == list:
                item = QStandardItem(arg[0])
                item.setToolTip(arg[1])
            else:
                item = QStandardItem(arg)
            if not first_item:
                first_item = item
            row.append(item)
        parent.appendRow(row)
        self.attach_xml_node(first_item, xml_node)
        return first_item
