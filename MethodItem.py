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

class MethodItem(BaseItem):
    def __init__(self, xml_name, view_name, view_root_node):
        BaseItem.__init__(self, xml_name, view_name, view_root_node)
        pass

    def add(self, parent, xml_node):
        name = getShortName(xml_node)
        item = QStandardItem(name)
        parent.appendRow([item, QStandardItem(''), QStandardItem(''), QStandardItem('')])
        self.attach_xml_node(item, xml_node)
        return item    

    def show_detail_impl(self, view, node):
        self.tree_view = view.treeView
        self.clear_detail(view)
        self.show_method(node, view.model)
        view.treeView.expandAll()


    def show_method_param(self, node, parent):
        item = QStandardItem(getShortName(node))
        #QStandardItem(getNameSpace(node))
        namespace = QStandardItem(getType(node))
        #namespace.setToolTip('namespace')
        parent.appendRow([item, QStandardItem(getDirection(node)), namespace])
        self.attach_xml_node(item, node)
        return item

    def show_method_error(self, node, parent):
        error_name = getXmlContent(node)
        error_number = '' # self.model_tree.get_application_error_value(error_name)
        n = QStandardItem(error_name)
        parent.appendRow([n])
        k = parent.rowCount()
        self.tree_view.setFirstColumnSpanned(k-1, parent.index(), True)


    def show_method(self, node, model):

        #Fire-And-Forget
        item = self.add_row_detail(model, 'Fire-And-Forget', getFireAndForget(node), '')

        # methode name
        #item = self.add_row_detail(model, getShortName(node), '', QStandardItem(getNameSpace(node)), node)
        item = self.add_row_detail(model, 'Arguments', '', '')
        #method arguments
        itemlist = node.getElementsByTagName('ARGUMENT-DATA-PROTOTYPE')
        for s in itemlist:
            self.show_method_param(s, item)

        #method errors
        item = self.add_row_detail(model, 'Possible Errors', '', '')
        itemlist = node.getElementsByTagName('POSSIBLE-ERROR-REF')
        for s in itemlist:
            self.show_method_error(s, item)

    def clear_detail(self, view):
        view.model = QStandardItemModel(0, 3, None)
        view.model.setHeaderData(0, Qt.Horizontal, "Name")
        view.model.setHeaderData(1, Qt.Horizontal, "Value")
        view.model.setHeaderData(2, Qt.Horizontal, "Ref Dest")
        view.treeView.setModel(view.model)
        view.treeView.setColumnWidth(0, 200)
        view.treeView.setColumnWidth(1, 150)
        #view.treeView.setColumnWidth(1, 250)
        pass     
