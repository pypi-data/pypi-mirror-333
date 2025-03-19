#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
from abc import ABCMeta, abstractmethod

from testbot.config import MODULE_LOGS_PATH
from testbot.result.logger import logger_manager
from testbot.app.TestApplicationBase import TestType
from testbot.utils.project_utils import get_all_subclasses_in_installed_projects, get_atom_module_base_class, \
    get_wrap_module_base_class

# 存放用户注册的配置接口对象类型
_resource_device_mapping = dict()
_resource_port_mapping = dict()


class ResourceError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def register_resource(category, resource_type, comm_callback):
    """
    注册配置接口实例化的方法或者类。
    """
    if category == "device":
        _resource_device_mapping[resource_type] = comm_callback
    elif category == "port":
        _resource_port_mapping[resource_type] = comm_callback


class Resource(metaclass=ABCMeta):
    """
    代表所有测试资源设备的配置类，字段动态定义
    """
    name: str
    type: str
    description: str

    @classmethod
    def discover_resources(cls, settings_mod: str) -> list:
        """
        发现测试资源，测试资源类型有：测试设备/软件/服务资源和测试端口资源，测试设备/软件/服务资源之间通过测试端口资源进行通信
        """
        return list()

    def __init__(self, name: str, *args, **kwargs):
        self.settings_mod = kwargs.get('settings_mod', os.environ.get('TESTBOT_SETTINGS_MODULE', None))
        self.logger = kwargs.get("logger", logger_manager.register(
            logger_name="Resource",
            filename=os.path.join(MODULE_LOGS_PATH, "Resource.log"),
            for_test=True
        ))
        self.ports = dict()
        if self.settings_mod:
            for module_base_clz in [get_atom_module_base_class(resource_class=self.__class__), get_wrap_module_base_class(resource_class=self.__class__)]:
                found_subclasses = get_all_subclasses_in_installed_projects(prj_setting=self.settings_mod, parent_class=module_base_clz)
                for name, subclass in found_subclasses.items():
                    if name.endswith("ModuleBase"):
                        continue
                    print("加载接口模块：", name, subclass)
                    setattr(self, name, subclass(resource=self, logger=self.logger))

        self.name = name
        self.type = kwargs.get("type", self.__class__.__name__)
        self.description = kwargs.get("description", "")
        self.pre_connect = False
        self.client_attributes = dict()
        self.shared_attributes = dict()
        self.server_attributes = dict()
        self.reserved = False
        self._alive = False

    def initialize_resources(self, test_type):
        """
        初始化测试资源
        """
        pass

    def add_or_update_port(self, name: str, *args: tuple, **kwargs: dict):
        """
        添加端口

        :param name: 端口名称
        :type name: str
        :param args: 元祖参数
        :type args: tuple
        :param kwargs: 键值对参数
        :type kwargs: dict
        :return: None
        :rtype: NoneType
        """
        self.logger.info(f"Entering {self.__class__.__name__}.add_port...")
        settings_mod = os.environ.get('TESTBOT_SETTINGS_MODULE', None)
        if settings_mod and kwargs.get("type", None):
            from testbot.contrib.base.resources.ports.Port.Port import Port
            port_subclasses = get_all_subclasses_in_installed_projects(prj_setting=settings_mod, parent_class=Port)
            for name, subclass in port_subclasses.items():
                if name == kwargs.get("type", None):
                    self.ports[f"{name}"] = subclass(parent=self, name=name, *args, **kwargs)
        self.logger.info(f"Exiting {self.__class__.__name__}.add_port...")

    def __del__(self):
        self.clean_resource()

    @abstractmethod
    def to_dict(self) -> dict:
        """
        预留序列化接口，即将Resource对象序列化为字典对象

        :return: 序列化后的字典对象
        :rtype: dict
        """
        return dict()

    @classmethod
    def from_dict(cls, dict_obj):
        """
        预留反序列化接口，即从字典对象反序列化为Resource对象

        :return: 反序列化后的Resource对象
        :rtype: Resource
        """
        return None

    def get_remote_port(self, type):
        self.logger.info(f"self={self.ports}")
        for name, port in self.ports.items():
            self.logger.info(f"name, port={name}, {port}")
            if port.type == type:
                for _port in port.remote_ports:
                    self.logger.info(f"_port={_port}")
                    if _port.type == type:
                        return _port
        return None

    def get_local_port(self, type):
        self.logger.info(f"self={self.ports}")
        for name, port in self.ports.items():
            self.logger.info(f"name, port={name}, {port}")
            if port.type == type:
                return port
        return None

    def initialize_resource(self, test_type: TestType, reload: bool = True):
        """
        初始化测试资源

        :return:
        :rtype:
        """
        pass

    def clean_resource(self):
        pass