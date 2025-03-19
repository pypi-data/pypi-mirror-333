#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot_tcl.resources.devices.MT9653NATCLTVDevice.MT9653NATCLTVDeviceAtomModuleBase import MT9653NATCLTVDeviceAtomModuleBase


class MT9653NATCLTVDeviceWrapModuleBase(MT9653NATCLTVDeviceAtomModuleBase):
    """
    TCLTVDevice测试设备资源封装接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(MT9653NATCLTVDeviceWrapModuleBase, self).__init__(resource, *args, **kwargs)
