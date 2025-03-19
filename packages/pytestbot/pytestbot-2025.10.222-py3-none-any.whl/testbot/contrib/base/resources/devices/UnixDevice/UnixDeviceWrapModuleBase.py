#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.contrib.base.resources.devices.UnixDevice.UnixDeviceAtomModuleBase import UnixDeviceAtomModuleBase


class UnixDeviceWrapModuleBase(UnixDeviceAtomModuleBase):
    """
    UnixDevice测试设备资源封装接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(UnixDeviceWrapModuleBase, self).__init__(resource, *args, **kwargs)
