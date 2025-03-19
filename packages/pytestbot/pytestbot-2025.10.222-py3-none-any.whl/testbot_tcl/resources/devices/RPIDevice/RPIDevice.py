#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import platform

from testbot.contrib.base.resources.devices.LinuxDevice.LinuxDevice import LinuxDevice
from testbot.utils.serial_number import get_serial_number


class RPIDevice(LinuxDevice):
    """
    RPI树莓派设备类
    """

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    @classmethod
    def discover_resources(cls, settings_mod: str) -> list:
        """
        发现测试资源，测试资源类型有：测试设备/软件/服务资源和测试端口资源，测试设备/软件/服务资源之间通过测试端口资源进行通信
        """
        res_objs = list()
        if platform.system()!="Linux":
            return res_objs

        res_obj = cls(name=get_serial_number())

        infra_port, video_index, comm_port, ip, pc_sn, tv_sn = None, None, None, None, None, None
        try:
            infra_port = cls._discover_infra_port()
            if infra_port:
                res_obj.add_or_update_port(name=infra_port, type="InfraredSerialPort", baud_rate=115200)
        except:
            pass

        try:
            video_index = cls._discover_video_port()
            if video_index:
                res_obj.add_or_update_port(name=f"/dev/video{video_index}", type="VideoStreamSerialPort")
        except:
            pass

        try:
            comm_port = cls._discover_comm_port()
            if comm_port:
                res_obj.add_or_update_port(name=comm_port, type="CommSerialPort", baud_rate=115200)
        except:
            pass

        try:
            ip, tv_sn = cls._discover_ip_sn(comm_port=comm_port)
            if ip:
                res_obj.add_or_update_port(name=f"{ip}:5555", type="AdbPort")
                res_obj.add_or_update_port(name=f"{ip}:60000", type="GRPCPort")
        except:
            pass

        res_obj.add_or_update_port(name="GPIO12", type="PowerPort")
        res_obj.add_or_update_port(name="GPIO26", type="HDMIPort")
        res_obj.add_or_update_port(name="GPIO21", type="EthernetPort")
        res_obj.add_or_update_port(name="GPIO5/6", type="USBPort")

        res_objs.append(res_objs)
        return res_objs
