# -*- coding: utf-8 -*-
# @Author: maoyongfan
# @email: maoyongfan@163.com
# @Date: 2025/2/26 21:19
from pybaselib.utils.net import is_valid_ip
from pybaselib.utils import ParameterError
from pybaselib.utils.interface import IntType as intType
from functools import reduce


def int_to_hex_string(int_value, length=2):
    return f"{int_value:0{length}X}"


def ip_to_hex_string(ip_value):
    hex_string = ""
    if is_valid_ip(ip_value):
        for item in ip_value.split("."):
            hex_string += f"{int(item):02X}"
        return hex_string
    else:
        raise ParameterError("无效的IP地址")


def int_to_binary_string(int_value, length, reversal=True):
    binary_string = format(int_value, f'0{length}b')
    if reversal:
        return reduce(lambda x, y: y + x, binary_string)
    else:
        return binary_string


class IntType:
    int_to_hex_string = staticmethod(int_to_hex_string)
    int_to_binary_string = staticmethod(int_to_binary_string)
    ip_to_hex_string = staticmethod(ip_to_hex_string)


if __name__ == '__main__':
    print(int_to_hex_string(38393, 5))
    # print(ip_to_hex_string("192.168.1.122"))
    # print(int_to_binary_string(30, 15))
