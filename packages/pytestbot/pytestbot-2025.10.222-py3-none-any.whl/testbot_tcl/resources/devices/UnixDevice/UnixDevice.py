#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
import re
import cv2
import time
import serial
from serial.tools import list_ports

from testbot.utils.serial_number import get_serial_number
from testbot.contrib.base.resources.devices.Device.Device import Device


class UnixDevice(Device):
    """
    Unix设备类
    """

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def to_dict(self) -> dict:
        return super(UnixDevice, self).to_dict()

    @classmethod
    def _discover_infra_port(cls):
        infra_port = None
        for port in list_ports.comports():
            if port[0].startswith("/dev/ttyUSB"):
                ser = None
                try:
                    ser = serial.Serial(port=port[0], baudrate=115200, timeout=1)
                    ser.write("\r\n".encode("UTF-8"))
                    ser.flush()
                    time.sleep(3)
                    data = ser.read_all()
                    if b'\xfe\xfd\xdf' in data:
                        infra_port = port[0]
                        ser.close()
                        break
                    else:
                        ser.close()
                except:
                    if ser:
                        ser.close()
        if not infra_port:
            raise Exception("搜索电视的红外串口失败！")
        return infra_port

    @classmethod
    def discover_resources(cls, settings_mod: str) -> dict:
        """
        发现测试资源，测试资源类型有：测试设备/软件/服务资源和测试端口资源，测试设备/软件/服务资源之间通过测试端口资源进行通信
        """
        res_objs = list()
        res_obj = cls(name=get_serial_number())

        infra_port, video_index, comm_port, ip, pc_sn, tv_sn = None, None, None, None, None, None
        try:
            infra_port = cls._discover_infra_port()
            if infra_port:
                res_obj.add_port(name=infra_port, type="InfraredSerialPort", baud_rate=115200)
        except:
            pass

        try:
            video_index = cls._discover_video_port()
            if video_index:
                res_obj.add_port(name=f"/dev/video{video_index}", type="VideoStreamSerialPort")
        except:
            pass

        try:
            comm_port = cls._discover_comm_port()
            if comm_port:
                res_obj.add_port(name=comm_port, type="CommSerialPort", baud_rate=115200)
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

    @classmethod
    def _discover_video_port(cls):
        video_index = None
        vid_indices = sorted(
            [int(dev.replace('video', '')) for dev in os.listdir('/dev') if dev.startswith('video') and dev])
        print(f"发现采集卡端口：{vid_indices}")
        for vid in vid_indices:
            cap = cv2.VideoCapture(index=vid)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920.0)  # 画面帧宽度
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080.0)  # 画面帧高度
            cap.set(cv2.CAP_PROP_FPS, 30.0)  # 帧率
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # 缓存帧数，返回False不支持缓冲区设置
            if not cap.isOpened() or not cap.grab():
                print(f"当前采集卡端口：{vid}")
                raise Exception("搜索电视的采集卡串口失败！")
            else:
                video_index = vid
                break
        return video_index

    @classmethod
    def _discover_comm_port(cls):
        comm_port = None
        for port in list_ports.comports():
            if port[0].startswith("/dev/ttyUSB"):
                ser = None
                try:
                    ser = serial.Serial(port=port[0], baudrate=115200, timeout=1)
                    ser.write("\r\n".encode("UTF-8"))
                    ser.flush()
                    time.sleep(3)
                    data = ser.read_all().decode("UTF-8")
                    if 'console' in data:
                        comm_port = port[0]
                        ser.close()
                        break
                    else:
                        ser.close()
                except:
                    if ser:
                        ser.close()
        if not comm_port:
            raise Exception("搜索电视的指令串口失败！")
        return comm_port

    @classmethod
    def _discover_ip_sn(cls, comm_port):
        tv_ip, tv_sn = None, None
        ser = None
        ips = []
        try:
            ser = serial.Serial(port=comm_port, baudrate=115200, timeout=1)
            ser.flush()
            ser.write("ifconfig\r\n".encode("UTF-8"))
            time.sleep(3)
            output = ser.read_all().decode("UTF-8").strip()
            pat_ipv4 = re.compile(r'^\s*inet addr:(\S+)', flags=re.M)
            for _ip in pat_ipv4.findall(output):
                if _ip != "127.0.0.1":
                    ips.append(_ip)
            ser.flush()
            ser.write("getprop ro.boot.serialno\r\n".encode("UTF-8"))
            time.sleep(3)
            output = ser.read_all().decode("UTF-8").strip()
            pat_sn = re.compile(r'^\s*getprop ro.boot.serialno\r\r\n(\S+)\r\nconsole:', flags=re.M)
            tv_sn = pat_sn.findall(output)[0]
            if len(ips) >= 1 and tv_sn != "":
                tv_ip = ips[0]
                ser.close()
            else:
                ser.close()
        except:
            if ser:
                ser.close()
        if not tv_ip:
            raise Exception("获取电视的IP地址/序列号信息失败！")
        return tv_ip, tv_sn
