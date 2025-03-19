#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import time

import cv2

from testbot.contrib.base.resources.ports.SerialPort import SerialPort


class VideoStreamSerialPort(SerialPort):
    """
    代表VideoStreamSerial端口类
    """

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def initialize_resource(self, test_type, reload: bool = True):
        """
        初始化测试资源

        :return:
        :rtype:
        """
        if self._instance and self._instance.isOpened():
            if reload:
                self._instance.release()
                time.sleep(5)
                self._instance = cv2.VideoCapture(int(self.name.replace("/dev/video", "")))
                self._instance.set(cv2.CAP_PROP_FRAME_WIDTH, 1920.0)  # 画面帧宽度
                self._instance.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080.0)  # 画面帧高度
                self._instance.set(cv2.CAP_PROP_FPS, getattr(self, "fps", 30.0))  # 帧率
                self._instance.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # 缓存帧数，返回False不支持缓冲区设置
        else:
            self._instance = cv2.VideoCapture(int(self.name.replace("/dev/video", "")))
            self._instance.set(cv2.CAP_PROP_FRAME_WIDTH, 1920.0)  # 画面帧宽度
            self._instance.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080.0)  # 画面帧高度
            self._instance.set(cv2.CAP_PROP_FPS, getattr(self, "fps", 30.0))  # 帧率
            self._instance.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # 缓存帧数，返回False不支持缓冲区设置
        if not self._instance.isOpened() or not self._instance.grab():
            raise Exception("Capture enable failed！")
        if not self._instance:
            raise Exception("初始化采集卡端口失败！")
