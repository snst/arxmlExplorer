#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Stefan Schmidt
import os
import sys
from xml.dom import *

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

def getDirectChildNodesByName(parent, name):
    rc = []
    for node in parent.childNodes:
        if node.nodeType == Node.ELEMENT_NODE and node.tagName == name:
            rc.append(node)
    return rc


def getShortName(node):
    return getValueByName(node, 'SHORT-NAME')

def getXmlErrorCode(node):
    return getValueByName(node, 'ERROR-CODE')

def getCategory(node):
    return getValueByName(node, 'CATEGORY')

def getType(node):
    return getValueByName(node, 'TYPE-TREF')

def getDirection(node):
    return getValueByName(node, 'DIRECTION')

def getXmlImplementationDataTypeRef(node):
    return getValueByNameDeep(node, 'IMPLEMENTATION-DATA-TYPE-REF')

def getXmlBaseTypeRef(node):
    return getValueByNameDeep(node, 'BASE-TYPE-REF')

def getXmlArraySize(node):
    return getValueByName(node, 'ARRAY-SIZE')

def getXmlArraySizeSemantics(node):
    return getValueByName(node, 'ARRAY-SIZE-SEMANTICS')

def getNameSpace2(node):
    nodeName = None
    namespace = ''

    if node.nodeName == 'AR-PACKAGE':
        nodeName = getShortName(node)
    

    if node.parentNode != None:
        namespace = getNameSpace(node.parentNode)

    if nodeName != None:
        if namespace != '':
            namespace = namespace + '::'
        return namespace + nodeName
    else:
        return namespace

def getNameSpaceIntern(node):

    localNameSpace = getShortName(node)
    parentNameSpace = None

    if node.parentNode != None:
        parentNameSpace = getNameSpaceIntern(node.parentNode)

    if (parentNameSpace != None) and (localNameSpace != None):
        return parentNameSpace + "::" + localNameSpace
    elif parentNameSpace != None:
        return parentNameSpace
    elif localNameSpace != None:
        return localNameSpace
    else:
        return None


def getNameSpace(node):
    return getNameSpaceIntern(node.parentNode)

    