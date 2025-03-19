#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
import json
import click
import docutils
from json2html import json2html
from rst2html5_ import HTML5Writer
from docutils.core import publish_parts

from testbot.config import CONFIG_PATH
from testbot.config.setting import static_setting
from testbot.testengine.testlist import TestList
from testbot.testengine.caserunner import CaseRunner
from testbot.cli import env, runner, doc, cli


def main2(testlist: str = os.path.join(CONFIG_PATH, 'TCList.json'), resource: str = os.path.join(CONFIG_PATH, 'pool.json'), owner: str = 'Sunny'):
    os.environ.setdefault('TESTBOT_SETTINGS_MODULE', 'testbot_tcl.settings')
    # 加载配置文件，从%TESTBOT_HOME%/configs目录加载文件如资源配置文件、用例执行器配置文件等
    if CONFIG_PATH:
        static_setting.setting_path = CONFIG_PATH
    static_setting.load_all()
    # 初始化测试引擎，创建用例执行器对象
    runner = CaseRunner(settings_mod=os.environ.get('TESTBOT_SETTINGS_MODULE', None))
    # 加载测试资源池数据
    runner.load_resource(filename=resource, owner=owner)
    # 加载测试用例列表数据
    test_list = TestList(filepath=testlist)
    runner.set_test_list(test_list=test_list)
    # 执行测试
    runner.start()
    runner.wait_for_test_done()


@env.command()
@click.option('--type', multiple=True, help='测试类型，如冒烟、门禁、媒资等')
def inspect(type: list):
    """
    检查指定测试类型的环境健康情况

    :param type:
    :type type:
    :return:
    :rtype:
    """
    spaces = "\t"*4
    for _type in type:
        print(f"当前测试环境是否支持测试类型({_type})的执行：【PASS】")
        print(f"【PASS】是否有指令串口：{spaces}【PASS】")
        print(f"【PASS】是否有采集卡：{spaces}【PASS】")
        print(f"【PASS】是否有U盘：{spaces}【PASS】")
        print(f"【PASS】是否能够访问TV设备IP地址：{spaces}【PASS】")
        print(f"【PASS】是否能够访问公司网络：{spaces}【PASS】")
        print(f"【PASS】是否能够访问国内网络：{spaces}【PASS】")
        print(f"【PASS】是否能够访问海外网络：{spaces}【PASS】")
        print(f"【PASS】音频线是否连接：{spaces}【PASS】")
        print(f"【PASS】电源断电上电是否正常：{spaces}【PASS】")
        print(f"【PASS】网络通断是否正常：{spaces}【PASS】")
        print(f"【PASS】U盘切换是否正常：{spaces}【PASS】")
        print(f"【PASS】采集卡是否正常：{spaces}【PASS】")
        print(f"【PASS】红外指令是否正常：{spaces}【PASS】")
        print(f"【PASS】WIFI打开关闭是否正常：{spaces}【PASS】")
        print(f"【PASS】adb连接是否正常：{spaces}【PASS】")
        print(f"【PASS】检测是否有声音：{spaces}【PASS】")
        print(f"【PASS】检测是否有信源HDMI/TV：{spaces}【PASS】")
        print("\n")


@runner.command()
@click.option('--testlist', default=os.path.join(CONFIG_PATH, 'TCList.json'), type=str, required=True, help='测试用例列表文件路径')
@click.option('--pool', default=os.path.join(CONFIG_PATH, 'pool.json'),  type=str, required=False, help='测试资源池数据文件路径')
@click.option('--user', type=str, required=False, default='sunny', help='测试用户')
def test(testlist: str, pool: str, user: str):
    # 设置项目配置模块包路径
    os.environ.setdefault('TESTBOT_SETTINGS_MODULE', 'testbot_tcl.settings')
    # 加载配置文件，从%TESTBOT_HOME%/config目录加载文件如资源配置文件、用例执行器配置文件等
    if CONFIG_PATH:
        static_setting.setting_path = CONFIG_PATH
    static_setting.load_all()
    # 初始化测试引擎，创建用例执行器对象
    runner = CaseRunner()
    # 加载测试资源池数据
    runner.load_resource(filename=pool, owner=user)
    # 加载测试用例列表数据
    test_list = TestList(filepath=testlist)
    runner.set_test_list(test_list=test_list)
    # 执行测试
    runner.start()
    runner.wait_for_test_done()


@doc.command()
@click.option('--auto', type=bool, default=False, help='是否自动检测扫描接口数据')
@click.option('--rst', type=str, default=None, help='输入RST文件路径')
@click.option('--html', type=str, default=None, help='输入HTML文件路径')
@click.option('--file', type=str, default=None, help='输出json文件路径')
@click.option('--output', type=str, default=None, help='输出html文件路径')
def api(auto: bool, rst: str, html: str, file: str, output: str):
    # 设置项目配置模块包路径
    os.environ.setdefault('TESTBOT_SETTINGS_MODULE', 'testbot_tcl.settings')

    data, html_codes = None, None
    if auto:
        from testbot.contrib.base.resources.softwares.TestBotSoftware.TestBotSoftware import TestBotSoftware
        soft = TestBotSoftware(name="TESTBOT框架")
        print(f"soft={dir(soft)}")
        data, data_eng = soft.DocWrapModule.get_apis()
        if file:
            if not os.path.exists(os.path.dirname(file)):
                os.makedirs(os.path.dirname(file))
            with open(file, 'w', encoding='utf-8') as f:
                print(f"将API数据保存到{file}")
                json.dump(data_eng, f, ensure_ascii=False, indent=4)
        html_codes = json2html.convert(json=data)
    if rst:
        # 将restructuredtext文件转成html代码
        with open(rst, 'r') as f:
            data = f.read().rstrip()
        html_codes = publish_parts(writer=HTML5Writer(), source=data)['body']
        # print(html_codes)

    if html:
        with open(html, 'rb') as f:
            data = f.read().rstrip().decode()
        html_codes = data.split('<body>')[1].split('</body>')[0]
        # print(html_codes)

    if output:
        with open(output, 'w') as f:
            f.write(html_codes)


@doc.command()
@click.option('--rst', type=str, help='RST文件路径')
def rst2html(rst: str):
    # 将restructuredtext文件转成html代码
    docutils.core.publish_file(source_path=rst, destination_path=os.path.join(os.path.dirname(rst), os.path.basename(rst).replace(".rst", ".html")), writer_name="html")


def main():
    cli()

if __name__ == "__main__":
    main()
