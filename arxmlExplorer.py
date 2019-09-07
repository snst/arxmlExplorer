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
from NodeCache import *
from ViewError import *
from ViewDataType import *
from ViewMethod import *
from ViewEvent import *
from ViewField import *
from ViewMachine import *
from ViewDeployment import *
from NamespaceCache import *
from ViewModeDeclaration import *
from ViewEthernet import *
from ViewMachine import *
from ViewProcess import *
from ViewExecutable import *
from ViewStartupConfig import *
from ViewApplication import *
from ViewAdaptiveSwComponent import *

class App(QWidget):
  
    def __init__(self):
        super().__init__()
        self.title = 'ARXML Explorer'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 700
        self.model_cache = NamespaceCache()
        self.deploy_cache = NamespaceCache()
        self.cache = NodeCache()
        self.views = []
        self.initUI()
        path = './models/demo7'
        files = [f for f in os.listdir(path) if os.path.isfile(path + '/' + f)]
        for f in files:
            if f.endswith('.arxml'):
                self.parseXML(path + '/' + f)


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.model_tree = ModelTreeView()
        self.detail = MethodArgumentsTreeView("Details", self)
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
        #self.tabs.addTab(self.combo,"Details")
        #self.tabs.addTab(self.errorlist.groupDataTypes, "Possible Errors")

        self.model_tree.treeView.selectionModel().selectionChanged.connect(self.show_model_tree_details)

        self.setLayout(mainLayout)
        mainLayout.addWidget(self.splitter1)
        self.show()
        self.view_error = self.add_view(ViewError(self.model_tree.root_node_model, self.model_cache))
        self.view_datatype = self.add_view(ViewDataType(self.model_tree.root_node_model))
        self.view_method = self.add_view(ViewMethod(self.model_tree.root_node_model, self.model_cache))
        self.view_event = self.add_view(ViewEvent(self.model_tree.root_node_model, self.model_cache))
        self.view_field = self.add_view(ViewField(self.model_tree.root_node_model, self.model_cache))
        ##self.view_machine = self.add_view(ViewMachine(self.model_tree.model))
        self.view_deployment = self.add_view(ViewDeployment(self.model_tree.root_node_deployment, self.deploy_cache))
        self.view_mode_declaration = self.add_view(ViewModeDeclaration(self.model_tree.root_node_machine, self.cache))
        self.view_ethernet = self.add_view(ViewEthernet(self.model_tree.root_node_ethernet, self.cache))
        self.view_machine = self.add_view(ViewMachine(self.model_tree.root_node_machine, self.cache))

        self.view_executable = self.add_view(ViewExecutable(self.model_tree.root_node_executable, self.cache))
        self.view_process = self.add_view(ViewProcess(self.model_tree.root_node_process, self.cache))
        self.view_startup_config = self.add_view(ViewStartupConfig(self.model_tree.root_node_startup_config, self.cache))
        self.view_application = self.add_view(ViewApplication(self.model_tree.root_node_application, self.cache))
        self.view_adaptive_sw_component = self.add_view(ViewAdaptiveSwComponent(self.model_tree.root_node_adaptive_sw_component, self.cache))


    def get_cache_for(self, name):
        for view in self.views:
            if view.xml_tag_name == name:
                return view.cache
        return None

    def add_view(self, view):
        self.views.append(view)
        return view

                    
    def show_model_tree_details(self, selected, deselected):
        a = self.model_tree.treeView.selectedIndexes()[0]
        xml_node = a.data(Qt.UserRole + 1)
        self.detail.clear()
        if xml_node != None:
            self.show_xml(xml_node)
            for item in self.views:
                if item.show_detail(self.detail.model, xml_node):
                    return
            return
        self.detail.treeView.expandAll()
        self.plaintext_xml.setPlainText('')

    def show_xml(self, node):
        str = node.toprettyxml(indent=' ', newl='')
        self.plaintext_xml.setPlainText(str)


    def parseXML(self, file):
        self.xmldoc = minidom.parse(file)
        for item in self.views:
            item.parse(self.xmldoc, file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())