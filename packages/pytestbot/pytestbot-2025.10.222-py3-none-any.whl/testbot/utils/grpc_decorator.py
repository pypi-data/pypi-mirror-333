#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import time
import functools


def set_as_grpc_api(*args, **kwargs):
    """
    设置接口方法为gRPC接口，在调用被装饰的gRPC接口之前，检查gRPC连接保活状态，若在默认60以内gRPC包或状态仍然为False，则直接调用gRPC接口
    """

    timeout: int = kwargs.get("timeout", 60)
    duration: int = kwargs.get("duration", 3)
    def decorator(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            self.logger.info(f"在调用方法{self.__class__.__name__}.{func.__name__}之前，做gRPC保活状态检查")
            for name, port in self.resource.ports.items():
                self.logger.info(f"name, port={name}, {port}")
                if port.type == "GRPCPort":
                    for _port in port.remote_ports:
                        if _port.type == "GRPCPort":
                            start_ts = time.time()
                            while time.time() - start_ts <= timeout:
                                if not _port._alive:
                                    self.logger.info(f"gRPC保活状态为False，等待{duration}秒后重新检查")
                                    time.sleep(duration)
                                else:
                                    self.logger.info(f"gRPC保活状态为True，可以放心调用gRPC接口")
                                    break
            return func(self, *args, **kwargs)
        return wrap
    return decorator
