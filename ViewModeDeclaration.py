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
        ViewBase.__init__(self, 'MODE-DECLARATION-GROUP', None, view_root_node, cache)
        pass

    def show_detail_data(self, tv_node, xml_node):

        self.add_tv_row_detail(tv_node, ['INITIAL-MODE-REF', getValueByNameT(xml_node,'INITIAL-MODE-REF')], findFirstChildNodeByName(xml_node, 'INITIAL-MODE-REF'))

        # mode refs
        item = self.add_tv_row_detail(tv_node, ['Mode Declarations'])
        #method arguments
        itemlist = xml_node.getElementsByTagName('MODE-DECLARATION')
        for s in itemlist:
            self.show_machine_state(item, s)

    def show_machine_state(self, tv_parent, xml_node):
        self.add_tv_row_detail(tv_parent, [getShortName(xml_node), getValueByNameT(xml_node, 'VALUE')], xml_node)