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

class ViewMethod(ViewBase):
    def __init__(self, view_root_node, cache):
        ViewBase.__init__(self, 'CLIENT-SERVER-OPERATION', 'Methods', view_root_node, cache)
        pass

    def add_to_treeview(self, parent, xml_node):
        name = getShortName(xml_node)
        item = QStandardItem(name)
        parent.appendRow([item, QStandardItem(''), QStandardItem(''), QStandardItem('')])
        attach_xml_node(item, xml_node)
        return item    


    def show_method_param(self, node, parent):
        item = QStandardItem(getShortName(node))
        #QStandardItem(getNameSpace(node))
        namespace = QStandardItem(getType(node))
        #namespace.setToolTip('namespace')
        parent.appendRow([item, QStandardItem(getDirection(node)), namespace])
        attach_xml_node(item, node)
        return item

    def show_method_error(self, node, parent):
        error_name = getXmlContent(node)
        error_number = '' # self.model_tree.get_application_error_value(error_name)
        n = QStandardItem(error_name)
        parent.appendRow([n])
        k = parent.rowCount()
        self.tree_view.setFirstColumnSpanned(k-1, parent.index(), True)


    def show_detail_data(self, model, node):

        #Fire-And-Forget
        item = self.add_tv_row_detail(model, ['Fire-And-Forget', getFireAndForget(node)])

        # methode name
        item = self.add_tv_row_detail(model, ['Arguments'])
        #method arguments
        itemlist = node.getElementsByTagName('ARGUMENT-DATA-PROTOTYPE')
        for s in itemlist:
            self.show_method_param(s, item)

        #method errors
        item = self.add_tv_row_detail(model, ['Possible Errors'])
        itemlist = node.getElementsByTagName('POSSIBLE-ERROR-REF')
        for s in itemlist:
            self.show_method_error(s, item)

    def clear_detail(self, my_tree):
        my_tree.model = QStandardItemModel(0, 3, None)
        my_tree.model.setHeaderData(0, Qt.Horizontal, "Name")
        my_tree.model.setHeaderData(1, Qt.Horizontal, "Value")
        my_tree.model.setHeaderData(2, Qt.Horizontal, "Ref Dest")
        my_tree.treeView.setModel(my_tree.model)
        my_tree.treeView.setColumnWidth(0, 200)
        my_tree.treeView.setColumnWidth(1, 150)
        #my_tree.treeView.setColumnWidth(1, 250)
        pass     
