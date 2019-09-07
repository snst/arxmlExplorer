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


class ViewEthernet(ViewBase):
    def __init__(self, view_root_node, cache):
        ViewBase.__init__(self, 'ETHERNET-CLUSTER', None, view_root_node, cache)
        self.register_detail_func("NETWORK-ENDPOINT", self.show_detail_network_endpoint)
        self.register_detail_func("VLAN", self.show_detail_vlan)
        pass

    def show_detail_default(self, model, xml_node):
        pass

    def node_added(self, namespace, tv_node, xml_node):
        self.add_subnodes(tv_node, xml_node, 'ETHERNET-PHYSICAL-CHANNEL')
        pass

    def subnode_added(self, tv_node, xml_node, tag_name):
        if tag_name == 'ETHERNET-PHYSICAL-CHANNEL':
            self.add_subnodes(tv_node, xml_node, 'NETWORK-ENDPOINT')
            self.add_subnodes(tv_node, xml_node, 'VLAN')
        pass

    def show_detail_network_endpoint(self, tv_node, xml_node):
        self.add_value(tv_node, xml_node, 'FULLY-QUALIFIED-DOMAIN-NAME')
        itemlist = xml_node.getElementsByTagName('IPV-4-CONFIGURATION')
        for s in itemlist:
            self.add_value(tv_node, s, 'IPV-4-ADDRESS')
            self.add_value(tv_node, s, 'IPV-4-ADDRESS-SOURCE')

    def show_detail_vlan(self, tv_node, xml_node):
        self.add_value(tv_node, xml_node, 'VLAN-IDENTIFIER')
