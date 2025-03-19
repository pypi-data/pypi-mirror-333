#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import time
from socket import socket

import adbutils
import grpc
import serial

from testbot.app.TestApplicationBase import TESTTYPE_CHECKLIST, CheckItem
from testbot.contrib.base.resources.ports.SerialPort import SerialPort


class GRPCPort(SerialPort):
    """
    代表GRPC端口类
    """

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def initialize_resource(self, test_type, reload: bool = True):
        """
        初始化测试资源

        :return:
        :rtype:
        """
        for checkitem in TESTTYPE_CHECKLIST.get(test_type, []):
            self.logger.info(f"检查项：{checkitem.name}")
            ip_port = self.name
            if CheckItem.COMM_SERIAL_PORT_CHECK__EXIST in TESTTYPE_CHECKLIST.get(test_type, []):
                ips = self.get_remote_resource(type="AdbWirelessPort").CommSerialWrapperModule.get_ip_addresses()
                if len(ips) >= 1:
                    ip_port = f"{ips[0]:60000}"
            self.logger.info(f"检查apk是否安装，没有安装则下载并安装最新版本[未实现]")
            self.logger.info(f"检查apk是否为最新版本，不是最新版本则下载最新版本/卸载当前版本/安装最新版本[未实现]")
            self.logger.info(f"创建gRPC客户端")
            self._instance = grpc.insecure_channel(ip_port)
            self.logger.info(f"port_obj={self}")
            if not self._instance:
                raise Exception("初始化gRPC连接失败！")
            self.logger.info(f"创建gRPC心跳保活线程")
            from threading import Thread
            th = Thread(target=self._keep_grpc_alive, args=(60,), daemon=True)
            th.start()

    def _keep_grpc_alive(self, duration: int=60):
        self.logger.info("初始化心跳状态为False")
        self._alive = False
        last_ip_port = None
        res_obj = None
        for _port in getattr(self, "remote_ports", []):
            self.logger.info(f"_port={_port}")
            if _port.type == self.type:
                res_obj = _port.parent
        while True:
            try:
                self.logger.info("获取最新IP地址")
                ip_port = self.name
                ips = res_obj.CommSerialWrapperModule.get_ip_addresses()
                if len(ips) >= 1:
                    ip_port = f"{ips[0]:60000}"
                self.logger.info(f"检查gRPC端口#{ip_port}#是否存在")
                service_available = False
                s = socket.socket()
                try:
                    ip = ip_port.split(":")[0]
                    port = 60000
                    try:
                        port = int(ip_port.split(":")[1])
                    except:
                        pass
                    s.connect((ip, port))
                    service_available = True
                except socket.error as e:
                    service_available = False
                finally:
                    s.close()

                if not service_available:
                    self.logger.info(f"若gRPC端口{ip_port}不存在，则查询apk是否已安装")
                    installed = res_obj.CommSerialWrapperModule.is_grpc_apk_installed()
                    if not installed:
                        try:
                            self.logger.info(f"若apk未安装，则下载并安装最新版本apk[未实现]")
                        except:
                            self.logger.error("安装过程出现异常，则重头开始")
                            self._alive = False
                            last_ip_port = ip_port
                            continue
                    self.logger.info(f"检查gRPC服务是否已启动")
                    service_available = res_obj.CommSerialWrapperModule.is_grpc_service_up()
                    if not service_available:
                        try:
                            self.logger.info(f"若grpc服务未启动，则启动grpc服务")
                            res_obj.CommSerialWrapperModule.start_grpc_service()
                        except:
                            self.logger.error("启动过程出现异常，则重头开始")
                            self._alive = False
                            last_ip_port = ip_port
                            continue
                    self.logger.info(f"若grpc客户端为空或IP地址端口发生变化，则创建grpc客户端对象")
                if not self._instance or ip_port!=last_ip_port:
                    self.logger.info("创建gRPC客户端对象")
                    self._instance = grpc.insecure_channel(ip_port)
                    time.sleep(2)
                self.logger.info(f"调用gprc心跳接口")
                try:
                    value = res_obj.GRPCAtomModule.check_heart_beat()
                    self.logger.info(f"gRPC心跳接口返回值：{value}")
                    if value == "online":
                        self._alive = True
                    else:
                        self._alive = False
                except Exception as ex:
                    self._alive = False
                    last_ip_port = ip_port
                    # traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                    self.logger.error(str(ex))
                    continue
                last_ip_port = ip_port
                if self._alive:
                    time.sleep(duration)
            except Exception as ex:
                import traceback
                traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                self.logger.error(traceinfo)
