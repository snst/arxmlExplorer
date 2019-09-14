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
        ViewBase.__init__(self, 'PROCESS', 'Process', view_root_node, cache)
        self.view_root_node = self.add_node2(self.view_root_node, 'Process')

    def FunctionGroupMode_added(self, node, xml):
        self.add_value(node, xml, 'CONTEXT-MODE-DECLARATION-GROUP-PROTOTYPE-REF', 'ModeRef')
        self.add_value(node, xml, 'TARGET-MODE-DECLARATION-REF', 'TargetRef')
        pass

    def MachineMode_added(self, node, xml):
        self.add_value(node, xml, 'CONTEXT-MODE-DECLARATION-GROUP-PROTOTYPE-REF', 'ModeRef')
        self.add_value(node, xml, 'TARGET-MODE-DECLARATION-REF', 'TargetRef')
        pass

    def ModeDependentStartupConfig_added(self, node, xml):
        self.add_value(node, xml, 'STARTUP-CONFIG-REF', 'StartupConfigRef', h='process_startupConfig')
        self.add_subnodes2(node, xml, 'FunctionGroupMode', 'FUNCTION-GROUP-IREF', self.FunctionGroupMode_added, h='process_functionGroupMode')
        self.add_subnodes2(node, xml, 'MachineMode', 'MACHINE-MODE-IREF', self.MachineMode_added, h='process_machineMode')
        pass

    def show_detail_default(self, tv_node, xml_node):
        xml_child = getChild(xml_node, 'APPLICATION-MODE-MACHINE')
        subnode = self.add_node2(tv_node, 'ApplicationModeMachine', xml_node=xml_child, h='process_applicationModeMachine')
        if xml_child:
            self.add_short_name(subnode, xml_child)
            self.add_value(subnode, xml_child, 'TYPE-TREF', 'ModeRef')
            #self.add_value(subnode, xml_child, 'TYPE-TREF', getShortName(xml_child), italic=True)

        self.add_value(tv_node, xml_node, 'EXECUTABLE-REF', 'ExecutableRef', h='process_executableRef')

        xml_child = getChild(xml_node, 'MODE-DEPENDENT-STARTUP-CONFIGS')
        subnode = self.add_node2(tv_node, 'ModeDependentStartupConfigs', xml_node=xml_child, h=None)
        self.add_subnodes2(subnode, xml_child, 'ModeDependentStartupConfig', 'MODE-DEPENDENT-STARTUP-CONFIG', self.ModeDependentStartupConfig_added, h='process_modeDependentStartupConfig')


