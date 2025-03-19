#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot_tcl.resources.devices.MT9653JPTCLTVDevice.MT9653JPTCLTVDeviceAtomModuleBase import MT9653JPTCLTVDeviceAtomModuleBase


class MT9653JPTCLTVDeviceWrapModuleBase(MT9653JPTCLTVDeviceAtomModuleBase):
    """
    TCLTVDevice测试设备资源封装接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(MT9653JPTCLTVDeviceWrapModuleBase, self).__init__(resource, *args, **kwargs)
