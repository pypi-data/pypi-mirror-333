#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
import time
import json
import platform

from testbot.contrib.base.resources.devices.Device.Device import Device
from testbot.resource.Resource import ResourceError, Resource
from testbot.result.logger import logger_manager
from testbot.config import MODULE_LOGS_PATH, CONFIG_PATH
from testbot.config.static_setting import ResourceSetting
from testbot.utils.project_utils import get_all_subclasses_in_installed_projects
from testbot.resource.constraint import ConnectionConstraint, ResourceNotMeetConstraint


class ResourcePool(object):
    """
    资源池类，负责资源的序列化和反序列化以及储存和读取
    """
    def __init__(self, *args, **kwargs):
        self.settings_mod = kwargs.get('settings_mod', os.environ.get('TESTBOT_SETTINGS_MODULE', None))
        self.logger = kwargs.get("logger", logger_manager.register(logger_name="Resource", filename=os.path.join(MODULE_LOGS_PATH, "Resource.log"), for_test=True))
        self.topology = dict()
        self.reserved = None
        self.information = dict()
        self.file_name = None
        self.owner = None

    def add_or_update_resource(self, name: str, **kwargs):
        """
        添加测试资源到资源池

        :param name: 测试资源名称
        :type name: str
        :param kwargs: 键值对参数
        :type kwargs: dict
        :return: None
        :rtype: NoneType
        """
        self.logger.info(f"Entering {self.__class__.__name__}.add_device...")
        if name in self.topology:
            raise ResourceError(f"device {name} already exists")
        self.topology[name] = Resource(name=name, **kwargs)
        self.logger.info(f"Exiting {self.__class__.__name__}.add_device...")

    def reserve(self):
        """
        占用当前资源

        :return:
        :rtype:
        """
        self.logger.info(f"Entering {self.__class__.__name__}.reserve...")
        if self.file_name is None:
            raise ResourceError("load a resource file first")
        self.load(self.file_name, self.owner)
        self.reserved = {"owner": self.owner, "date": time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())}
        self.save(self.file_name)
        self.logger.info(f"Exiting {self.__class__.__name__}.reserve...")

    def release(self):
        """
        释放当前资源

        :return:
        :rtype:
        """
        self.logger.info(f"Entering {self.__class__.__name__}.release...")
        if self.file_name is None:
            raise ResourceError("load a resource file first")
        self.load(self.file_name)
        self.reserved = None
        self.save(self.file_name)
        self.logger.info(f"Exiting {self.__class__.__name__}.release...")

    def select_resource(self, resource_type, count, constraints=list()):
        ret = list()
        for key, value in self.topology.items():
            if value.type == resource_type:
                for constraint in constraints:
                    if not constraint.is_meet(value):
                        break
                else:
                    ret.append(value)
            if len(ret) >= count:
                return ret
        else:
            return list()

    def select_all_resources(self, resource_type, constraints=list()):
        ret = list()
        for key, value in self.topology.items():
            if value.type == resource_type:
                for constraint in constraints:
                    if not constraint.is_meet(value):
                        break
                else:
                    ret.append(value)
        return ret

    def collect_connection_route(self, resource: str, constraints: list=list()) -> list:
        """
        获取资源连接路由

        :param resource:
        :type resource:
        :param constraints:
        :type constraints:
        :return: 链接路由
        :rtype: list
        """
        # 限制类必须是连接限制ConnectionConstraint
        for constraint in constraints:
            if not isinstance(constraint, ConnectionConstraint):
                raise ResourceError(
                    "collect_connection_route only accept ConnectionConstraints type")
        ret = list()
        for constraint in constraints:
            conns = constraint.get_connection(resource)
            if not any(conns):
                raise ResourceNotMeetConstraint([constraint])
            for conn in conns:
                ret.append(conn)
        return ret

    def load(self, filename: str, owner: str):
        """
        加载文件

        :param filename: 文件路径
        :type filename: str
        :param owner: 资源所有人
        :type owner: str
        :return: None
        :rtype: NoneType
        """
        self.logger.info(f"Entering {self.__class__.__name__}.load...")
        # 检查文件是否存在
        if not os.path.exists(filename):
            self.save(filename=filename)
        self.file_name = filename

        # 初始化
        self.topology.clear()
        self.reserved = False
        self.information = dict()

        #读取资源配置的json字符串
        with open(filename) as file:
            json_object = json.load(file)

        #判断是否被占用
        # if "reserved" in json_object and json_object['reserved'] is not None and json_object['reserved']['owner'] != owner:
        #     raise ResourceError(f"Resource is reserved by {json_object['reserved']['owner']}")

        self.owner = owner

        if "info" in json_object:
            self.information = json_object['info']
        for key, value in json_object.get('resources', {}).items():
            res_subclasses = get_all_subclasses_in_installed_projects(prj_setting=self.settings_mod, parent_class=Resource)
            for name, subclass in res_subclasses.items():
                if name==value.get("type", None) and getattr(subclass, "from_dict", None):
                    res_obj = subclass.from_dict(dict_obj=value)
                    self.topology[key] = res_obj

        # 映射所有测试资源的连接关系
        for key, resource in json_object.get('resources', {}).items():
            for port_name, port in resource.get('ports', {}).items():
                for remote_port in port.get('remote_ports', []):
                    remote_port_obj = self.topology[remote_port["device"]].ports[remote_port["port"]]
                    self.topology[key].ports[port_name].remote_ports.append(remote_port_obj)
        self.logger.info(f"topology={self.topology}")
        self.logger.info(f"Exiting {self.__class__.__name__}.load...")

    def to_dict(self):
        root_object = dict()
        root_object['resources'] = dict()
        root_object['info'] = self.information
        root_object['reserved'] = self.reserved
        for device_key, device in self.topology.items():
            root_object['resources'][device_key] = device.to_dict()
        return root_object

    def save(self, filename: str):
        """
        保存文件

        :param filename: 文件路径
        :type filename: str
        :return: None
        :rtype: NoneType
        """
        self.logger.info(f"Entering {self.__class__.__name__}.save...")
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, mode="w") as file:
            json.dump(self.to_dict(), file, indent=4)
        self.logger.info(f"Exiting {self.__class__.__name__}.save...")

    def _set_power_on(self):
        if platform.system() == 'Linux':
            import RPi.GPIO as GPIO
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(12, GPIO.OUT)
            GPIO.output(12, GPIO.HIGH)

    def discover_resources(self, filename: str = os.path.join(CONFIG_PATH, "pool.json"), owner: str = "sunny"):
        # self.load(filename=filename, owner=owner)

        if self.settings_mod:
            res_subclasses = get_all_subclasses_in_installed_projects(prj_setting=self.settings_mod, parent_class=Device)
            for name, subclass in res_subclasses.items():
                if getattr(subclass, "discover_resources", None):
                    self.logger.info(subclass)
                    try:
                        for res in subclass.discover_resources(settings_mod=self.settings_mod):
                            self.logger.info(res)
                            self.topology[res.name] = res
                    except Exception as ex:
                        import traceback
                        traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                        self.logger.error(traceinfo)
        if getattr(self, "assemble_resources", None):
            self.assemble_resources()

        self.logger.info(f"pool={self.to_dict()}")
        # self.save(filename=filename)

    def init_resources(self, test_type):
        self.logger.info(f"pool.topology = {self.topology}")
        self.logger.info(f"test_type = {test_type}")
        for name, res_obj in self.topology.items():
            res_obj.initialize_resource(test_type=test_type)

def get_resource_pool(filename: str, owner: str) -> ResourcePool:
    """
    获取资源池，加载本地json文件以获取资源池，并设置该资源池的owner所有者

    :param filename: 资源池json文件路径
    :type filename: str
    :param owner: 资源所有者
    :type owner: str
    :return: 资源池对象
    :rtype: ResourcePool
    """
    ResourceSetting.load()
    full_name = os.path.join(ResourceSetting.resource_path, filename)
    rv = ResourcePool()
    rv.load(full_name, owner)
    return rv

