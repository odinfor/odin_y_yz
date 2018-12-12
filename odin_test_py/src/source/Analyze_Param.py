# -*- coding: utf-8 -*-
# @Time    : 2018-12-01 19:57
# @Author  : odin_y
# @Email   : 
# @File    : Analyze_Param.py
# @Software: PyCharm
# @Comment : 解析请求参数形式,casename<支持形式：smoke, useconfig, is_null, too_long>
#                          param<1.依赖入参:${}, 2.函数构建:=func()>

class ParamsMethod:

    __base_url = ''       # 基准url
    __base_type = False   # 基准状态,第一条case为smoke,该case设置为基准状态<base_type=True>
    __base_data = {}

    def case_method(self, url, casename, **kwargs):
        """
        # 组合casename场景下的入参
        :param base: 是否是基准入参形式
        :param casename: casename<'smoke', 'useconfig',等>
        :param kwargs:
        :return: 请求入参
        """
        data = {'error_code': 0, 'msg': 'SUCCESS', 'getdata':{}}

        # 第一条case和url改变的case且为smoke
        if url != self.__base_url and casename == 'smoke':
            self.__base_url = url         # 记录改变的url
            self.__base_type = True       # 基准状态设置为True
            self.__base_data = kwargs
            data['getdata'] = kwargs
            return data
        # url相同的case且不是smoke场景
        elif url == self.__base_url and casename != 'smoke':
            self.__base_type = False
            # useconfig:完全使用配置入参
            if casename == 'useconfig':
                data['getdata'] = kwargs
                return data
            # 设置目标参数为空
            elif '_is_null' in casename:
                # 已设置过基准值
                if self.__base_type:
                    data['getdata'] = self.__base_data
                # 没有设置基准值
                else:
                    data['getdata'] = kwargs

                if casename.strip('_is_null') in data['getdata']:
                    data['getdata'][casename.strip('_is_null')] = None
                    return data
                else:
                    data['errror_code'] = 201
                    data['msg'] = '配置参数中没有找到参数:{},无法设置该参数为空'.format(casename.strip('_is_null'))
                    return data
            # 设置目标长度
            elif '_too_long_' in casename:
                caselist = casename.split('_too_long_')
                # 已设置过基准值
                if self.__base_type:
                    data['getdata'] = self.__base_data
                # 没有设置基准值
                else:
                    data['getdata'] = kwargs

                if caselist[0] in data['getdata']:
                    try:
                        data['getdata'][caselist[0]] = data['getdata'][caselist[0]] + 's'*int(caselist[1])
                    except Exception as msg:
                        data['error_code'] = 202
                        data['msg'] = msg
                    return data
                else:
                    data['errror_code'] = 201
                    data['msg'] = '配置参数中没有找到参数:{},无法设置该参数为空'.format(casename.strip('_is_null'))
                    return data










