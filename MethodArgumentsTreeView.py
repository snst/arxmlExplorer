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
from arxmlHelper import *


class MethodArgumentsTreeView():
    def __init__(self, name):
        self.groupDataTypes = QGroupBox(name)
        self.treeView = QTreeView()
        #self.treeView.setRootIsDecorated(False)
        self.treeView.setAlternatingRowColors(True)
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.treeView)
        self.groupDataTypes.setLayout(dataLayout)
        self.model = None
        self.clear_obsolete()
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
        self.attach_xml_node(item, xml_node)
        return item


    def show_datatype_element(self, node, parent):
        name = getShortName(node)
        category = getCategory(node)
        impl_type = getXmlImplementationDataTypeRef(node)
        if None == impl_type:
            impl_type = getXmlBaseTypeRef(node)

        array_size = getXmlArraySize(node)
        array_size_semantic = getXmlArraySizeSemantics(node)
        item = QStandardItem(name)
        parent.appendRow([item, QStandardItem(category), QStandardItem(array_size), QStandardItem(array_size_semantic), QStandardItem(impl_type)])
        return item

    def show_datatype(self, node, model):
        nodecopy = node.cloneNode(True)
        removeAllChildNodesWithName(nodecopy, 'SUB-ELEMENTS')
        item = self.show_datatype_element(nodecopy, model)
        self.attach_xml_node(item, node)

        sub_element = findFirstChildNodeByName(node, 'SUB-ELEMENTS')
        if sub_element:
            itemlist = getDirectChildNodesByName(sub_element, 'IMPLEMENTATION-DATA-TYPE-ELEMENT')
            for s in itemlist:
                #self.show_datatype_element(s, item)
                self.show_datatype(s, item)

        
        pass

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

    def clear_data_type(self):
        if self.model != None:
            self.model.clear()
        self.model = QStandardItemModel(0, 5, None)
        self.model.setHeaderData(0, Qt.Horizontal, "Name")
        self.model.setHeaderData(1, Qt.Horizontal, "Category")
        self.model.setHeaderData(2, Qt.Horizontal, "Size")
        self.model.setHeaderData(3, Qt.Horizontal, "Semantic")
        self.model.setHeaderData(4, Qt.Horizontal, "Ref Dest")
        self.treeView.setModel(self.model)
        self.treeView.setColumnWidth(0, 200)
        self.treeView.setColumnWidth(1, 150)
        self.treeView.setColumnWidth(4, 250)
        pass        