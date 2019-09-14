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
from arxmlHelp import *

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
        self.help = arxmlHelp()
        path = './models/demo7'
        files = [f for f in os.listdir(path) if os.path.isfile(path + '/' + f)]
        for f in files:
            if f.endswith('.arxml'):
                self.parseXML(path + '/' + f)


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.model_tree = ModelTreeView(self)
        self.detail = MethodArgumentsTreeView("Details", self)
        self.errorlist = MethodErrorListWidget()
        self.combo = MethodArgumentEditor()
        #self.tabs = QTabWidget()
        self.plaintext_xml = QPlainTextEdit()
        #self.plaintext_xml.resize(400,150)
        self.plaintext_help = QPlainTextEdit()
        #self.plaintext_help.resize(400,150)
        self.splitter1 = QSplitter(Qt.Vertical)

        self.splitter1.addWidget(self.model_tree.groupDataTypes)
        self.splitter1.addWidget(self.detail.groupDataTypes)

        self.splitter2 = QSplitter(Qt.Horizontal)
        self.splitter2.addWidget(self.plaintext_xml)
        self.splitter2.addWidget(self.plaintext_help)
        self.splitter1.addWidget(self.splitter2)
        self.splitter2.setStretchFactor(0,1)
        self.splitter2.setStretchFactor(1,0)
        #self.splitter2.setSizes([0, 1])

        #self.splitter1.addWidget(self.tabs)

        mainLayout = QVBoxLayout()
        #self.tabs.addTab(self.plaintext_xml,"XML")
        #self.tabs.addTab(self.plaintext_help,"Help")
        #self.tabs.addTab(self.errorlist.groupDataTypes, "Possible Errors")

        self.model_tree.treeView.selectionModel().selectionChanged.connect(self.on_model_tree_selection_changed)
        #self.detail.treeView.selectionModel().selectionChanged.connect(self.on_detail_tree_selection_changed)

        self.setLayout(mainLayout)
        mainLayout.addWidget(self.splitter1)
        self.show()
        """
        self.view_error = self.add_view(ViewError(self.model_tree.root_node_model, self.model_cache))
        self.view_datatype = self.add_view(ViewDataType(self.model_tree.root_node_model))
        self.view_method = self.add_view(ViewMethod(self.model_tree.root_node_model, self.model_cache))
        self.view_event = self.add_view(ViewEvent(self.model_tree.root_node_model, self.model_cache))
        self.view_field = self.add_view(ViewField(self.model_tree.root_node_model, self.model_cache))
        self.view_deployment = self.add_view(ViewDeployment(self.model_tree.root_node_deployment, self.deploy_cache))

        """

        self.view_executable = self.add_view(ViewExecutable(self.model_tree.root_node_application_design, self.cache))
        
        
        self.view_ethernet = self.add_view(ViewEthernet(self.model_tree.root_node_communication_connector, self.cache))
        self.view_machine = self.add_view(ViewMachine(self.model_tree.root_node_machine_manifest, self.cache))

        self.view_adaptive_sw_component = self.add_view(ViewAdaptiveSwComponent(self.model_tree.root_node_application_design, self.cache))
        self.view_application = self.add_view(ViewApplication(self.model_tree.root_node_application_design, self.cache))
        self.view_mode_declaration = self.add_view(ViewModeDeclaration(self.model_tree.root_node_machine_manifest, self.cache))
        self.view_startup_config = self.add_view(ViewStartupConfig(self.model_tree.root_node_startup_config_set, self.cache))
        self.view_process = self.add_view(ViewProcess(self.model_tree.root_node_execution_manifest, self.cache))


    def get_cache_for(self, name):
        for view in self.views:
            if view.xml_tag_name == name:
                return view.cache
        return None

    def add_view(self, view):
        self.views.append(view)
        return view

    def handle_selected_main_item(self, index):
        self.show_help_row(index)

        xml_node = index.data(Qt.UserRole + 1)
        self.show_help(index.data(Qt.DisplayRole))
        self.detail.clear()
        if xml_node != None:
            self.show_xml(xml_node)
            for item in self.views:
                if item.show_detail(self.detail.model, xml_node):
                    self.detail.treeView.expandAll()
                    return
            return
        self.plaintext_xml.setPlainText('')
        pass 
                    
    def on_model_tree_selection_changed(self, selected, deselected):
        a = self.model_tree.treeView.selectedIndexes()[0]
        self.handle_selected_main_item(a)


    def show_xml(self, node):
        str = node.toprettyxml(indent=' ', newl='')
        self.plaintext_xml.setPlainText(str)

    def show_help_row(self, index):
        self.show_help(index.data(RoleHelp))
        self.show_xml(index.data(RoleXmlNode))
        pass

    def show_help(self, item):
        self.set_help_text(self.help.get(item))

    def set_help_text(self, str):
        self.plaintext_help.setPlainText(str)

    def parseXML(self, file):
        self.xmldoc = minidom.parse(file)
        for item in self.views:
            item.parse(self.xmldoc, file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())