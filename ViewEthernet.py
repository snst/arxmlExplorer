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


class ViewEthernet(ViewBase):
    def __init__(self, view_root_node, cache):
        ViewBase.__init__(self, 'ETHERNET-CLUSTER', None, view_root_node, cache)
        pass

    def show_detail_data(self, model, xml_node):
        pass

    def add_to_treeview(self, parent, xml_node):
        name = getShortName(xml_node)
        namespace = getNameSpace(xml_node)
        
        item = self.cache.addViewSubNode(namespace, parent, name)
        attach_xml_node(item, xml_node)
        return item    

    def show_detail_impl(self, my_tree, xml_node):
        self.tree_view = my_tree.treeView
        self.clear_detail(my_tree)
        self.show_detail_data(my_tree.model, xml_node)
        my_tree.treeView.expandAll()
