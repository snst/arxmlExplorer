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


class ViewAdaptiveSwComponent(ViewBase):
    def __init__(self, view_root_node, cache):
        ViewBase.__init__(self, 'ADAPTIVE-APPLICATION-SW-COMPONENT-TYPE', None, view_root_node, cache)
        self.register_detail_func("P-PORT-PROTOTYPE", self.show_detail_p_port)
        self.register_detail_func("R-PORT-PROTOTYPE", self.show_detail_r_port)
        self.view_root_node = self.add_node2(view_root_node, 'AdaptiveApplicationSwComponent')


    def node_added(self, node, xml):
        n = self.add_node2(node, 'ProvidedPorts')
        self.add_subnodes2(n, xml, None, 'P-PORT-PROTOTYPE')
        n = self.add_node2(node, 'RequiredPorts')
        self.add_subnodes2(n, xml, None, 'R-PORT-PROTOTYPE')
        pass


    def show_detail_default(self, node, xml):
        #self.add_value(tree_view, xml, 'TRANSFORMATION-PROPS-MAPPING-SET-REF')
        pass


    def show_detail_p_port(self, node, xml):
        self.add_value(node, xml, 'PROVIDED-INTERFACE-TREF')


    def show_detail_r_port(self, node, xml):
        self.add_value(node, xml, 'REQUIRED-INTERFACE-TREF')
