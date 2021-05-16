# -*- coding: utf-8 -*-
"""
    :time: 2021/1/22 11:06
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: port_scanner.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import logging
import socket
import random


class PortDetect:
    """
    扫描本机的可用端口。
    eg:
        pd = PortDetect()
        pd()
        print pd.avaliable
    ==>
        50000

    默认会从本机的50000端口开始扫描，依次递增到55000，如果发现可用的端口则把端口号赋值给
    类的成员变量avaliable，如果扫描完成后avaliable的值是0，说明所有端口都被占用了。

    也可以单独使用check_port方法，通过传入端口的方式来检查端口是否被占用。
    eg:
        pd = PortDetect()
        pd.check_port(9999)

    ==>
        True
    """

    def __init__(self, range_s=7777, range_e=8000):
        self.range_s = range_s
        self.range_e = range_e
        self.available = 0

    def check_port(self, port):
        """
        单独检查端口是否可用
        :param port: int, 端口号
        :return: Bool， True表示端口可用，False表示端口不可用
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex(("127.0.0.1", int(port)))
        if result == 0:
            return False
        else:
            return True

    def __call__(self, *args, **kwargs):
        for x in range(self.range_s, self.range_e):
            rst = self.check_port(x)
            if rst:
                self.available = x
                break
        else:
            logging.warning("all port used")

    def get_available_range(self):
        """
        获取区间内可用端口
        """
        port = random.randint(self.range_s, self.range_e)
        while not self.check_port(port):
            port = random.randint(self.range_s, self.range_e)
        return port
