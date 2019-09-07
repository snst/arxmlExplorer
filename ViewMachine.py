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


class ViewMachine(ViewBase):
    def __init__(self, view_root_node, cache):
        ViewBase.__init__(self, 'MACHINE', 'machine', view_root_node, cache)
        self.register_detail_func("ETHERNET-COMMUNICATION-CONNECTOR", self.show_detail_ethernet_communication_connector)
        self.register_detail_func("MODE-DECLARATION-GROUP-PROTOTYPE", self.show_detail_mode_declaration_group_prototype)
        self.register_detail_func("SERVICE-DISCOVER-CONFIGS", self.show_detail_service_discover_configs)

    def show_detail_ethernet_communication_connector(self, my_tree, xml_node):
        self.add_value(my_tree, xml_node, 'UNICAST-NETWORK-ENDPOINT-REF')

    def show_detail_mode_declaration_group_prototype(self, my_tree, xml_node):
        self.add_value(my_tree, xml_node, 'TYPE-TREF')

    def show_detail_service_discover_configs(self, my_tree, xml_node):
        node = getChild(xml_node, 'SOMEIP-SERVICE-DISCOVERY')
        if node:
            self.add_value(my_tree, node, 'MULTICAST-SD-IP-ADDRESS-REF')
            self.add_value(my_tree, node, 'SOMEIP-SERVICE-DISCOVERY-PORT')

    def node_added(self, tv_node, xml_node):
        self.add_subnodes(tv_node, xml_node, 'ETHERNET-COMMUNICATION-CONNECTOR')
        self.add_subnodes(tv_node, xml_node, 'FUNCTION-GROUPS')
        self.add_subnodes(tv_node, xml_node, 'MACHINE-MODE-MACHINES')
        self.add_subnodes(tv_node, xml_node, 'SERVICE-DISCOVER-CONFIGS')
        pass

    def subnode_added(self, tv_node, xml_node, tag_name):
        if tag_name == 'FUNCTION-GROUPS':
            self.add_subnodes(tv_node, xml_node, 'MODE-DECLARATION-GROUP-PROTOTYPE')
        elif tag_name == 'MACHINE-MODE-MACHINES':
            self.add_subnodes(tv_node, xml_node, 'MODE-DECLARATION-GROUP-PROTOTYPE')
        pass