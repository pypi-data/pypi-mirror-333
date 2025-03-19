#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"


from testbot.contrib.base.resources.devices.AndroidDevice.AndroidDevice import AndroidDevice
from testbot.contrib.base.resources.ports.Port.Port import Port


class TVDevice(AndroidDevice):
    """
    电视设备类
    """


    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def to_dict(self) -> dict:
        return super(TVDevice, self).to_dict()

    @classmethod
    def from_dict(cls, dict_obj):
        """
        预留反序列化接口，即从字典对象反序列化为Resource对象

        :return: 反序列化后的Resource对象
        :rtype: Resource
        """
        res = TVDevice(**dict_obj)
        for key, value in dict_obj.items():
            if key == "ports":
                ports = dict()
                for port_name, port in value.items():
                    ports[port_name] = Port.from_dict(port, res)
                setattr(res, "ports", ports)
            else:
                setattr(res, key, value)
        return res
