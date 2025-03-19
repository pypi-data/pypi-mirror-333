#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.contrib.base.resources.devices.PhoneDevice.PhoneDeviceAtomModuleBase import PhoneDeviceAtomModuleBase


class PhoneDeviceWrapModuleBase(PhoneDeviceAtomModuleBase):
    """
    PhoneDevice测试设备资源封装接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(PhoneDeviceWrapModuleBase, self).__init__(resource, *args, **kwargs)
