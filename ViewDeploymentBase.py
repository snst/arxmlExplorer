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

class ViewDeploymentBase(BaseItem):
    def __init__(self, xml_name, view_name, view_root_node, cache):
        BaseItem.__init__(self, xml_name, view_name, view_root_node, cache)
        pass

    def parse(self, xml_root_node, file):
        itemlist = xml_root_node.getElementsByTagName(self.xml_name)
        for s in itemlist:
            view_node_namespace = self.get_namespace_view_node(s, file)
            self.add(view_node_namespace, s)

    def parse2(self, xml_root_node, parent_view_node):

        itemlist = xml_root_node.getElementsByTagName(self.xml_name)
        if itemlist:
            sub_item = QStandardItem(self.view_name)
            parent_view_node.appendRow([sub_item, QStandardItem(''), QStandardItem(''), QStandardItem('')])

        for s in itemlist:
            #view_node_namespace = self.get_namespace_view_node(s, file)
            self.add(sub_item, s)


    def add(self, parent, xml_node):
        name = getShortName(xml_node)
        item = QStandardItem(name)
        
        if parent:
            parent.appendRow([item, QStandardItem(''), QStandardItem(''), QStandardItem('')])
            attach_xml_node(item, xml_node)
        else:
            print("Failed to add2:" + name)
        return item    

    def show_detail_impl(self, my_tree, xml_node):
        self.tree_view = my_tree.treeView
        self.clear_detail(my_tree)
        self.show_detail_methods(my_tree.model, xml_node)
        my_tree.treeView.expandAll()

    def show_detail_methods(self, my_tree, xml_node):
        pass


    def clear_detail(self, my_tree):
        my_tree.model = QStandardItemModel(0, 2, None)
        my_tree.model.setHeaderData(0, Qt.Horizontal, 'Name')
        my_tree.model.setHeaderData(1, Qt.Horizontal, 'Value')
        my_tree.treeView.setModel(my_tree.model)
        my_tree.treeView.setColumnWidth(0, 200)
        pass     
