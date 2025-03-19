#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import time

import serial

from testbot.contrib.base.resources.ports.SerialPort import SerialPort


class CommSerialPort(SerialPort):
    """
    代表CommSerial端口类
    """

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def initialize_resource(self, test_type, reload: bool = True):
        """
        初始化测试资源

        :return:
        :rtype:
        """
        if self._instance and self._instance.isOpen():
            if reload:
                self._instance.close()
                time.sleep(5)
                self._instance = serial.Serial(port=self.name, baudrate=self.baudrate, timeout=1)
        else:
            self._instance = serial.Serial(port=self.name, baudrate=self.baudrate, timeout=1)
        if not self._instance:
            raise Exception("初始化指令串口端口失败！")
