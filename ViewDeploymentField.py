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
from ViewDeploymentBase import *

class ViewDeploymentField(ViewDeploymentBase):
    def __init__(self, xml_name, view_name, view_root_node, cache):
        ViewDeploymentBase.__init__(self, xml_name, view_name, view_root_node, cache)
        pass

    def show_detail_methods(self, my_tree, xml_node):
        s = xml_node
        field = self.add_row_detail2(my_tree, [getShortName(s), '', getValueByNameT(s, 'FIELD-REF')], s)

        node = findFirstChildNodeByName(s, 'GET')
        if node:
            self.add_row_detail2(field, [[getShortName(node), 'GET'], getValueByNameT(node, 'METHOD-ID'), getValueByNameT(node, 'TRANSPORT-PROTOCOL')], node)

        node = findFirstChildNodeByName(s, 'SET')
        if node:
            self.add_row_detail2(field, [[getShortName(node), 'SET'], getValueByNameT(node, 'METHOD-ID'), getValueByNameT(node, 'TRANSPORT-PROTOCOL')], node)

        node = findFirstChildNodeByName(s, 'NOTIFIER')
        if node:
            self.add_row_detail2(field, [[getShortName(node), 'NOTIFIER'], getValueByNameT(node, 'EVENT-ID'), getValueByNameT(node, 'TRANSPORT-PROTOCOL')], node)


