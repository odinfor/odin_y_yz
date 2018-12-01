# -*- coding: utf-8 -*-
# @Time    : 2018-12-01 19:57
# @Author  : odin_y
# @Email   : 
# @File    : Analyze_Param.py
# @Software: PyCharm
# @Comment : 解析请求参数形式,casename<支持形式：smoke, useconfig, is_null, too_long>
#                          param<1.依赖入参:${}, 2.函数构建:=func()>

import re


class ParamsMethod:

    base_url = ''       # 基准url
    base_type = False   # 基准状态,第一条case为smoke,该case设置为基准状态<base_type=True>

    def case_method(self, url, casename, **kwargs):
        """
        # 组合casename场景下的入参
        :param base: 是否是基准入参形式
        :param casename: casename<'smoke', 'useconfig',等>
        :param kwargs:
        :return: 请求入参
        """
        data = {}   # 初始化入参data

        # 第一条case和url改变的case且为smoke
        if url != self.base_url and casename == 'smoke':
            self.base_url = url         # 记录改变的url
            self.base_type = True       # 基准状态设置为True
            data = kwargs
            return data
        # url相同的case
        elif url == self.base_url



