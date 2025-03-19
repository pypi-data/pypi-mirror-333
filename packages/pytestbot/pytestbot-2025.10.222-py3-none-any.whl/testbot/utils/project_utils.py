#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import sys
import importlib
import inspect
import os.path
import pkgutil



def get_atom_module_base_class(resource_class):
    mod = getattr(importlib.import_module(f"{resource_class.__module__}AtomModuleBase"), f"{resource_class.__name__}AtomModuleBase")
    return mod


def get_wrap_module_base_class(resource_class):
    mod = getattr(importlib.import_module(f"{resource_class.__module__}WrapModuleBase"), f"{resource_class.__name__}WrapModuleBase")
    return mod


def get_all_subclasses_in_installed_projects(prj_setting: str, parent_class) -> dict:
    """
    获取指定项目设置包路径的所有已安装的项目模块，后序遍历已安装的项目链
    """
    # print(f"###  {prj_setting}:Enter  ###")
    subclasses = dict()
    prj_setting_mod = importlib.import_module(prj_setting)
    prj_resources_mod = importlib.import_module(f"{prj_setting_mod.__package__}.resources")
    for _prj_setting in getattr(prj_setting_mod, "INSTALLED_PROJECTS", []):
        subclasses.update(get_all_subclasses_in_installed_projects(prj_setting=_prj_setting, parent_class=parent_class))
    subclasses.update(find_subclasses(pkg=prj_resources_mod, parent_class=parent_class))
    # print(f"###  {prj_setting}:Exit  ###")
    return subclasses

def find_subclasses(pkg, parent_class) -> dict:
    """
    在指定包下找到所有指定父类的子类
    """
    subclasses = dict()
    for importer, modname, ispkg in pkgutil.walk_packages(path=pkg.__path__, prefix=pkg.__name__ + "."):
        try:
            module = importlib.import_module(modname)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, parent_class) and obj != parent_class:
                    subclasses[obj.__name__] = obj
        except ImportError as ex:
            import traceback
            traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
            print(traceinfo)
            continue
    return subclasses


if __name__ == "__main__":
    from testbot.utils.project_utils import *
    from testbot.resource.Resource import Resource
    from testbot.resource.pool import ResourcePool
    from testbot.resource.ModuleBase import ModuleBase
    from testbot.contrib.base.resources.ports.Port.Port import Port

    found_subclasses = get_all_subclasses_in_installed_projects(prj_setting='testbot.contrib.base.settings', parent_class=Resource)
    for name, subclass in found_subclasses.items():
        # print(name, subclass)
        pass
    print(f"base project resource subclasses: {len(found_subclasses)}")

    found_subclasses = get_all_subclasses_in_installed_projects(prj_setting='testbot.contrib.base.settings',
                                                                parent_class=ModuleBase)
    for name, subclass in found_subclasses.items():
        # print(name, subclass)
        pass
    print(f"base project module subclasses: {len(found_subclasses)}")

    found_subclasses = get_all_subclasses_in_installed_projects(prj_setting='testbot.contrib.base.settings', parent_class=ResourcePool)
    for name, subclass in found_subclasses.items():
        # print(name, subclass)
        pass
    print(f"base project pool subclasses: {len(found_subclasses)}")

    found_subclasses = get_all_subclasses_in_installed_projects(prj_setting='testbot_anker.settings', parent_class=Resource)
    for name, subclass in found_subclasses.items():
        # print(name, subclass)
        pass
    print(f"Anker project resource subclasses: {len(found_subclasses)}")

    found_subclasses = get_all_subclasses_in_installed_projects(prj_setting='testbot_anker.settings', parent_class=ModuleBase)
    for name, subclass in found_subclasses.items():
        # print(name, subclass)
        pass
    print(f"Anker project module subclasses: {len(found_subclasses)}")

    found_subclasses = get_all_subclasses_in_installed_projects(prj_setting='testbot_anker.settings',
                                                                parent_class=ResourcePool)
    for name, subclass in found_subclasses.items():
        # print(name, subclass)
        pass
    print(f"Anker project pool subclasses: {len(found_subclasses)}")

    found_subclasses = get_all_subclasses_in_installed_projects(prj_setting='testbot_oppo.settings', parent_class=Resource)
    for name, subclass in found_subclasses.items():
        # print(name, subclass)
        pass
    print(f"OPPO project resource subclasses: {len(found_subclasses)}")

    found_subclasses = get_all_subclasses_in_installed_projects(prj_setting='testbot_oppo.settings', parent_class=ModuleBase)
    for name, subclass in found_subclasses.items():
        # print(name, subclass)
        pass
    print(f"OPPO project module subclasses: {len(found_subclasses)}")

    found_subclasses = get_all_subclasses_in_installed_projects(prj_setting='testbot_oppo.settings',
                                                                parent_class=ResourcePool)
    for name, subclass in found_subclasses.items():
        print(name, subclass)
        pass
    print(f"OPPO project pool subclasses: {len(found_subclasses)}")

    found_subclasses = get_all_subclasses_in_installed_projects(prj_setting='testbot_tcl.settings', parent_class=Resource)
    for name, subclass in found_subclasses.items():
        # print(name, subclass)
        pass
    print(f"TCL project resource subclasses: {len(found_subclasses)}")

    found_subclasses = get_all_subclasses_in_installed_projects(prj_setting='testbot_tcl.settings', parent_class=ModuleBase)
    for name, subclass in found_subclasses.items():
        # print(name, subclass)
        pass
    print(f"TCL project module subclasses: {len(found_subclasses)}")

    found_subclasses = get_all_subclasses_in_installed_projects(prj_setting='testbot_tcl.settings',
                                                                parent_class=ResourcePool)
    for name, subclass in found_subclasses.items():
        # print(name, subclass)
        pass
    print(f"TCL project pool subclasses: {len(found_subclasses)}")

    found_subclasses = get_all_subclasses_in_installed_projects(prj_setting='testbot_tcl.settings', parent_class=Port)
    for name, subclass in found_subclasses.items():
        print(name, subclass)
        pass
    print(f"TCL project port subclasses: {len(found_subclasses)}")

