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

class ViewDeploymentEventGroup(ViewDeploymentBase):
    def __init__(self, view_root_node, cache):
        ViewDeploymentBase.__init__(self, 'SOMEIP-EVENT-GROUP', 'Event Groups', view_root_node, cache)
        pass

    def show_detail_methods(self, my_tree, xml_node):
        s = xml_node
        eg_view = self.add_row_detail2(my_tree, [getShortName(s), [getValueByName(s, 'EVENT-GROUP-ID'), 'EVENT-GROUP-ID']], s)
        eg_list = s.getElementsByTagName('EVENT-REF')
        for eref_xml in eg_list:
                self.add_row_detail2(eg_view, ['Ref', [getXmlContent(eref_xml), 'EVENT-REF']], eref_xml)
