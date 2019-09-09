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
from NamespaceCache import *
from arxmlHelper import *

class ViewBase():
    def __init__(self, xml_tag_name, node_name, view_root_node, cache = None):
        if cache:
            self.cache = cache
        else:
            self.cache = NamespaceCache()
        self.xml_tag_name = xml_tag_name
        self.node_name = node_name
        self.view_root_node = view_root_node
        self.detail_funcs = { self.xml_tag_name: self.show_detail_default }

    def register_detail_func(self, tag, func):
        self.detail_funcs[tag] = func

    def show_detail_default(self, tree_view, xml_node):
        pass


    def parse(self, xml_node, filename):
        itemlist = xml_node.getElementsByTagName(self.xml_tag_name)
        for s in itemlist:
            namespace = getNameSpace(s)
            name = getShortName(s)
            node_name = s.localName
            node = self.add_row(self.view_root_node, [[self.node_name, s.localName], name, namespace, filename], s)
            #node = QStandardItem(node_name)
            #self.view_root_node.appendRow([node, QStandardItem(name), QStandardItem(namespace), QStandardItem(filename)])
            self.cache.add(self.xml_tag_name, [namespace, name], node)
            #attach_xml_node(node, s)
            self.node_added(node, s)


    def get_tv_node_with_namespace(self, namespace):
        tv_node = self.cache.get(self.xml_tag_name, namespace)
        if not tv_node:
            tv_node = self.add_tv_namespace_node(self.view_root_node, namespace, None)
            self.cache.add(self.xml_tag_name, namespace, tv_node)

        """if self.view_name:
            node = self.cache.getViewSubNode(namespace, self.view_name)
            if not node:
                node = self.cache.addViewSubNode(namespace, tv_node, self.view_name)
            return node
        else:            """
        return tv_node


    def node_added(self, tv_node, xml_node):
        pass


    def add_tv_namespace_node(self, parent, namespace, xml_node):
        item = QStandardItem(namespace)
        parent.appendRow([item, QStandardItem('ns'), QStandardItem(''), QStandardItem('')])
        attach_xml_node(item, xml_node)
        attach_type(item, 'NS')
        return item


    """def show_detail(self, tree_view, xml_node):
        if xml_node.localName != self.xml_tag_name:
            return False
        self.add_short_name(tree_view, xml_node)
        self.show_detail_default(tree_view, xml_node)
        return True"""

    def show_detail(self, tv_node, xml_node):
        func = self.detail_funcs.get(xml_node.localName)
        if func:
            self.add_short_name(tv_node, xml_node)
            func(tv_node, xml_node)
            return True
        return False



    """def show_detail_default(self, my_tree, xml_node):
        #self.clear_detail(my_tree)
        self.add_value(my_tree.model, xml_node, 'SHORT-NAME')
        self.show_detail_data(my_tree.model, xml_node)
        #my_tree.treeView.expandAll()"""


    def clear_detail(self, my_tree):
        my_tree.model = QStandardItemModel(0, 2, None)
        my_tree.model.setHeaderData(0, Qt.Horizontal, 'Name')
        my_tree.model.setHeaderData(1, Qt.Horizontal, 'Value')
        my_tree.treeView.setModel(my_tree.model)
        my_tree.treeView.setColumnWidth(0, 200)
        pass   

    def show_detail_data(self, tree, node):
        pass
        
    def add_row(self, parent, arg_list, xml_node = None):
        return self.add_tv_row_detail(parent, arg_list, xml_node)

    def add_tv_row_detail(self, parent, arg_list, xml_node = None):
        row = []
        first_item = None
        item = None
        for arg in arg_list:
            if type(arg) == list:
                item = QStandardItem(arg[0])
                item.setToolTip(arg[1])
            else:
                item = QStandardItem(arg)
            if not first_item:
                first_item = item
            row.append(item)
        parent.appendRow(row)
        attach_xml_node(first_item, xml_node)
        return first_item


    def add_to_treeview(self, parent, xml_node, filename=''):
        name = getShortName(xml_node)
        namespace = getNameSpace(xml_node)

        node = QStandardItem(xml_node.localName)
        parent.appendRow([node, QStandardItem(name), QStandardItem(filename)])
        self.cache.add(self.xml_tag_name, [namespace, name], node)
        attach_xml_node(node, xml_node)
        return node    


    def add_subnodes(self, tv_parent, xml_parent, tag_name, shown_name = None):
        itemlist = xml_parent.getElementsByTagName(tag_name)
        for s in itemlist:
            namespace = getNameSpace(s)
            name = getShortName(s)
            shown_name_space = namespace
            if not shown_name:
                shown_name = tag_name
            node = self.add_tv_row_detail(tv_parent, [[shown_name, tag_name], name, namespace], s)
            self.cache.add(tag_name, [namespace, getShortName(s)], node)   
            self.subnode_added(node, s, tag_name)

    def subnode_added(self, tv_node, xml_node, tag_name):
        pass

    def add_value(self, model, xml_node, xml_tag_name, shown_name = None):
        value = getValueByName(xml_node, xml_tag_name)
        node = findFirstChildNodeByName(xml_node, xml_tag_name)
        if not shown_name:
            shown_name = xml_tag_name
        self.add_tv_row_detail(model, [[shown_name, xml_tag_name], value], node)            

    def add_short_name(self, model, xml_node):
        self.add_value(model, xml_node, 'SHORT-NAME', 'name')