#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot_tcl.resources.devices.TC8000CNTCLTVDevice.TC8000CNTCLTVDeviceAtomModuleBase import TC8000CNTCLTVDeviceAtomModuleBase


class TC8000CNTCLTVDeviceWrapModuleBase(TC8000CNTCLTVDeviceAtomModuleBase):
    """
    TCLTVDevice测试设备资源封装接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(TC8000CNTCLTVDeviceWrapModuleBase, self).__init__(resource, *args, **kwargs)
