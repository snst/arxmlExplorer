#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Stefan Schmidt
import os
import sys
from PyQt5.QtGui import QIcon, QStandardItem
from PyQt5.QtCore import *
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
QWidget, QPushButton, QDialog, QPlainTextEdit, QTabWidget)
from xml.dom import minidom

class CustomTreeView( QTreeView ):
    def __init__(self):
        QTreeView.__init__(self)
        self.on_right_click = None
        self.on_left_click = None

    def mousePressEvent(self, event):
        if event.type() == QEvent.MouseButtonPress:
            index = self.selectionModel().selectedIndexes()
            if self.on_right_click and event.button() == Qt.RightButton:
                if index:
                    self.on_right_click(index[0])
                return
            elif self.on_left_click and event.button() == Qt.LeftButton:
                QTreeView.mousePressEvent(self, event)
                index = self.selectionModel().selectedIndexes()
                if index:
                    self.on_left_click(index[0])
                return

        QTreeView.mousePressEvent(self, event)
