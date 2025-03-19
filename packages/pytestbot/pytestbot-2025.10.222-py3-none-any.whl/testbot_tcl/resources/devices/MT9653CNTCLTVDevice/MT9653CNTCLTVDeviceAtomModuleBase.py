#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot_tcl.resources.devices.TCLTVDevice.TCLTVDeviceAtomModuleBase import TCLTVDeviceAtomModuleBase


class MT9653CNTCLTVDeviceAtomModuleBase(TCLTVDeviceAtomModuleBase):
    """
   TCLTVDevice设备资源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(MT9653CNTCLTVDeviceAtomModuleBase, self).__init__(resource, *args, **kwargs)
