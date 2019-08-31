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

class ViewDeploymentMethod(ViewDeploymentBase):
    def __init__(self, view_root_node, cache):
        ViewDeploymentBase.__init__(self, 'SOMEIP-METHOD-DEPLOYMENT', 'Methods', view_root_node, cache)
        pass

    def show_detail_data(self, my_tree, xml_node):
        s = xml_node
        self.add_tv_row_detail(my_tree, [getShortName(s), getValueByNameT(s, 'METHOD-ID'), getValueByNameT(s, 'TRANSPORT-PROTOCOL'), getValueByNameDeepT(s, 'METHOD-REF')], s)
