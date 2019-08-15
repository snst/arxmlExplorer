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


class ModelTreeView():
    def __init__(self):
        self.groupDataTypes = QGroupBox('Model')
        self.treeView = QTreeView()
        #self.treeView.setRootIsDecorated(False)
        self.treeView.setAlternatingRowColors(True)
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.treeView)
        self.groupDataTypes.setLayout(dataLayout)
        self.model = self.createModelDataTypes(self)
        self.treeView.setModel(self.model)
        self.treeView.setColumnWidth(0, 250)
        self.treeView.setColumnWidth(2, 250)
        self.addModelRootNodes()
        pass

    def addModelRootNodes(self):
        self.node_datatypes = QStandardItem('Data Types' )
        self.model.appendRow(self.node_datatypes)
        self.node_application_errors = QStandardItem('Application Errors' )
        self.model.appendRow(self.node_application_errors)
        self.node_interfaces = QStandardItem('Interfaces' )
        self.model.appendRow(self.node_interfaces)
        self.node_deployment = QStandardItem('Deployment' )
        self.model.appendRow(self.node_deployment)
        self.node_machine = QStandardItem('Machine' )
        self.model.appendRow(self.node_machine)

    def createModelDataTypes(self,parent):
        model = QStandardItemModel(0, 4, None)
        model.setHeaderData(0, Qt.Horizontal, "Name")
        model.setHeaderData(1, Qt.Horizontal, "Category")
        model.setHeaderData(2, Qt.Horizontal, "namespace")
        model.setHeaderData(3, Qt.Horizontal, "Source")
        return model
    
    def add(self, parent, name, category, source, namespace='', xml_node = None):
        item = QStandardItem(name)
        parent.appendRow([item, QStandardItem(category), QStandardItem(namespace), QStandardItem(source)])
        if xml_node != None:
            item.setData(xml_node, Qt.UserRole + 1)
            pass
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
