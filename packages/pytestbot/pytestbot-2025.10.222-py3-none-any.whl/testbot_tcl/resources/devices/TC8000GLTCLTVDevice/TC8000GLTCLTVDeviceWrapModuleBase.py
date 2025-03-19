#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot_tcl.resources.devices.TC8000GLTCLTVDevice.TC8000GLTCLTVDeviceAtomModuleBase import TC8000GLTCLTVDeviceAtomModuleBase


class TC8000GLTCLTVDeviceWrapModuleBase(TC8000GLTCLTVDeviceAtomModuleBase):
    """
    TCLTVDevice测试设备资源封装接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(TC8000GLTCLTVDeviceWrapModuleBase, self).__init__(resource, *args, **kwargs)
