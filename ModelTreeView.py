#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Stefan Schmidt
import os
import sys
from PyQt5.QtGui import QIcon, QStandardItem, QFontMetrics
from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
QTime, pyqtSlot, QObject, pyqtSignal)
from PyQt5.QtGui import QStandardItemModel, QBrush, QColor
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout, QStyledItemDelegate,
QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout, QTreeWidgetItem, QSpinBox, QStyle, 
QWidget, QPushButton, QDialog, QPlainTextEdit, QTabWidget)
from xml.dom import minidom
from CustomTreeView import *

class ViewDelegate(QStyledItemDelegate):
    def __init__(self):
        QStyledItemDelegate.__init__(self) 
        self.padding = 2
        self.AlignmentFlag =  Qt.AlignLeft

    def paint3(self, painter, option, index):
        super(ViewDelegate, self).paint(painter, option, index)

    def paint(self, painter, option, index):
        x = option.rect.x()
        y = option.rect.y()
        width = option.rect.width()
        height = option.rect.height()
        #iconList = index.data(256)                      # get the icons associated with the item
        text = index.data()                             # get the items text
        """
        for a, i in enumerate(iconList):
            m = max([i.width(), i.height()]) 
            f = (height- 2*self.padding)/m                  # scalingfactor
            i = i.scaled(int(i.width()*f),int(i.height()*f))                    # scale all pixmaps to the same size depending on lineheight
            painter.drawPixmap(QPoint(x,y+self.padding),i)
            x += height
        """


        if option.state & QStyle.State_Selected:
            option.backgroundBrush = QBrush(QColor(100, 200, 100, 200))
            #painter.fillRect(option.rect, painter.brush())
            painter.fillRect(option.rect, option.backgroundBrush)
        font = painter.font()
        fm = QFontMetrics(font);
        w = fm.width(text)
        painter.drawText(QRect(x + self.padding,y + self.padding, width - x - 2*self.padding, height - 2*self.padding),self.AlignmentFlag, text)

        font.setItalic(True);   
        painter.setFont(font);  

        painter.drawText(QRect(w+x + self.padding,y + self.padding, width - x - 2*self.padding, height - 2*self.padding),self.AlignmentFlag, text)
        font.setItalic(False);   
        painter.setFont(font);  


class MyFilter(QSortFilterProxyModel):
    def __init__(self):
        QSortFilterProxyModel.__init__(self)
        self.str_filter = ''
        pass

    def filterAcceptsRow (self, source_row, source_parent):
        index0 = self.sourceModel().index(source_row, 0, source_parent);
        str = self.sourceModel().data(index0)
        ns = index0.data(Qt.UserRole + 2)
        arg_node = source_parent.data(Qt.UserRole + 1)
        c = True
        if not self.str_filter=='' and ns == 'NS':
            if not self.str_filter in str:
                c = False
        #a = self.sourceModel()
        return c

class ModelTreeView():
    def __init__(self, main):
        self.main = main
        self.groupDataTypes = QGroupBox('Model')
        self.textbox_filter = QLineEdit()
        self.textbox_filter.returnPressed.connect(self.on_filter_updated)
        self.treeView = CustomTreeView()
        #self.treeView.setRootIsDecorated(False)
        self.treeView.setAlternatingRowColors(True)
        dataLayout = QVBoxLayout()
        dataLayout.addWidget(self.textbox_filter)
        dataLayout.addWidget(self.treeView)
        self.groupDataTypes.setLayout(dataLayout)

        self.model = self.createModelDataTypes(self)
        self.proxyModel = MyFilter()
        self.proxyModel.setDynamicSortFilter(True)
        self.proxyModel.setSourceModel(self.model)

        self.delegate = ViewDelegate()
        self.treeView.setItemDelegateForColumn(0, self.delegate)

        self.treeView.setModel(self.proxyModel)
        self.treeView.setColumnWidth(0, 350)
        self.treeView.setColumnWidth(1, 200)
        self.treeView.setColumnWidth(2, 250)

        #self.treeView.on_left_click = self.main.on_tree_selection_changed


        self.root_node_model = self.add_main_node('Model')
        self.root_node_deployment = self.add_main_node('Deployment')
        self.root_node_machine_manifest = self.add_main_node('Machine Manifest')
        self.root_node_application_design = self.add_main_node('Application Design')
        self.root_node_application_manifest = self.add_main_node('Application Manifest')
        self.root_node_execution_manifest = self.add_main_node('Execution Manifest')
        self.root_node_function_groups = self.add_node(self.root_node_machine_manifest, 'functionGroup')
        self.root_node_communication_connector = self.add_node(self.root_node_machine_manifest, 'CommunicationConnector')
        self.root_node_service_discover_config = self.add_node(self.root_node_machine_manifest, 'serviceDiscoverConfig')

        #self.root_node_model.appendRow(a)

        pass

    def add_node(self, parent, name):
        node = QStandardItem(name)
        parent.appendRow(node)
        return node

    def add_main_node(self, name):
        node = self.add_node(self.model, name)
        return node


    def on_filter_updated(self):
        str = self.textbox_filter.text()
        self.update_filter(str)

    def update_filter(self, str_filter):
        self.proxyModel.str_filter = str_filter
        self.proxyModel.invalidateFilter()

    def createModelDataTypes(self,parent):
        model = QStandardItemModel(0, 4, None)
        model.setHeaderData(0, Qt.Horizontal, "Name")
        model.setHeaderData(1, Qt.Horizontal, "Value")
        model.setHeaderData(2, Qt.Horizontal, "")
        model.setHeaderData(3, Qt.Horizontal, "Source")
        return model
    
    def add(self, parent, name, category, source, namespace='', xml_node = None):
        item = QStandardItem(name)
        parent.appendRow([item, QStandardItem(category), QStandardItem(namespace), QStandardItem(source)])
        attach_xml_node(item, xml_node)
        return item

    def get_application_error_value(self, name):

        child_count = self.node_application_errors.rowCount()
        n = self.node_application_errors
        for i in range(child_count):
            #l = self.node_application_errors.takeRow(i)
            err = n.child(i,2).data(Qt.DisplayRole) + "/" + n.child(i,0).data(Qt.DisplayRole)
            err_no = n.child(i,1).data(Qt.DisplayRole)
            #err = "/" + err.replace('/', "/")
            if name == err:
                #print(err)
                #print(err_no)
                return err_no

        return 'not found'
        """child_count = node.childCount()
        for i in range(child_count):
            item = node.child(i)
            print(item.text(0) + item.text(1))"""
