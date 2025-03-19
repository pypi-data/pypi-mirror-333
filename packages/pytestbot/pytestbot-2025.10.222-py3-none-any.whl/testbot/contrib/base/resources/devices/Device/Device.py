#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.contrib.base.resources.ports.Port.Port import Port
from testbot.resource.Resource import Resource, _resource_device_mapping, ResourceError


class Device(Resource):
    """
    代表所有测试设备类
    """

    def __init__(self, name: str = "", *args, **kwargs):
        super(Device, self).__init__(name=name, *args, **kwargs)
        self.logger.info("Initialize Device...")
        self._instance = None

    def get_port_count(self, **kwargs: dict):
        """
        获取端口数量

        :param kwargs: 键值对参数
        :type kwargs: dict
        :return: 端口数量
        :rtype: int
        """
        return len(self.ports)

    def to_dict(self):
        ret = dict()
        for key, value in self.__dict__.items():
            if key in ["__instance", "logger"] or key.endswith("AtomModule") or key.endswith("WrapperModule"):
                continue
            if key == "ports":
                ret[key] = dict()
                for port_name, port in value.items():
                    ret[key][port_name] = port.to_dict()
            else:
                ret[key] = value
        return ret

    def get_comm_instance(self, new=False):
        if self.type not in _resource_device_mapping:
            raise ResourceError(f"type {self.type} is not registered")
        if not new and self._instance:
            return self._instance
        else:
            self._instance = _resource_device_mapping[self.type](self)
        return self._instance

    @staticmethod
    def from_dict(dict_obj):
        ret = Device()
        for key, value in dict_obj.items():
            if key == "ports":
                ports = dict()
                for port_name, port in value.items():
                    ports[port_name] = Port.from_dict(port, ret)
                setattr(ret, "ports", ports)
            else:
                setattr(ret, key, value)
        return ret
