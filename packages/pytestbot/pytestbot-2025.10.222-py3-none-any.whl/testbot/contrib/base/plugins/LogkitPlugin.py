#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.config import CONFIG_PATH
from testbot.resource.pool import ResourcePool
from testbot.result.testreporter import CaseStepEntry
from testbot.plugin.PluginBase import PluginBase, PluginType
from testbot.config.setting import dynamic_setting, SettingBase


@dynamic_setting
class LogkitPlugin(PluginBase):
    """
    抓取logkit日志插件
    """
    plugin_type = PluginType.PARALLEL
    priority = 0

    def __init__(self, step: CaseStepEntry, pool: ResourcePool, **kwargs):
        super().__init__(step=step, pool=pool)
        self.setting_path = kwargs.get("setting_path", CONFIG_PATH)
        self.filename = kwargs.get("filename", None)

    def action(self):
        """
        执行插件入口

        :return:
        :rtype:
        """
        if self.step:
            with self.step.start(headline="执行插件DEMO") as step:
                self.logger.info(f"执行插件DEMO")
                with step.start(headline="第一步执行XXX") as step2:
                    self.logger.info(f"第一步执行XXX")
                    if self.pool:
                        pass
                with step.start(headline="第二步执行YYY") as step2:
                    self.logger.info(f"第二步执行YYY")
        else:
            self.logger.info(f"执行插件DEMO")
            self.logger.info(f"第一步执行XXX")
            if self.pool:
                pass
            self.logger.info(f"第二步执行YYY")

    def stop(self):
        """
        停止执行插件

        :return:
        :rtype:
        """
        if self.step:
            with self.step.start(headline="停止执行插件") as step:
                pass
        else:
            self.logger.info(f"停止执行插件")

    # 插件配置
    class PluginSetting(SettingBase):
        setting_value = "a value"
