#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Stefan Schmidt
import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
QWidget, QPushButton, QDialog, QPlainTextEdit, QTabWidget, QSplitter)
from xml.dom import minidom
from MethodArgumentEditor import *
from ModelTreeView import *
from MethodArgumentsTreeView import *
from arxmlHelper import *
from MethodErrorListWidget import *
from NamespaceCache import *
from ErrorItem import *
from DatatypeItem import *
from MethodItem import *
from EventItem import *
from FieldItem import *
from MachineItem import *
from DeploymentItem import *

class App(QWidget):
  
    def __init__(self):
        super().__init__()
        self.title = 'ARXML Explorer'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 700
        self.initUI()
        path = './models/demo3'
        files = [f for f in os.listdir(path) if os.path.isfile(path + '/' + f)]
        for f in files:
            if f.endswith('.arxml'):
                self.parseXML(path + '/' + f)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.model_tree = ModelTreeView()
        self.detail = MethodArgumentsTreeView("Details")
        self.errorlist = MethodErrorListWidget()
        self.combo = MethodArgumentEditor()
        self.tabs = QTabWidget()
        self.plaintext_xml = QPlainTextEdit()
        self.plaintext_xml.resize(400,150)
        self.splitter1 = QSplitter(Qt.Vertical)

        self.splitter1.addWidget(self.model_tree.groupDataTypes)
        self.splitter1.addWidget(self.detail.groupDataTypes)
        self.splitter1.addWidget(self.tabs)

        mainLayout = QVBoxLayout()
        self.tabs.addTab(self.plaintext_xml,"XML")
        self.tabs.addTab(self.combo,"Details")
        self.tabs.addTab(self.errorlist.groupDataTypes, "Possible Errors")

        self.model_tree.treeView.selectionModel().selectionChanged.connect(self.show_model_tree_details)
        self.detail.treeView.selectionModel().selectionChanged.connect(self.show_method_parameter_details)

        self.setLayout(mainLayout)
        mainLayout.addWidget(self.splitter1)
        self.show()
        self.items_error = ErrorItem('APPLICATION-ERROR', 'Errors', self.model_tree.model)
        self.items_datatype = DatatypeItem('IMPLEMENTATION-DATA-TYPE', 'Data types', self.model_tree.model)
        self.items_method = MethodItem('CLIENT-SERVER-OPERATION', 'Methods', self.model_tree.model)
        self.items_event = EventItem('VARIABLE-DATA-PROTOTYPE', 'Events', self.model_tree.model)
        self.items_field = FieldItem('FIELD', 'Fields', self.model_tree.model)
        self.items_machine = MachineItem('MACHINE', 'Machine', self.model_tree.model)
        self.items_deployment = DeploymentItem('SOMEIP-SERVICE-INTERFACE-DEPLOYMENT', 'Deployment', self.model_tree.model)
        self.items = [self.items_error, self.items_datatype, self.items_method, self.items_event, self.items_field, self.items_machine, self.items_deployment]

                    
    def show_model_tree_details(self, selected, deselected):
        a = self.model_tree.treeView.selectedIndexes()[0]
        #print(a.data(Qt.DisplayRole))
        b = a.data(Qt.UserRole + 1)
        #print(b)
        self.detail.clear()
        if b != None:
            self.show_xml(b)
            for item in self.items:
                if item.show_detail(self.detail, b):
                    break

    def show_method_parameter_details(self, selected, deselected):
        a = self.model_tree.treeView.selectedIndexes()[0]
        print(a.data(Qt.DisplayRole))
        b = a.data(Qt.UserRole + 1)
        print(b)

        arg = self.detail.treeView.selectedIndexes()[0]
        print(arg.data(Qt.DisplayRole))
        arg_node = arg.data(Qt.UserRole + 1)
        print(arg_node)
        self.show_xml(arg_node)

        self.combo.edit_name.setText(getShortName(arg_node))
        dir_index = self.combo.cb_dir.findText(getDirection(arg_node))
        if dir_index >= 0:
            self.combo.cb_dir.setCurrentIndex(dir_index)


    def show_xml(self, node):
        str = node.toprettyxml(indent=' ', newl='')
        self.plaintext_xml.setPlainText(str)


    def parseXML(self, file):
        self.xmldoc = minidom.parse(file)
        for item in self.items:
            item.parse(self.xmldoc, file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())