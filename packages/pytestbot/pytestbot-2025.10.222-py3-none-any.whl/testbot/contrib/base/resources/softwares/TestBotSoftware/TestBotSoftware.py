#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.config.setting import dynamic_setting, SettingBase
from testbot.contrib.base.resources.softwares.Software.Software import Software


@dynamic_setting
class TestBotSoftware(Software):
    """
    TestBot测试软件类
    """

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def to_dict(self) -> dict:
        return dict()

    def update_json_data(self):
        data = self.DocWrapperModule.get_apis()
        self.setting.apis = data
        self.setting.save()

    class Setting(SettingBase):
        atom_pkg = (None, None)
        wrapper_pkg = (None, None)

