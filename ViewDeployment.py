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
from ViewDeploymentBase import *
from ViewDeploymentMethod import *
from ViewDeploymentField import *
from ViewDeploymentEvent import *
from ViewDeploymentEventGroup import *
from NamespaceCache import *


class ViewDeployment(BaseItem):
    def __init__(self, xml_name, view_name, view_root_node, cache):
        BaseItem.__init__(self, xml_name, view_name, view_root_node, cache)
        self.view_deployment_method = ViewDeploymentMethod('SOMEIP-METHOD-DEPLOYMENT', 'Methods', view_root_node, cache)
        self.view_deployment_field = ViewDeploymentField('SOMEIP-FIELD-DEPLOYMENT', 'Fields', view_root_node, cache)
        self.view_deployment_event = ViewDeploymentEvent('SOMEIP-EVENT-DEPLOYMENT', 'Events', view_root_node, cache)
        self.view_deployment_event_group = ViewDeploymentEventGroup('SOMEIP-EVENT-GROUP', 'Event Groups', view_root_node, cache)
        pass

    def show_detail_methods(self, model, xml_node):
        item = self.add_row_detail(model, 'Service Interface Id', getValueByName(xml_node, 'SERVICE-INTERFACE-ID'))
        item = self.add_row_detail(model, 'Service Interface Ref', getValueByName(xml_node, 'SERVICE-INTERFACE-REF'))
        version_node = findFirstChildNodeByName(xml_node, 'SERVICE-INTERFACE-VERSION')
        item = self.add_row_detail(model, 'Service Interface Version', '')
        self.add_row_detail(item, 'Major', getValueByName(version_node, 'MAJOR-VERSION'))
        self.add_row_detail(item, 'Minor', getValueByName(version_node, 'MINOR-VERSION'))

    def add(self, parent, xml_node):
        name = getShortName(xml_node)
        #item = QStandardItem(name)
        namespace = getNameSpace(xml_node)
        
        item = self.cache.addViewSubNode(namespace, parent, name)
        attach_xml_node(item, xml_node)

        self.view_deployment_field.parse2(xml_node, item)
        self.view_deployment_method.parse2(xml_node, item)
        self.view_deployment_event.parse2(xml_node, item)
        self.view_deployment_event_group.parse2(xml_node, item)

        return item    

    def show_detail_impl(self, my_tree, xml_node):
        self.tree_view = my_tree.treeView
        self.clear_detail(my_tree)
        self.show_detail_methods(my_tree.model, xml_node)
        my_tree.treeView.expandAll()

    def clear_detail(self, my_tree):
        my_tree.model = QStandardItemModel(0, 2, None)
        my_tree.model.setHeaderData(0, Qt.Horizontal, 'Name')
        my_tree.model.setHeaderData(1, Qt.Horizontal, 'Value')
        my_tree.treeView.setModel(my_tree.model)
        my_tree.treeView.setColumnWidth(0, 200)
        pass     

    def show_detail(self, my_tree, xml_node):
        if self.view_deployment_field.show_detail(my_tree, xml_node):
            return True
        if self.view_deployment_event.show_detail(my_tree, xml_node):
            return True
        if self.view_deployment_event_group.show_detail(my_tree, xml_node):
            return True
        if self.view_deployment_method.show_detail(my_tree, xml_node):
            return True

        if xml_node.localName != self.xml_name:
            return False
        self.show_detail_impl(my_tree, xml_node)
        return True