#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot_tcl.resources.devices.RT2875PJPTCLTVDevice.RT2875PJPTCLTVDeviceAtomModuleBase import RT2875PJPTCLTVDeviceAtomModuleBase


class RT2875PJPTCLTVDeviceWrapModuleBase(RT2875PJPTCLTVDeviceAtomModuleBase):
    """
    TCLTVDevice测试设备资源封装接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(RT2875PJPTCLTVDeviceWrapModuleBase, self).__init__(resource, *args, **kwargs)
