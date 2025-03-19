#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"


import os
import json
from enum import Enum
from threading import Thread
from importlib import import_module
from abc import ABCMeta, abstractmethod

from testbot.config import CONFIG_PATH
from testbot.resource.pool import ResourcePool
from testbot.result.reporter import ResultReporter
from testbot.config.setting import static_setting, SettingBase


class PluginType(Enum):
    PRE = 1
    PARALLEL = 2
    POST =3


class PluginBase(metaclass=ABCMeta):
    """
    逻辑配置模块的基类
    """
    plugin_type = None
    priority = 99

    def __init__(self, report: ResultReporter, resource: ResourcePool):
        self.reporter = report

        self.resource = resource
        self.thread = None

    @abstractmethod
    def action(self):
        """
        实现该方法来实现模块的逻辑功能
        """
        pass

    def do(self):
        if self.plugin_type == PluginType.PARALLEL:
            self.thread = Thread(target=self.action)
            self.thread.start()
        else:
            self.action()

    @abstractmethod
    def stop(self):
        """
        实现该方法来实现模块逻辑功能的终止方法
        """
        pass


@static_setting.setting("PluginModule")
class PluginSetting(SettingBase):

    plugin_list_file = os.path.join(CONFIG_PATH, "pluginlist.json")
    plugin_setting_path = CONFIG_PATH


class PluginManager:
    """
    插件模块的管理
    """
    def __init__(self):
        self.plugins = dict()

    def load(self):
        """
        从模块列表装载所有模块类
        """
        if not os.path.exists(PluginSetting.plugin_list_file):
            # 如果没有找到插件配置文件，则不做任何操作
            return
        with open(PluginSetting.plugin_list_file) as file:
            obj = json.load(file)

        for item in obj['modules']:
            try:
                plugin_name = item['name']
                plugin_package = item['package']
                setting_file = item.get("setting_file", None)
                setting_path = item.get('setting_path', PluginSetting.plugin_setting_path)
                plugin = import_module(plugin_package)
                for element, value in plugin.__dict__.items():
                    if element == plugin_name:
                        self.plugins[plugin_name] = {
                            "class": value,
                            "setting_file": setting_file,
                            "setting_path": setting_path
                        }
            except Exception:
                pass

    def add_plugin(self, plugin_class, setting_file=None, setting_path=None):
        """
        添加插件
        """
        obj = {
            "class": plugin_class,
            "setting_file": setting_file,
            "setting_path": setting_path
        }
        self.plugins[plugin_class.__name__] = obj

    def get_plugin_instances(self, plugin_type, result_reporter, resources):
        """
        获取插件的实例化列表
        """
        rv = list()
        for pkey, pvalue in self.plugins.items():
            print(pvalue['class'].module_type)
            print(plugin_type)
            if pvalue['class'].module_type.value == plugin_type.value:
                rv.append(pvalue['class'](result_reporter, resources))
        return rv

    def save(self):
        """
        保存所有模块到模块配置列表
        """
        obj = dict()
        obj['plugins'] = list()
        for pkey, pvalue in self.plugins.items():
            obj['plugins'].append({
                "name": pkey,
                "package": pvalue["class"].__module__,
                "setting_file": pvalue['setting_file'],
                "setting_path": pvalue['setting_path']
            })
        file_dir = os.path.dirname(PluginSetting.plugin_list_file)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        with open(PluginSetting.plugin_list_file, "w") as _file:
            json.dump(obj, _file, indent=4)

    def run_plugin(self, type):
        pass

    def stop_plugin(self):
        pass


if __name__ == "__main__":
    pass
