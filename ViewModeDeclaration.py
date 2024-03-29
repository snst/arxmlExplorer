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


class ViewModeDeclaration(ViewBase):
    def __init__(self, view_root_node, cache):
        ViewBase.__init__(self, 'MODE-DECLARATION-GROUP', 'ModeDeclarationGroup', view_root_node, cache)
        self.view_root_node = self.add_node2(self.view_root_node, 'functionGroup')
        self.register_detail_func("MODE-DECLARATION", self.show_detail_mode_declaration)


    def node_added(self, node, xml):
        self.add_subnodes2(node, xml, None, 'MODE-DECLARATION')

 
    def show_detail_default(self, node, xml):
        self.add_value(node, xml, 'INITIAL-MODE-REF', 'initialMode')


    def show_detail_mode_declaration(self, node, xml):
        self.add_value(node, xml, 'VALUE', 'Value')
