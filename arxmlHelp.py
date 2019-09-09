#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Stefan Schmidt
import os
import sys


class arxmlHelp():
    def __init__(self):
        self.dict = {}
        self.add('functionGroup', 'Function groups with function group states individually control groups of functionally coherent Application processes. The Process state may depend on a mode that is defined in the function group in case that the StateDependentStartupConfig refers to the function group state with the functionGroupState reference.')
        self.add('initialMode', 'The initial mode of the ModeDeclarationGroup. This mode is active before any mode switches occurred.')
        self.add('ModeDeclarationGroup', 'The "collection of ModeDeclarations" ( = ModeDeclarationGroup) supported by a component')
        self.add('ModeDeclaration', 'The ModeDeclarations collected in this ModeDeclarationGroup.')
        self.add('NetworkEndpoint', 'The network endpoint defines the network addressing (e.g. IP-Address or MAC multicast address).')
        self.add('fullyQualifiedDomainName', 'Defines the fully qualified domain name (FQDN) e.g. some.example.host.')
        self.add('networkEndpointAddress', 'To build a valid network endpoint address there has to be either one MAC multicast group reference or an ipv4 configuration or an ipv6 configuration')
        self.add('ipv4Address','IPv4 Address. Notation: 255.255.255.255. The IP Address shall be declared in case the ipv4Address Source is FIXED and thus no auto-configuration mechanism is used.')
        self.add('ipv4AddressSource','Defines how the node obtains its IP address.')
        self.add('StartupConfigSet','Collection of reusable startup configurations for processes.')
        self.add('StartupOption','This meta-class represents a single startup option consisting of option name and an optional argument.')
        self.add('optionKind','This attribute specifies the style how the command line options appear in the command line.')
        self.add('optionName','This attribute defines option name.')
        self.add('optionArgument','This attribute defines option value.')
        self.add('StartupConfig','This meta-class represents a reusable startup configuration for processes.')
        self.add('Execution Manifest','This kind of Manifest is used to specify the deployment-related information of applications running on the AUTOSAR adaptive platform. An Execution Manifest is bundled with the actual executable code in order to support the integration of the executable code onto the machine.')
        self.add('Machine Manifest','This kind of Manifest is supposed to describe deployment-related content that applies to the configuration of just the underlying machine (i.e. without any applications running on the machine) that runs an AUTOSAR adaptive platform. A Machine Manifest is bundled with the software taken to establish an in-stance of the AUTOSAR adaptive platform.')
        self.add('Service Instance Manifest','This kind of Manifest is used to specify how service-oriented communication is configured in terms of the requirements of the underlying transport protocols. A Service Instance Manifest is bundled with the actual executable code that implements the respective usage of service-oriented communication.')
        self.add('Process','This meta-class provides information required to execute the referenced executable.')
        self.add('ExecutableRef','Reference to executable that is executed in the process.')
        self.add('StartupConfigRef','Reference to a reusable startup configuration with startup parameters.')
        self.add('StateDependentStartupConfig','This meta-class defines the startup configuration for the process depending on a collection of machine states.')
        self.add('ModeDeclarationRef','This represent the applicable functionGroupMode.')
        
        self.add('StateDependentStartupConfig','The purpose of meta-class StateDependentStartupConfig is to \
qualify the startup configuration represented by meta-class StartupConfig for specific ModeDeclarations. \
The ModeDeclarations referenced in the role StateDependentStartupConfig.functionGroupState shall be considered in a \
way such that the StateDependentStartupConfig applies if any of the referenced ModeDeclarations is active.')
        self.add('applicationModeMachine','Set of ApplicationStates (Modes) that are defined for the process.')
        self.add('','')
        self.add('','')
        self.add('','')

    def get(self, item):
        ret = self.dict.get(item)
        return ret

    def add(self, item, info):
        self.dict[item] = info
