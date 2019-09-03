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
        self.clear_obsolete()
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
        index = self.treeView.selectionModel().selectedIndexes()
        if index:
            a = index[0]
            xml_node = a.data(Qt.UserRole + 1)
            text = a.data(Qt.DisplayRole)
            print(xml_node)
            print(text)
            ns = text[1:].replace('/', '::')
            node = self.main.view_executable.cache.getViewNode(ns)
            print(node)
            print(node.data(Qt.DisplayRole))
            if node:
                proxy = self.main.model_tree.treeView.model()
                model = proxy.sourceModel()    
                #k = proxy.indexFromItem(node)
                #k = model.index(3, 0)
                k = model.indexFromItem(node.parent().parent())
                self.main.model_tree.treeView.setExpanded(proxy.mapFromSource(k), True)
                k2 = model.indexFromItem(node.parent())
                k3 = model.indexFromItem(node)
                self.main.model_tree.treeView.setExpanded(proxy.mapFromSource(k2), True)
                self.main.model_tree.treeView.scrollTo(proxy.mapFromSource(k2), True)
                self.main.model_tree.treeView.setCurrentIndex(proxy.mapFromSource(k3))

                #k = self.main.model_tree.model.indexFromItem(node.parent())
                #k = self.main.model_tree.model.indexFromItem(node)
                #px = self.main.model_tree.proxyModel.mapFromSource(k)
                #self.main.model_tree.treeView.selectionModel().setCurrentIndex(node.index(), QItemSelectionModel.ClearAndSelect)
                #self.main.model_tree.treeView.setExpanded(px, True)
                #self.main.model_tree.treeView.expandRecursively(k, -1)
                #self.main.model_tree.treeView.setFirstColumnSpanned(1, k, True)
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



    def clear_obsolete(self):
        if self.model != None:
            self.model.clear()
        self.model = QStandardItemModel(0, 6, None)
        self.model.setHeaderData(0, Qt.Horizontal, "Name")
        self.model.setHeaderData(1, Qt.Horizontal, "Category")
        self.model.setHeaderData(2, Qt.Horizontal, "Size")
        self.model.setHeaderData(3, Qt.Horizontal, "Semantic")
        self.model.setHeaderData(4, Qt.Horizontal, "Ref Dest")
        self.model.setHeaderData(5, Qt.Horizontal, "Source")
        self.treeView.setModel(self.model)
        self.treeView.setColumnWidth(0, 200)
        self.treeView.setColumnWidth(1, 150)
        self.treeView.setColumnWidth(4, 250)
        pass

    def clear(self):
        if self.model != None:
            self.model.clear()
        self.model = QStandardItemModel(0, 1, None)

