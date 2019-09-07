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
from ViewDeploymentBase import *
from ViewDeploymentMethod import *
from ViewDeploymentField import *
from ViewDeploymentEvent import *
from ViewDeploymentEventGroup import *
from NamespaceCache import *


class ViewDeployment(ViewBase):
    def __init__(self, view_root_node, cache):
        ViewBase.__init__(self, 'SOMEIP-SERVICE-INTERFACE-DEPLOYMENT', None, view_root_node, cache)
        self.view_deployment_method = ViewDeploymentMethod(view_root_node, cache)
        self.view_deployment_field = ViewDeploymentField(view_root_node, cache)
        self.view_deployment_event = ViewDeploymentEvent(view_root_node, cache)
        self.view_deployment_event_group = ViewDeploymentEventGroup(view_root_node, cache)
        pass

    def show_detail_default(self, model, xml_node):
        item = self.add_tv_row_detail(model, ['Service Interface Id', getValueByNameT(xml_node, 'SERVICE-INTERFACE-ID')])
        item = self.add_tv_row_detail(model, ['SERVICE-INTERFACE-REF', getValueByNameT(xml_node, 'SERVICE-INTERFACE-REF')])
        version_node = findFirstChildNodeByName(xml_node, 'SERVICE-INTERFACE-VERSION')
        item = self.add_tv_row_detail(model, ['Service Interface Version'])
        self.add_tv_row_detail(item, ['Major', getValueByNameT(version_node, 'MAJOR-VERSION')])
        self.add_tv_row_detail(item, ['Minor', getValueByNameT(version_node, 'MINOR-VERSION')])

    def add_to_treeview(self, parent, xml_node):
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

    def show_detail_default(self, my_tree, xml_node):
        self.tree_view = my_tree.treeView
        self.clear_detail(my_tree)
        self.show_detail_default(my_tree.model, xml_node)
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

        if xml_node.localName != self.xml_tag_name:
            return False
        self.show_detail_default(my_tree, xml_node)
        return True