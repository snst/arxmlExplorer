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


class App(QWidget):
  
    def __init__(self):
        super().__init__()
        self.title = 'ARXML Explorer'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 700
        self.cache_datatypes = NamespaceCache()
        self.cache_errors = NamespaceCache()
        self.cache_methods = NamespaceCache()
        self.cache_events = NamespaceCache()
        self.cache_fields = NamespaceCache()
        #self.error_items = ErrorItem()
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
        #mainLayout.addWidget(self.model_tree.groupDataTypes)
        #mainLayout.addWidget(self.detail.groupDataTypes)
        #mainLayout.addWidget(self.tabs)

        self.tabs.addTab(self.plaintext_xml,"XML")
        self.tabs.addTab(self.combo,"Details")
        self.tabs.addTab(self.errorlist.groupDataTypes, "Possible Errors")

        self.model_tree.treeView.selectionModel().selectionChanged.connect(self.show_model_tree_details)
        self.detail.treeView.selectionModel().selectionChanged.connect(self.show_method_parameter_details)

        self.setLayout(mainLayout)
        mainLayout.addWidget(self.splitter1)
        self.show()

    def show_details_method_obsolete(self, node):
        itemlist = node.getElementsByTagName('ARGUMENT-DATA-PROTOTYPE')
        for s in itemlist:
            self.detail.add(getShortName(s), getDirection(s), getType(s), getNameSpace(s), s)

        self.errorlist.clear()
        itemlist = node.getElementsByTagName('POSSIBLE-ERROR-REF')
        for s in itemlist:
            error_name = getXmlContent(s)
            error_number = self.model_tree.get_application_error_value(error_name)
            self.errorlist.add(error_name, error_number)
            pass

    def show_details_method(self, node):
        self.detail.clear_method()
        self.detail.show_method(node, self.detail.model)
        self.detail.treeView.expandAll()

    def show_details_datatype(self, node):
        self.detail.clear_data_type()
        self.detail.show_datatype(node, self.detail.model)
        self.detail.treeView.expandAll()
        pass
                    
    def show_model_tree_details(self, selected, deselected):
        a = self.model_tree.treeView.selectedIndexes()[0]
        #print(a.data(Qt.DisplayRole))
        b = a.data(Qt.UserRole + 1)
        #print(b)
        self.detail.clear()
        if b != None:
            self.show_xml(b)
            if b.localName == 'CLIENT-SERVER-OPERATION':
                self.show_details_method(b)
            elif b.localName == 'IMPLEMENTATION-DATA-TYPE':
                self.show_details_datatype(b)
    
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

    def get_namespace_view_node(self, xml_node, cache, view_root_node, file):
        namespace = getNameSpace(xml_node)
        view_namespace_node = cache.getViewNode(namespace)
        if not view_namespace_node:
            view_namespace_node = self.model_tree.add(view_root_node, namespace, '', file, '', xml_node)
            cache.addViewNode(namespace, view_namespace_node)
        return view_namespace_node


    def parse_datatypes(self, xml_node, file):
        itemlist = xml_node.getElementsByTagName('IMPLEMENTATION-DATA-TYPE')
        for s in itemlist:
            view_node_namespace = self.get_namespace_view_node(s, self.cache_datatypes, self.model_tree.node_datatypes, file)
            self.model_tree.add(view_node_namespace, getShortName(s), getCategory(s), '', '', s)

    def parse_errors(self, xml_node, file):
        itemlist = xml_node.getElementsByTagName('APPLICATION-ERROR')
        for s in itemlist:
            view_node_namespace = self.get_namespace_view_node(s, self.cache_errors, self.model_tree.node_application_errors, file)
            self.model_tree.add(view_node_namespace, getShortName(s), getXmlErrorCode(s), '', '', s)

    def parse_methods(self, xml_node, file):
        itemlist = xml_node.getElementsByTagName('CLIENT-SERVER-OPERATION')
        for s in itemlist:
            view_node_namespace = self.get_namespace_view_node(s, self.cache_methods, self.model_tree.node_methods, file)
            self.model_tree.add(view_node_namespace, getShortName(s), '', '', '', s)

    def parse_events(self, xml_node, file):
        itemlist = xml_node.getElementsByTagName('VARIABLE-DATA-PROTOTYPE')
        for s in itemlist:
            view_node_namespace = self.get_namespace_view_node(s, self.cache_events, self.model_tree.node_events, file)
            self.model_tree.add(view_node_namespace, getShortName(s), '', '', '', s)

    def parse_fields(self, xml_node, file):
        itemlist = xml_node.getElementsByTagName('FIELD')
        for s in itemlist:
            view_node_namespace = self.get_namespace_view_node(s, self.cache_fields, self.model_tree.node_fields, file)
            self.model_tree.add(view_node_namespace, getShortName(s), '', '', '', s)

    def parseXML(self, file):
        self.xmldoc = minidom.parse(file)
        self.parse_datatypes(self.xmldoc, file)
        self.parse_errors(self.xmldoc, file)
        self.parse_methods(self.xmldoc, file)
        self.parse_fields(self.xmldoc, file)
        self.parse_events(self.xmldoc, file)

    
        itemlist = self.xmldoc.getElementsByTagName('SOMEIP-SERVICE-INTERFACE-DEPLOYMENT')
        for s in itemlist:
            self.model_tree.add(self.model_tree.node_deployment, getShortName(s), '', file, getNameSpace(s), s)
    
        itemlist = self.xmldoc.getElementsByTagName('MACHINE')
        for s in itemlist:
            self.model_tree.add(self.model_tree.node_machine, getShortName(s), '', file, getNameSpace(s), s)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())