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

class ViewDataType(ViewBase):
    def __init__(self, view_root_node):
        ViewBase.__init__(self, 'IMPLEMENTATION-DATA-TYPE', 'Data Types', view_root_node)
        pass

    def add_to_treeview(self, parent, xml_node):
        name = getShortName(xml_node)
        item = QStandardItem(name)
        parent.appendRow([item, QStandardItem(getCategory(xml_node)), QStandardItem(''), QStandardItem('')])
        attach_xml_node(item, xml_node)
        return item    


    def clear_detail(self, my_tree):
        my_tree.model = QStandardItemModel(0, 5, None)
        my_tree.model.setHeaderData(0, Qt.Horizontal, "Name")
        my_tree.model.setHeaderData(1, Qt.Horizontal, "Category")
        my_tree.model.setHeaderData(2, Qt.Horizontal, "Size")
        my_tree.model.setHeaderData(3, Qt.Horizontal, "Semantic")
        my_tree.model.setHeaderData(4, Qt.Horizontal, "Ref Dest")
        my_tree.treeView.setModel(my_tree.model)
        my_tree.treeView.setColumnWidth(0, 200)
        my_tree.treeView.setColumnWidth(1, 150)
        my_tree.treeView.setColumnWidth(4, 250)
        pass                

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
        attach_xml_node(item, node)

        sub_element = findFirstChildNodeByName(node, 'SUB-ELEMENTS')
        if sub_element:
            itemlist = getDirectChildNodesByName(sub_element, 'IMPLEMENTATION-DATA-TYPE-ELEMENT')
            for s in itemlist:
                self.show_datatype(s, item)
        pass
