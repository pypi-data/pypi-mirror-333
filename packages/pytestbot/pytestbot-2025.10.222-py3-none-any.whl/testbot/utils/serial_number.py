#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"


import os
import re
import platform
if platform.system() == 'Windows':
    import wmi
    import pythoncom
    pythoncom.CoInitialize()


def get_bios_sn():
    sn = ""
    if platform.system() == 'Windows':
        c = wmi.WMI()
        for id in c.Win32_BIOS():
            sn = id.SerialNumber
            break
    return sn

def get_disk_sn():
    sn = ""
    if platform.system() == 'Windows':
        c = wmi.WMI()
        for id in c.Win32_DiskDrive():
            sn = id.SerialNumber
            break
    return sn

def get_serial_number():
    sn = None
    try:
        if platform.system() == "Windows":
            sn = get_bios_sn().strip()
            if sn == "":
                sn = get_disk_sn()
        elif platform.system() == "Linux":
            data = open('/proc/cpuinfo', 'r').read()
            pat_sn = re.compile(r'^\s*Serial\t\t: (\S+)\n', flags=re.M)
            sns = pat_sn.findall(data)
            sn = sns[0]
        elif platform.system() == "Darwin":
            # 执行命令并获取输出
            pipe = os.popen('system_profiler SPHardwareDataType | grep "Serial Number (system):"')
            output = pipe.read().strip()
            pipe.close()
            if output:
                # 提取序列号
                sn = output.split(':')[-1].strip()
    except Exception as e:
        print(f"An error occurred: {e}")
    return sn
