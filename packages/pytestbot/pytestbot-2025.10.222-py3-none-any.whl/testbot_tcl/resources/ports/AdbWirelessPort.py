#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import time

import adbutils
import serial

from testbot.app.TestApplicationBase import TESTTYPE_CHECKLIST, CheckItem
from testbot.contrib.base.resources.ports.SerialPort import SerialPort


class AdbWirelessPort(SerialPort):
    """
    代表AdbWireless端口类
    """

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def initialize_resource(self, test_type, reload: bool = True):
        """
        初始化测试资源

        :return:
        :rtype:
        """
        for checkitem in TESTTYPE_CHECKLIST.get(test_type, []):
            self.logger.info(f"检查项：{checkitem.name}")
            ip_port = self.name
            if CheckItem.COMM_SERIAL_PORT_CHECK__EXIST in TESTTYPE_CHECKLIST.get(test_type, []):
                ips = self.get_remote_resource(type="AdbWirelessPort").CommSerialWrapperModule.get_ip_addresses()
                if len(ips) >= 1:
                    ip_port = f"{ips[0]:5555}"
            # 建立adb connect连接
            self.logger.info(f"IP={ip_port}")
            adbutils.adb.connect(addr=ip_port, timeout=5)
            # 获取adb客户端对象
            self._instance = adbutils.AdbClient(host="127.0.0.1", port=5037)
            if not self._instance:
                raise Exception("初始化adb无线连接端口失败！")
