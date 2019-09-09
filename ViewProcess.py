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


class ViewProcess(ViewBase):
    def __init__(self, view_root_node, cache):
        ViewBase.__init__(self, 'PROCESS', None, view_root_node, cache)
        self.register_detail_func("APPLICATION-MODE-MACHINE", self.show_detail_app_mode_machine)
        self.register_detail_func("FUNCTION-GROUP-IREF", self.show_detail_mode_ref)
        self.register_detail_func("MACHINE-MODE-IREF", self.show_detail_mode_ref)
        self.register_detail_func("MODE-DEPENDENT-STARTUP-CONFIG", self.show_detail_mode_dependent_startup_config)

    def show_detail_default(self, tv_node, xml_node):
        self.add_value(tv_node, xml_node, 'EXECUTABLE-REF')
        #self.add_subnodes(tv_node, xml_node, 'APPLICATION-MODE-MACHINE')
        #self.add_subnodes(tv_node, xml_node, 'MODE-DEPENDENT-STARTUP-CONFIG')

    def show_detail_mode_ref(self, tv_node, xml_node):
        self.add_value(tv_node, xml_node, 'CONTEXT-MODE-DECLARATION-GROUP-PROTOTYPE-REF')
        self.add_value(tv_node, xml_node, 'TARGET-MODE-DECLARATION-REF')

    def show_detail_mode_dependent_startup_config(self, tv_node, xml_node):
        self.add_value(tv_node, xml_node, 'STARTUP-CONFIG-REF')

    def node_added(self, tv_node, xml_node):
        self.add_subnodes(tv_node, xml_node, 'APPLICATION-MODE-MACHINE')
        self.add_subnodes(tv_node, xml_node, 'MODE-DEPENDENT-STARTUP-CONFIG')
        pass

    def subnode_added(self, tv_node, xml_node, tag_name):
        if tag_name == 'MODE-DEPENDENT-STARTUP-CONFIG':
            self.add_subnodes(tv_node, xml_node, 'FUNCTION-GROUP-IREF')
            self.add_subnodes(tv_node, xml_node, 'MACHINE-MODE-IREF')
        pass

    def show_detail_app_mode_machine(self, my_tree, xml_node):
        self.add_value(my_tree, xml_node, 'TYPE-TREF')
