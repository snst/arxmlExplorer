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


class ViewApplication(ViewBase):
    def __init__(self, view_root_node, cache):
        ViewBase.__init__(self, 'ADAPTIVE-AUTOSAR-APPLICATION', None, view_root_node, cache)
        pass


    def show_detail_default(self, tv_node, xml_node):
        self.add_value(tv_node, xml_node, 'CATEGORY')

        itemlist = xml_node.getElementsByTagName('EXECUTABLE-REF')
        for s in itemlist:
            self.add_tv_row_detail(tv_node, ['EXECUTABLE-REF', getXmlContent(s)], s)

        # executables refs
        """item = self.add_tv_row_detail(model, ['Executables'])
        #method arguments
        itemlist = xml_node.getElementsByTagName('EXECUTABLE-REF')
        for s in itemlist:
            self.add_tv_row_detail(item, ['EXECUTABLE-REF', getXmlContent(s)], s)"""


    #def node_added(self, namespace, tv_node, xml_node):
    #    self.add_subnodes(tv_node, xml_node, 'EXECUTABLE-REF')
