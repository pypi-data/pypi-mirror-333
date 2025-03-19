#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.resource.Resource import Resource, _resource_port_mapping, ResourceError


class Port(Resource):
    """
    代表所有端口类
    """

    def __init__(self, parent = None, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)
        self.baudrate = kwargs.get("baudrate", 115200)
        self.parent = parent
        self.remote_ports = list()
        self._instance = None

    def get_comm_instance(self, new=False):
        if self.type not in _resource_port_mapping:
            raise ResourceError(f"type {self.type} is not registered")
        if not new and self._instance:
            return self._instance
        else:
            self._instance = _resource_port_mapping[self.type](self)
        return self._instance

    def to_dict(self):
        ret = dict()
        for key, value in self.__dict__.items():
            if key in ["__instance", "logger"]:
                continue
            if key == "parent":
                ret[key] = value.name
            elif key == "remote_ports":
                ret[key] = list()
                for remote_port in value:
                    # 使用device的名称和port的名称来表示远端的端口
                    # 在反序列化的时候可以方便地找到相应的对象实例
                    ret[key].append(
                        {
                            "resource": remote_port.parent.name,
                            "port": remote_port.name
                        }
                    )
            else:
                ret[key] = value
        return ret

    def get_remote_port(self, type):
        res_obj = None
        for _port in getattr(self, "remote_ports", []):
            self.logger.info(f"_port={_port}")
            if _port.type == self.type:
                res_obj = _port
        return res_obj

    def get_remote_resource(self, type):
        res_obj = None
        remote_port = self.get_remote_port(type=type)
        if remote_port:
            res_obj = remote_port.parent
        return res_obj

    @staticmethod
    def from_dict(dict_obj, parent):
        ret = Port(parent)
        for key, value in dict_obj.items():
            if key == "remote_ports" or key == "parent":
                continue
            setattr(ret, key, value)
        return ret
