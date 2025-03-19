#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.contrib.base.resources.devices.TVDevice.TVDevice import TVDevice
from testbot.contrib.base.resources.devices.UnixDevice.UnixDevice import UnixDevice


class TCLTVDevice(TVDevice):
    """
    TCL电视设备类
    """

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def to_dict(self) -> dict:
        return dict()

    @classmethod
    def discover_resources(cls, settings_mod: str) -> list:
        """
        发现测试资源，测试资源类型有：测试设备/软件/服务资源和测试端口资源，测试设备/软件/服务资源之间通过测试端口资源进行通信
        """
        res_objs = list()
        res_obj = None

        try:
            comm_port = cls._discover_comm_port()
            if comm_port:
                res_obj = cls(name=comm_port)
                res_obj.add_or_update_port(name="CommSerialPort", type="CommSerialPort")
        except:
            pass

        try:
            infra_port = cls._discover_infra_port()
            if res_obj and infra_port:
                res_obj.add_or_update_port(name="InfraredSerialPort", type="InfraredSerialPort")
        except:
            pass

        try:
            video_index = cls._discover_video_port()
            if res_obj and video_index:
                res_obj.add_or_update_port(name="VideoStreamSerialPort", type="VideoStreamSerialPort")
        except:
            pass

        try:
            ip, tv_sn = UnixDevice._discover_ip_sn(comm_port=comm_port)
            if res_obj and ip:
                res_obj.add_or_update_port(name="AdbPort", type="AdbPort")
                res_obj.add_or_update_port(name="GRPCPort", type="GRPCPort")
        except:
            pass

        if res_obj:
            res_obj.add_or_update_port(name="PowerPort", type="PowerPort")
            res_obj.add_or_update_port(name="HDMIPort", type="HDMIPort")
            res_obj.add_or_update_port(name="EthernetPort", type="EthernetPort")
            res_obj.add_or_update_port(name="USBPort", type="USBPort")
            res_objs.append(res_obj)
        return res_objs


if __name__ == "__main__":
    device = TCLTVDevice(name="TV1")
    device.logger.info("This is TCL TV Device")
