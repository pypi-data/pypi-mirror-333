#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.resource.pool import ResourcePool


class ProjectResourcePool(ResourcePool):
    """
    资源池类，负责资源的序列化和反序列化以及储存和读取
    """

    def assemble_resources(self):
        """
        组装测试资源
        """
        pass
