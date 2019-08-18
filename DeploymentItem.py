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
from BaseItem import *

class DeploymentItem(BaseItem):
    def __init__(self, xml_name, view_name, view_root_node):
        BaseItem.__init__(self, xml_name, view_name, view_root_node)
        pass

    def add(self, parent, xml_node):
        name = getShortName(xml_node)
        item = QStandardItem(name)
        self.node_events = QStandardItem('Events')
        self.node_event_groups = QStandardItem('Event groups')
        self.node_methods =  QStandardItem('Methods')
        self.node_fields =  QStandardItem('Fields')
        
        parent.appendRow([item, QStandardItem(''), QStandardItem(''), QStandardItem('')])
        item.appendRow([self.node_methods, QStandardItem(''), QStandardItem(''), QStandardItem('')])
        item.appendRow([self.node_fields, QStandardItem(''), QStandardItem(''), QStandardItem('')])
        item.appendRow([self.node_events, QStandardItem(''), QStandardItem(''), QStandardItem('')])
        item.appendRow([self.node_event_groups, QStandardItem(''), QStandardItem(''), QStandardItem('')])
        self.attach_xml_node(item, xml_node)
        self.attach_xml_node(self.node_methods, findFirstChildNodeByName(xml_node, 'METHOD-DEPLOYMENTS'))
        self.attach_xml_node(self.node_fields, findFirstChildNodeByName(xml_node, 'FIELD-DEPLOYMENTS'))
        self.attach_xml_node(self.node_events, findFirstChildNodeByName(xml_node, 'EVENT-DEPLOYMENTS'))
        self.attach_xml_node(self.node_event_groups, findFirstChildNodeByName(xml_node, 'EVENT-GROUPS'))
        return item    

    def show_detail_impl(self, my_tree, xml_node):
        self.tree_view = my_tree.treeView
        self.clear_detail(my_tree)
        self.show_detail_data(my_tree.model, xml_node)
        my_tree.treeView.expandAll()

    def show_detail_methods(self, my_tree, xml_node):
        self.clear_detail(my_tree)
        itemlist = xml_node.getElementsByTagName('SOMEIP-METHOD-DEPLOYMENT')
        for s in itemlist:
            self.add_row_detail2(my_tree.model, [getShortName(s), getValueByNameT(s, 'METHOD-ID'), getValueByNameT(s, 'TRANSPORT-PROTOCOL'), getValueByNameDeepT(s, 'METHOD-REF')], s)

    def show_detail_events(self, my_tree, xml_node):
        self.clear_detail(my_tree)
        itemlist = xml_node.getElementsByTagName('SOMEIP-EVENT-DEPLOYMENT')
        for s in itemlist:
            self.add_row_detail2(my_tree.model, [getShortName(s), getValueByNameT(s, 'EVENT-ID'), getValueByNameT(s, 'TRANSPORT-PROTOCOL'), getValueByNameDeepT(s, 'EVENT-REF')], s)

    def show_detail_event_groups(self, my_tree, xml_node):
        self.clear_detail(my_tree)
        itemlist = xml_node.getElementsByTagName('SOMEIP-EVENT-GROUP')
        for eg_xml in itemlist:
            eg_view = self.add_row_detail2(my_tree.model, [getShortName(eg_xml), [getValueByName(eg_xml, 'EVENT-GROUP-ID'), 'EVENT-GROUP-ID']], eg_xml)
            #eg_view.setToolTip('hello')
            eg_list = eg_xml.getElementsByTagName('EVENT-REF')
            for eref_xml in eg_list:
                self.add_row_detail2(eg_view, ['Ref', [getXmlContent(eref_xml), 'EVENT-REF']], eref_xml)
                

    def show_detail_fields(self, my_tree, xml_node):
        self.clear_detail(my_tree)
        itemlist = xml_node.getElementsByTagName('SOMEIP-FIELD-DEPLOYMENT')
        for s in itemlist:
            field = self.add_row_detail2(my_tree.model, [getShortName(s), '', getValueByNameT(s, 'FIELD-REF')], s)

            node = findFirstChildNodeByName(s, 'GET')
            if node:
                self.add_row_detail2(field, [[getShortName(node), 'GET'], getValueByNameT(node, 'METHOD-ID'), getValueByNameT(node, 'TRANSPORT-PROTOCOL')], node)

            node = findFirstChildNodeByName(s, 'SET')
            if node:
                self.add_row_detail2(field, [[getShortName(node), 'SET'], getValueByNameT(node, 'METHOD-ID'), getValueByNameT(node, 'TRANSPORT-PROTOCOL')], node)

            node = findFirstChildNodeByName(s, 'NOTIFIER')
            if node:
                self.add_row_detail2(field, [[getShortName(node), 'NOTIFIER'], getValueByNameT(node, 'EVENT-ID'), getValueByNameT(node, 'TRANSPORT-PROTOCOL')], node)



    def show_detail_data(self, model, xml_node):
        item = self.add_row_detail(model, 'Service Interface Id', getValueByName(xml_node, 'SERVICE-INTERFACE-ID'))
        item = self.add_row_detail(model, 'Service Interface Ref', getValueByName(xml_node, 'SERVICE-INTERFACE-REF'))
        version_node = findFirstChildNodeByName(xml_node, 'SERVICE-INTERFACE-VERSION')
        item = self.add_row_detail(model, 'Service Interface Version', '')
        self.add_row_detail(item, 'Major', getValueByName(version_node, 'MAJOR-VERSION'))
        self.add_row_detail(item, 'Minor', getValueByName(version_node, 'MINOR-VERSION'))

    def clear_detail(self, my_tree):
        my_tree.model = QStandardItemModel(0, 2, None)
        my_tree.model.setHeaderData(0, Qt.Horizontal, 'Name')
        my_tree.model.setHeaderData(1, Qt.Horizontal, 'Value')
        my_tree.treeView.setModel(my_tree.model)
        my_tree.treeView.setColumnWidth(0, 200)
        pass     
