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
from MethodArgumentEditor import *
from ModelTreeView import *
from MethodArgumentsTreeView import *
from arxmlHelper import *
from MethodErrorListWidget import *

def showdialog():
    #demo = MethodArgumentEditor()
    #demo.exec_()
    pass



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

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.model_tree.groupDataTypes)
        mainLayout.addWidget(self.detail.groupDataTypes)
        mainLayout.addWidget(self.tabs)

        self.tabs.addTab(self.combo,"Details")
        self.tabs.addTab(self.plaintext_xml,"XML")
        self.tabs.addTab(self.errorlist.groupDataTypes, "Possible Errors")

        #b = QPushButton()
        #b.setText("Hello World!")
        #mainLayout.addWidget(b)
        #b.clicked.connect(showdialog)

        self.model_tree.treeView.selectionModel().selectionChanged.connect(self.show_model_tree_details)
        self.detail.treeView.selectionModel().selectionChanged.connect(self.show_method_parameter_details)



        #mainLayout.addWidget(self.viewInterfaces.groupDataTypes)
        #mainLayout.addWidget(self.viewEvents.groupDataTypes)
        self.setLayout(mainLayout)
        self.show()

    def show_method_details(self, node):
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

    def show_datatype_details(self, node):
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
                self.show_method_details(b)
            elif b.localName == 'IMPLEMENTATION-DATA-TYPE':
                self.show_datatype_details(b)
    
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
        itemlist = self.xmldoc.getElementsByTagName('IMPLEMENTATION-DATA-TYPE')
        for s in itemlist:
            self.model_tree.add(self.model_tree.node_datatypes, getShortName(s), getCategory(s), file, getNameSpace(s), s)

        itemlist = self.xmldoc.getElementsByTagName('APPLICATION-ERROR')
        for s in itemlist:
            self.model_tree.add(self.model_tree.node_application_errors, getShortName(s), getXmlErrorCode(s), file, getNameSpace(s), s)
    
        itemlist = self.xmldoc.getElementsByTagName('SOMEIP-SERVICE-INTERFACE-DEPLOYMENT')
        for s in itemlist:
            self.model_tree.add(self.model_tree.node_deployment, getShortName(s), '', file, getNameSpace(s), s)
    
        itemlist = self.xmldoc.getElementsByTagName('MACHINE')
        for s in itemlist:
            self.model_tree.add(self.model_tree.node_machine, getShortName(s), '', file, getNameSpace(s), s)
    


#        itemlist = self.xmldoc.getElementsByTagName('CLIENT-SERVER-OPERATION')
#        for s in itemlist:
#            self.model_tree.add(self.model_tree.node_operations, getShortName(s), "", file, getNameSpace(s))

#        itemlist = self.xmldoc.getElementsByTagName('VARIABLE-DATA-PROTOTYPE')
#        for s in itemlist:
#            self.model_tree.add(self.model_tree.node_events, getShortName(s), 'VARIABLE-DATA-PROTOTYPE', file, getNameSpace(s))

        service_interface_list = self.xmldoc.getElementsByTagName('SERVICE-INTERFACE')
        for service_interface in service_interface_list:
            service_interface_node = self.model_tree.add(self.model_tree.node_interfaces, getShortName(service_interface), 'SERVICE-INTERFACE', file, getNameSpace(service_interface), service_interface)
            # add methods
            methods_node = self.model_tree.add(service_interface_node, 'METHODS', '', '', '')
            method_list = service_interface.getElementsByTagName('CLIENT-SERVER-OPERATION')
            for method in method_list:
                self.model_tree.add(methods_node, getShortName(method), "CLIENT-SERVER-OPERATION", file, getNameSpace(method), method)
            # add events
            events_node = self.model_tree.add(service_interface_node, 'EVENTS', '', '', '')
            event_list = self.xmldoc.getElementsByTagName('VARIABLE-DATA-PROTOTYPE')
            for event in event_list:
                self.model_tree.add(events_node, getShortName(event), 'VARIABLE-DATA-PROTOTYPE', file, getNameSpace(event), event)
            # add fields
            field_node = self.model_tree.add(service_interface_node, 'FIELDS', '', '', '')
            field_list = self.xmldoc.getElementsByTagName('FIELD')
            for field in field_list:
                self.model_tree.add(field_node, getShortName(field), 'FIELD', file, getNameSpace(field), field)
               
                


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())