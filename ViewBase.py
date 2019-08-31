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

class ViewBase():
    def __init__(self, xml_tag_name, view_name, view_root_node, cache = None):
        if cache:
            self.cache = cache
        else:
            self.cache = NamespaceCache()
        self.xml_tag_name = xml_tag_name
        self.view_name = view_name
        self.view_root_node = view_root_node


    def get_tv_namespace_node(self, xml_node, file):
        namespace = getNameSpace(xml_node)
        view_namespace_node = self.cache.getViewNode(namespace)
        if not view_namespace_node:
            view_namespace_node = self.add_tv_namespace_node(self.view_root_node, namespace, file, xml_node)
            #attach_xml_node(view_namespace_node, xml_node)
            self.cache.addViewNode(namespace, view_namespace_node)

        if self.view_name:
            node = self.cache.getViewSubNode(namespace, self.view_name)
            if not node:
                node = self.cache.addViewSubNode(namespace, view_namespace_node, self.view_name)
            return node
        else:
            return view_namespace_node


    def parse(self, xml_node, file):
        itemlist = xml_node.getElementsByTagName(self.xml_tag_name)
        for s in itemlist:
            tv_parent = self.get_tv_namespace_node(s, file)
            self.add_to_treeview(tv_parent, s)


    def add_tv_namespace_node(self, parent, namespace, file, xml_node):
        item = QStandardItem(namespace)
        parent.appendRow([item, QStandardItem(''), QStandardItem(''), QStandardItem(file)])
        attach_xml_node(item, xml_node)
        attach_type(item, 'NS')
        return item


    def show_detail(self, tree_view, xml_node):
        if xml_node.localName != self.xml_tag_name:
            return False
        self.show_detail_impl(tree_view, xml_node)
        return True

    def show_detail_impl(self, my_tree, xml_node):
        pass


    def add_tv_row_detail(self, parent, arg_list, xml_node = None):
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
        attach_xml_node(first_item, xml_node)
        return first_item
