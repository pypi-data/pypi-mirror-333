#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import platform

from testbot.contrib.base.resources.devices.UnixDevice.UnixDevice import UnixDevice


class LinuxDevice(UnixDevice):
    """
    Linux设备类
    """

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    @classmethod
    def discover_resources(cls, settings_mod: str) -> list:
        """
        发现测试资源，测试资源类型有：测试设备/软件/服务资源和测试端口资源，测试设备/软件/服务资源之间通过测试端口资源进行通信
        """
        res_objs = list()
        if platform.system() != "Linux":
            return res_objs
