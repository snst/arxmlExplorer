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
        self.register_detail_func("ROOT-SW-COMPONENT-PROTOTYPE", self.show_detail_root_sw)


    def node_added(self, tv_node, xml_node):
        self.add_subnodes(tv_node, xml_node, 'ROOT-SW-COMPONENT-PROTOTYPE')


    def show_detail_default(self, tree_view, xml_node):
        self.add_value(tree_view, xml_node, 'TRANSFORMATION-PROPS-MAPPING-SET-REF')


    def show_detail_root_sw(self, tree_view, xml_node):
        self.add_value(tree_view, xml_node, 'APPLICATION-TYPE-TREF')
