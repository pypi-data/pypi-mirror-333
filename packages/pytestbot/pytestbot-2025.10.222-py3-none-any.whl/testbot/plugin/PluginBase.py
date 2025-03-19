#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"


import os
from enum import Enum
from threading import Thread
from abc import ABCMeta, abstractmethod

from testbot.config import MODULE_LOGS_PATH
from testbot.result.logger import logger_manager
from testbot.result.testreporter import CaseStepEntry


class PluginType(Enum):
    PRE = 1
    PARALLEL = 2
    POST =3


class PluginBase(metaclass=ABCMeta):
    """
    插件模块的基类
    """
    plugin_type = None
    priority = 99

    def __init__(self, step: CaseStepEntry, pool, **kwargs):
        self.step = step
        self.logger = kwargs.get("logger", logger_manager.register(logger_name="Plugin", filename=os.path.join(MODULE_LOGS_PATH,"Plugin.log"), for_test=True))
        self.pool = pool
        self.thread = None

    @abstractmethod
    def action(self):
        """
        实现该方法来实现插件的逻辑功能
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
