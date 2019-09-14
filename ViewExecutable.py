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


class ViewExecutable(ViewBase):
    def __init__(self, view_root_node, cache):
        ViewBase.__init__(self, 'EXECUTABLE', None, view_root_node, cache)
        #self.register_detail_func("ROOT-SW-COMPONENT-PROTOTYPE", self.show_detail_root_sw)
        self.view_root_node = self.add_node2(view_root_node, 'Executables')


    #def node_added(self, node, xml):
        #self.add_subnodes(node, xml, 'ROOT-SW-COMPONENT-PROTOTYPE')
        #self.add_subnodes2(node, xml, None, 'ROOT-SW-COMPONENT-PROTOTYPE')


    def show_detail_default(self, node, xml):
        self.add_value(node, xml, 'TRANSFORMATION-PROPS-MAPPING-SET-REF')
        
        xml_child = getChild(xml, 'ROOT-SW-COMPONENT-PROTOTYPE')
        subnode = self.add_node2(node, 'RootSwComponent', xml_node=xml_child)
        if xml_child:
            self.add_short_name(subnode, xml_child)
            self.add_value(subnode, xml_child, 'APPLICATION-TYPE-TREF', 'ApplicationTypeRef')


    #def show_detail_root_sw(self, node, xml):
    #    self.add_value(node, xml, 'APPLICATION-TYPE-TREF')
