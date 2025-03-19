#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import platform

from testbot.app.TestApplicationBase import TestType, TESTTYPE_CHECKLIST, CheckItem
from testbot.utils.serial_number import get_serial_number
from testbot.contrib.base.resources.devices.UnixDevice.UnixDevice import UnixDevice


class MacosDevice(UnixDevice):
    """
    Macos设备类
    """

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    @classmethod
    def discover_resources(cls, settings_mod: str) -> list:
        """
        发现测试资源，测试资源类型有：测试设备/软件/服务资源和测试端口资源，测试设备/软件/服务资源之间通过测试端口资源进行通信
        """
        res_objs = list()
        if platform.system()!="Darwin":
            return res_objs

        res_obj = cls(name=get_serial_number())

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
                res_obj.add_port(name=f"{ip}:5555", type="AdbPort")
                res_obj.add_port(name=f"{ip}:60000", type="GRPCPort")
        except:
            pass

        res_objs.append(res_obj)
        return res_objs

    def initialize_resource(self, test_type: TestType, reload: bool = True):
        """
        初始化测试资源

        :return:
        :rtype:
        """
        for checkitem in TESTTYPE_CHECKLIST.get(test_type, []):
            self.logger.info(f"检查项：{checkitem.name}")
            # 是否有指令串口
            if checkitem == CheckItem.COMM_SERIAL_PORT_CHECK__EXIST:
                port_obj = self.get_local_port(type="CommSerialPort")
                if port_obj:
                    port_obj.init_resource(test_type=test_type, reload=reload)

            # 是否可以通过指令串口获取TV IP地址
            if checkitem == CheckItem.COMM_SERIAL_PORT_CHECK__HAS_IP:
                self.logger.info(f"对资源类型：{self.type}，资源名称：{self.name}，执行检查项：{checkitem}：是否可以通过指令串口获取TV IP地址")
            # TV端是否可以正常访问公司网络，如Panda、AI服务
            if checkitem == CheckItem.COMM_SERIAL_PORT_CHECK__ACCESS_INTERNAL_NET:
                self.logger.info(f"对资源类型：{self.type}，资源名称：{self.name}，执行检查项：{checkitem}：TV端是否可以正常访问公司网络，如Panda、AI服务")
            # TV端是否可以正常访问国内网络
            if checkitem == CheckItem.COMM_SERIAL_PORT_CHECK__ACCESS_DOMESTIC_NET:
                self.logger.info(f"对资源类型：{self.type}，资源名称：{self.name}，执行检查项：{checkitem}：TV端是否可以正常访问国内网络")
            # TV端是否可以正常访问海外网络
            if checkitem == CheckItem.COMM_SERIAL_PORT_CHECK__ACCESS_OVERSEAS_NET:
                self.logger.info(f"对资源类型：{self.type}，资源名称：{self.name}，执行检查项：{checkitem}：TV端是否可以正常访问海外网络")

            # 是否有红外串口
            if checkitem == CheckItem.INFRA_SERIAL_PORT_CHECK__EXIST:
                port_obj = self.get_local_port(type="InfraredSerialPort")
                if port_obj:
                    port_obj.init_resource(test_type=test_type, reload=reload)

            # 通过红外串口发送红外指令是否正常
            if checkitem == CheckItem.INFRA_SERIAL_PORT_CHECK__NORMAL:
                self.logger.info(f"对资源类型：{self.type}，资源名称：{self.name}，执行检查项：{checkitem}：通过红外串口发送红外指令是否正常")

            # 是否有采集卡串口
            if checkitem == CheckItem.CAP_SERIAL_PORT_CHECK__EXIST:
                port_obj = self.get_local_port(type="VideoStreamSerialPort")
                if port_obj:
                    port_obj.init_resource(test_type=test_type, reload=reload)

            # 是否能够通过采集卡串口采集图像正常
            if checkitem == CheckItem.CAP_SERIAL_PORT_CHECK__NORMAL:
                self.logger.info(f"对资源类型：{self.type}，资源名称：{self.name}，执行检查项：{checkitem}：是否能够通过采集卡串口采集图像正常")

            # 是否有音频口
            if checkitem == CheckItem.AUDIO_PORT_CHECK__EXIST:
                self.logger.info(f"对资源类型：{self.type}，资源名称：{self.name}，执行检查项：{checkitem}：是否有音频口")
            # 音频口是否检测有声音
            if checkitem == CheckItem.AUDIO_PORT_CHECK__HAS_SOUND:
                self.logger.info(f"对资源类型：{self.type}，资源名称：{self.name}，执行检查项：{checkitem}：音频口是否检测有声音")

            # 是否有电源通断口
            if checkitem == CheckItem.POWER_PORT_CHECK__EXIST:
                self.logger.info(f"对资源类型：{self.type}，资源名称：{self.name}，执行检查项：{checkitem}：是否有电源通断口")

            # 是否有ADB无线连接
            if checkitem == CheckItem.ADB_WIRELESS_PORT_CHECK__EXIST:
                self.logger.info(f"对资源类型：{self.type}，资源名称：{self.name}，执行检查项：{checkitem}：是否有ADB无线连接")
                port_obj = self.get_local_port(type="AdbWirelessPort")
                if port_obj:
                    port_obj.init_resource(test_type=test_type, reload=reload)

            # 是否有ADB有线连接
            if checkitem == CheckItem.ADB_WIRE_PORT_CHECK__EXIST:
                self.logger.info(f"对资源类型：{self.type}，资源名称：{self.name}，执行检查项：{checkitem}：是否有ADB有线连接")

            # 是否有gRPC连接
            if checkitem == CheckItem.GRPC_PORT_CHECK__EXIST:
                port_obj = self.get_local_port(type="GRPCPort")
                if port_obj:
                    port_obj.init_resource(test_type=test_type, reload=reload)

            # 是否有网卡通断口
            if checkitem == CheckItem.ETHER_PORT_CHECK__EXIST:
                self.logger.info(f"对资源类型：{self.type}，资源名称：{self.name}，执行检查项：{checkitem}：是否有网卡通断口")
            # 是否能够从PC端访问TV端的IP地址
            if checkitem == CheckItem.ETHER_PORT_CHECK__ACCESS_IP:
                self.logger.info(f"对资源类型：{self.type}，资源名称：{self.name}，执行检查项：{checkitem}：是否能够从PC端访问TV端的IP地址")

            # 是否有U盘通断口
            if checkitem == CheckItem.UDISK_PORT_CHECK__EXIST:
                self.logger.info(f"对资源类型：{self.type}，资源名称：{self.name}，执行检查项：{checkitem}：是否有U盘通断口")

            # 是否有U盘插入
            if checkitem == CheckItem.UDISK_PORT_CHECK__HAS_UDISK:
                self.logger.info(f"对资源类型：{self.type}，资源名称：{self.name}，执行检查项：{checkitem}：是否有U盘插入")

