#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.contrib.base.resources.devices.Device.Device import Device
from testbot.utils.serial_number import get_serial_number


class MacosDevice(Device):
    """
    Macos设备类
    """

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    @classmethod
    def discover_resources(cls) -> dict:
        """
        发现测试资源，测试资源类型有：测试设备/软件/服务资源和测试端口资源，测试设备/软件/服务资源之间通过测试端口资源进行通信
        """
        return dict()
