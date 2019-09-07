#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Stefan Schmidt
import os
import sys
from xml.dom import *
from PyQt5.QtCore import (Qt)

def getXmlContent(node):
    val = None
    if node != None:
        val = node.childNodes[0].nodeValue
    return val

def getValueByNameDeep(node, name):
    val = None
    n = node.getElementsByTagName(name)
    #val = n[0].childNodes[0].nodeValue
    if n != None and len(n) > 0:
        val = getXmlContent(n[0])
    return val

def getValueByNameDeepT(node, name):
    return [getValueByNameDeep(node, name), name]

def getChild(node, name):
    return findFirstChildNodeByName(node, name)

def findFirstChildNodeByName(parent, name):
    for node in parent.childNodes:
        if node.nodeType == Node.ELEMENT_NODE and node.tagName == name:
            return node

def removeAllChildNodesWithName(parent, name):
    for node in parent.childNodes:
        if node.nodeType == Node.ELEMENT_NODE and node.tagName == name:
            parent.removeChild(node)


def getValueByName(parent, name):
    node = findFirstChildNodeByName(parent, name)
    if node:
        return node.childNodes[0].nodeValue
    return None

def getValueByNameT(parent, name):
    return [getValueByName(parent, name), name]    

def getDirectChildNodesByName(parent, name):
    rc = []
    for node in parent.childNodes:
        if node.nodeType == Node.ELEMENT_NODE and node.tagName == name:
            rc.append(node)
    return rc


def getShortName(node):
    val = getValueByName(node, 'SHORT-NAME')
    return val

def getXmlErrorCode(node):
    val = getValueByName(node, 'ERROR-CODE')
    return val

def getCategory(node):
    val = getValueByName(node, 'CATEGORY')
    return val

def getType(node):
    val = getValueByName(node, 'TYPE-TREF')
    return val

def getDirection(node):
    val = getValueByName(node, 'DIRECTION')
    return val

def getFireAndForget(node):
    val = getValueByName(node, 'FIRE-AND-FORGET')
    return val

def getXmlImplementationDataTypeRef(node):
    val = getValueByNameDeep(node, 'IMPLEMENTATION-DATA-TYPE-REF')
    return val

def getXmlBaseTypeRef(node):
    val = getValueByNameDeep(node, 'BASE-TYPE-REF')
    return val

def getXmlArraySize(node):
    val = getValueByName(node, 'ARRAY-SIZE')
    return val

def getXmlArraySizeSemantics(node):
    val = getValueByName(node, 'ARRAY-SIZE-SEMANTICS')
    return val

def getNameSpace2(node):
    nodeName = None
    namespace = ''

    if node.nodeName == 'AR-PACKAGE':
        nodeName = getShortName(node)
    

    if node.parentNode != None:
        namespace = getNameSpace(node.parentNode)

    if nodeName != None:
        if namespace != '':
            namespace = namespace + '/'
        return namespace + nodeName
    else:
        return namespace

def getNameSpaceIntern(node):

    localNameSpace = getShortName(node)
    parentNameSpace = None

    if node.parentNode != None:
        parentNameSpace = getNameSpaceIntern(node.parentNode)

    if (parentNameSpace != None) and (localNameSpace != None):
        return parentNameSpace + '/' + localNameSpace
    elif parentNameSpace != None:
        return parentNameSpace
    elif localNameSpace != None:
        return localNameSpace
    else:
        return None


def getNameSpace(node):
    val = getNameSpaceIntern(node.parentNode)
    return val


def attach_type(item, str):
    item.setData(str, Qt.UserRole + 2)

def attach_xml_node(item, xml_node):
    if xml_node != None:
        item.setData(xml_node, Qt.UserRole + 1)
        pass


def show_node(treeView, node):
    if node:
        proxy = treeView.model()
        model = proxy.sourceModel()    
        node_list = [node]
        while node.parent():
            node = node.parent()
            node_list.insert(0, node)

        for n in node_list:
            k = model.indexFromItem(n)
            index = proxy.mapFromSource(k)
            treeView.setExpanded(index, True)
            
        treeView.scrollTo(index, True)
        treeView.setCurrentIndex(index)

def get_xml_attribute(xml_node, attr_name):
    ret = None
    if xml_node.attributes:
        attr = xml_node.attributes[attr_name]
        if attr:
            ret = attr.firstChild.data;
    return ret

def get_text_from_tvnode(node):
    ret = None
    if node:
        ret = node.data(Qt.DisplayRole)
    return ret

def get_xmlnode_from_tvnode(node):
    ret = None
    if node:
        ret = node.data(Qt.UserRole + 1)
    return ret

def get_selected_tvnode_from_treeview(treeview):
    index = treeview.selectionModel().selectedIndexes()
    return index