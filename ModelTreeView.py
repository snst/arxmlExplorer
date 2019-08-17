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

class MyFilter(QSortFilterProxyModel):
    def __init__(self):
        QSortFilterProxyModel.__init__(self)
        self.str_filter = ''
        pass

    def filterAcceptsRow (self, source_row, source_parent):
        index0 = self.sourceModel().index(source_row, 0, source_parent);
        str = self.sourceModel().data(index0)
        ns = index0.data(Qt.UserRole + 2)
        arg_node = source_parent.data(Qt.UserRole + 1)
        c = True
        if not self.str_filter=='' and ns == 'NS':
            if not self.str_filter in str:
                c = False
        #a = self.sourceModel()
        return c

class ModelTreeView():
    def __init__(self):
        self.groupDataTypes = QGroupBox('Model')
        self.textbox_filter = QLineEdit()
        self.textbox_filter.returnPressed.connect(self.on_filter_updated)
        self.treeView = QTreeView()
        #self.treeView.setRootIsDecorated(False)
        self.treeView.setAlternatingRowColors(True)
        dataLayout = QVBoxLayout()
        dataLayout.addWidget(self.textbox_filter)
        dataLayout.addWidget(self.treeView)
        self.groupDataTypes.setLayout(dataLayout)

        self.model = self.createModelDataTypes(self)
        self.proxyModel = MyFilter()
        self.proxyModel.setDynamicSortFilter(True)
        self.proxyModel.setSourceModel(self.model)

        self.treeView.setModel(self.proxyModel)
        self.treeView.setColumnWidth(0, 350)
        self.treeView.setColumnWidth(2, 250)

        self.root_node_model = QStandardItem('Model')
        self.model.appendRow(self.root_node_model)
        pass

    def on_filter_updated(self):
        str = self.textbox_filter.text()
        self.update_filter(str)

    def update_filter(self, str_filter):
        self.proxyModel.str_filter = str_filter
        self.proxyModel.invalidateFilter()

    def createModelDataTypes(self,parent):
        model = QStandardItemModel(0, 4, None)
        model.setHeaderData(0, Qt.Horizontal, "Name")
        model.setHeaderData(1, Qt.Horizontal, "Value")
        model.setHeaderData(2, Qt.Horizontal, "")
        model.setHeaderData(3, Qt.Horizontal, "Source")
        return model
    
    def add(self, parent, name, category, source, namespace='', xml_node = None):
        item = QStandardItem(name)
        parent.appendRow([item, QStandardItem(category), QStandardItem(namespace), QStandardItem(source)])
        self.attach_xml_node(item, xml_node)
        return item

    def get_application_error_value(self, name):

        child_count = self.node_application_errors.rowCount()
        n = self.node_application_errors
        for i in range(child_count):
            #l = self.node_application_errors.takeRow(i)
            err = n.child(i,2).data(Qt.DisplayRole) + "/" + n.child(i,0).data(Qt.DisplayRole)
            err_no = n.child(i,1).data(Qt.DisplayRole)
            err = "/" + err.replace("::", "/")
            if name == err:
                #print(err)
                #print(err_no)
                return err_no

        return 'not found'
        """child_count = node.childCount()
        for i in range(child_count):
            item = node.child(i)
            print(item.text(0) + item.text(1))"""
