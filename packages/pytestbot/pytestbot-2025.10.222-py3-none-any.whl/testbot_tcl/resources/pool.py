#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.contrib.base.resources.ports.Port.Port import Port
from testbot.resource.pool import ResourcePool
from testbot.utils.project_utils import get_all_subclasses_in_installed_projects


class ProjectResourcePool(ResourcePool):
    """
    资源池类，负责资源的序列化和反序列化以及储存和读取
    """

    def assemble_resources(self):
        """
        组装测试资源
        """
        self.logger.info(f"Entering assemble_resources")
        pcs = self.select_resource(resource_type="MacosDevice", count=1)
        pc = pcs[0] if len(pcs)>0 else None
        tvs = self.select_resource(resource_type="TCLTVDevice", count=1)
        tv = tvs[0] if len(tvs) > 0 else None

        if tv and pc:
            if self.settings_mod:
                res_subclasses = get_all_subclasses_in_installed_projects(prj_setting=self.settings_mod, parent_class=Port)
                for port in [name for name, subclass in res_subclasses.items()]:
                    pc_port = pc.get_local_port(type=port)
                    tv_port = tv.get_local_port(type=port)
                    if pc_port and tv_port:
                        pc_port.remote_ports.append(tv_port)
                        tv_port.remote_ports.append(pc_port)
        self.logger.info(f"Exiting assemble_resources")
