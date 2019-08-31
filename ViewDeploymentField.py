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

class ViewDeploymentField(ViewDeploymentBase):
    def __init__(self, view_root_node, cache):
        ViewDeploymentBase.__init__(self, 'SOMEIP-FIELD-DEPLOYMENT', 'Fields', view_root_node, cache)
        pass

    def show_detail_data(self, my_tree, xml_node):
        s = xml_node
        field = self.add_tv_row_detail(my_tree, [getShortName(s), '', getValueByNameT(s, 'FIELD-REF')], s)

        node = findFirstChildNodeByName(s, 'GET')
        if node:
            self.add_tv_row_detail(field, [[getShortName(node), 'GET'], getValueByNameT(node, 'METHOD-ID'), getValueByNameT(node, 'TRANSPORT-PROTOCOL')], node)

        node = findFirstChildNodeByName(s, 'SET')
        if node:
            self.add_tv_row_detail(field, [[getShortName(node), 'SET'], getValueByNameT(node, 'METHOD-ID'), getValueByNameT(node, 'TRANSPORT-PROTOCOL')], node)

        node = findFirstChildNodeByName(s, 'NOTIFIER')
        if node:
            self.add_tv_row_detail(field, [[getShortName(node), 'NOTIFIER'], getValueByNameT(node, 'EVENT-ID'), getValueByNameT(node, 'TRANSPORT-PROTOCOL')], node)


