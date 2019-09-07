#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Stefan Schmidt
import os
import sys
from PyQt5.QtGui import QIcon, QStandardItem
from PyQt5.QtCore import *
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
QWidget, QPushButton, QDialog, QPlainTextEdit, QTabWidget)
from xml.dom import minidom
from arxmlHelper import *


class MethodArgumentsTreeView():
    def __init__(self, name, main):
        self.groupDataTypes = QGroupBox(name)
        self.treeView = QTreeView()
        self.treeView.mousePressEvent = self.mousePressEvent
        #self.treeView.setRootIsDecorated(False)
        self.treeView.setAlternatingRowColors(True)
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.treeView)
        self.groupDataTypes.setLayout(dataLayout)
        self.model = None
        self.clear()
        self.main = main
        pass

    def mousePressEvent(self, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                self.jump_to_reference()
                return
            else:
                super(QTreeView, self.treeView).mousePressEvent(event)

    def jump_to_reference(self):
        row = get_selected_tvnode_from_treeview(self.treeView)
        if row:
            text = get_text_from_tvnode(row[1])
            ns = text[1:].replace('/', '/')

            xml_node = get_xmlnode_from_tvnode(row[0])
            dest_ref = get_xml_attribute(xml_node, 'DEST')

            node = self.main.cache.get(dest_ref, ns)
            show_node(self.main.model_tree.treeView, node)

            """cache = self.main.get_cache_for(dest_ref)
            if cache:
                node = cache.getViewNode(ns)
                show_node(self.main.model_tree.treeView, node)
            else:
                node = self.main.cache.get(dest_ref, ns)
                show_node(self.main.model_tree.treeView, node)"""

            #node = self.main.view_executable.cache.getViewNode(ns)
            #show_node(self.main.model_tree.treeView, node)
        pass


    def attach_xml_node(self, item, xml_node):
        if xml_node != None:
            #print(xml_node)
            item.setData(xml_node, Qt.UserRole + 1)
            pass

    
    def add(self, name, category, source, namespace, xml_node = None):
        item = QStandardItem(name)
        self.model.appendRow([item, QStandardItem(category), QStandardItem(namespace), QStandardItem(source)])
        #
        attach_xml_node(item, xml_node)
        return item

    def clear(self):
        self.model = QStandardItemModel(0, 2, None)
        self.model.setHeaderData(0, Qt.Horizontal, 'Name')
        self.model.setHeaderData(1, Qt.Horizontal, 'Value')
        self.treeView.setModel(self.model)
        self.treeView.setColumnWidth(0, 200)

