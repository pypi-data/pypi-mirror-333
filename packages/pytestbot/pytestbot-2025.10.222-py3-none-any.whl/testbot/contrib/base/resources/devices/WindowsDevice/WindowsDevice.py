#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.contrib.base.resources.devices.Device.Device import Device


class WindowsDevice(Device):
    """
    Windows设备类
    """

    def __init__(self, name: str = "", *args, **kwargs):
        super(WindowsDevice, self).__init__(name=name, *args, **kwargs)
