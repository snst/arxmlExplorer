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

class DatatypeItem(BaseItem):
    def __init__(self, xml_name, view_name, view_root_node):
        BaseItem.__init__(self, xml_name, view_name, view_root_node)
        pass

    def add(self, parent, xml_node):
        name = getShortName(xml_node)
        item = QStandardItem(name)
        parent.appendRow([item, QStandardItem(getCategory(xml_node)), QStandardItem(''), QStandardItem('')])
        if xml_node != None:
            item.setData(xml_node, Qt.UserRole + 1)
            pass
        return item    

    def show_detail_impl(self, view, node):
        self.clear_detail(view)
        self.show_datatype(node, view.model)
        view.treeView.expandAll()
        return True

    def clear_detail(self, view):
        view.model = QStandardItemModel(0, 5, None)
        view.model.setHeaderData(0, Qt.Horizontal, "Name")
        view.model.setHeaderData(1, Qt.Horizontal, "Category")
        view.model.setHeaderData(2, Qt.Horizontal, "Size")
        view.model.setHeaderData(3, Qt.Horizontal, "Semantic")
        view.model.setHeaderData(4, Qt.Horizontal, "Ref Dest")
        view.treeView.setModel(view.model)
        view.treeView.setColumnWidth(0, 200)
        view.treeView.setColumnWidth(1, 150)
        view.treeView.setColumnWidth(4, 250)
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
        self.attach_xml_node(item, node)

        sub_element = findFirstChildNodeByName(node, 'SUB-ELEMENTS')
        if sub_element:
            itemlist = getDirectChildNodesByName(sub_element, 'IMPLEMENTATION-DATA-TYPE-ELEMENT')
            for s in itemlist:
                self.show_datatype(s, item)
        pass
