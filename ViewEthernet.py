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
        ViewBase.__init__(self, 'ETHERNET-CLUSTER', 'EthernetCluster', view_root_node, cache)
        self.register_detail_func("NETWORK-ENDPOINT", self.show_detail_network_endpoint)
        self.register_detail_func("VLAN", self.show_detail_vlan)
        pass

    def show_detail_default(self, model, xml_node):
        pass

    def node_added(self, tv_node, xml_node):
        self.add_subnodes(tv_node, xml_node, 'ETHERNET-PHYSICAL-CHANNEL', 'EthernetPhysicalChannel')
        pass

    def subnode_added(self, tv_node, xml_node, tag_name):
        if tag_name == 'ETHERNET-PHYSICAL-CHANNEL':
            self.add_subnodes(tv_node, xml_node, 'NETWORK-ENDPOINT', 'NetworkEndpoint')
            self.add_subnodes(tv_node, xml_node, 'VLAN', 'VlanConfig')
        pass

    def show_detail_network_endpoint(self, tv_node, xml_node):
        self.add_value(tv_node, xml_node, 'FULLY-QUALIFIED-DOMAIN-NAME', 'fullyQualifiedDomainName')
        itemlist = xml_node.getElementsByTagName('IPV-4-CONFIGURATION')
        for s in itemlist:
            n = self.add_row(tv_node, [['Ipv4Configuration', 'IPV-4-CONFIGURATION']], s)
            self.add_value(n, s, 'IPV-4-ADDRESS', 'ipv4Address')
            self.add_value(n, s, 'IPV-4-ADDRESS-SOURCE', 'ipv4AddressSource')

    def show_detail_vlan(self, tv_node, xml_node):
        self.add_value(tv_node, xml_node, 'VLAN-IDENTIFIER')
