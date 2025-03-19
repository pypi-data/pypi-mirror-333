#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.contrib.base.resources.devices.Device.DeviceAtomModuleBase import DeviceAtomModuleBase


class WindowsDeviceAtomModuleBase(DeviceAtomModuleBase):
    """
   WindowsDevice设备资源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(WindowsDeviceAtomModuleBase, self).__init__(resource, *args, **kwargs)
