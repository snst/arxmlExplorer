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


class ViewStartupConfig(ViewBase):
    def __init__(self, view_root_node, cache):
        ViewBase.__init__(self, 'STARTUP-CONFIG-SET', 'StartupConfigSet', view_root_node, cache)
        self.register_detail_func("STARTUP-CONFIG", self.show_detail_startup_config)

    def node_added(self, tv_node, xml_node):
        self.add_subnodes(tv_node, xml_node, 'STARTUP-CONFIG', 'StartupConfig')


    def show_detail_startup_config(self, tv_node, xml_node):
        self.add_value(tv_node, xml_node, 'SCHEDULING-POLICY', 'schedulingPolicy')
        self.add_value(tv_node, xml_node, 'SCHEDULING-PRIORITY', 'schedulingPriority')

        itemlist = xml_node.getElementsByTagName('STARTUP-OPTION')
        for s in itemlist:
            n = self.add_row(tv_node, [['StartupOption', 'STARTUP-OPTION']], s)
            self.add_value(n, s, 'OPTION-ARGUMENT', 'optionArgument')
            self.add_value(n, s, 'OPTION-KIND', 'optionKind')
            self.add_value(n, s, 'OPTION-NAME', 'optionName')


    def show_detail_default(self, tree_view, xml_node):
        pass
