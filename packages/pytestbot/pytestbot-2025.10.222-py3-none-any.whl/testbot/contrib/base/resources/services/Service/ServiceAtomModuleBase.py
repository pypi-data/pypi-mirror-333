#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.resource.ServiceModuleBase import ServiceModuleBase


class ServiceAtomModuleBase(ServiceModuleBase):
    """
    测试服务资源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(ServiceAtomModuleBase, self).__init__(resource, *args, **kwargs)
