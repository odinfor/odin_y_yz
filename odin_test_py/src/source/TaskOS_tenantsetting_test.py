#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/23 上午11:01
# @Author  : odin_y
# @Site    : 
# @File    : TaskOS_tenantsetting_test.py
# @Comment : 租户管理任务配置接口

import sys
sys.path.append('..')
from source.base import Logging, Config
import pymysql
import os
import json
import requests



class PySQLDB():
    """
    # db操作
    """
    def __init__(self):
        """
        # 连接db
        :return:
        """
        config = Config()
        # db_adress = 'mysql+pymysql://yz_dev_taskorchestration:n2Q0eclF2CJFtFMr@172.18.100.142:3306/yz_dev_taskorchestration'
        # # 初始化连接mysqldb, 不显示sql logging
        # self.engine = create_engine(db_adress, echo=False)  # 建立数据库
        # db_session = sessionmaker(bind=self.engine)  # 创建连接
        # self.session = db_session()
        if config.operating_environment == 'test':
            db_host = config.db_test_host
            db_user = config.db_test_username
            db_password = config.db_test_password
            db_name = config.db_test_name
        elif config.operating_environment == 'dev':
            db_host = config.db_dev_host
            db_user = config.db_dev_username
            db_password = config.db_dev_password
            db_name = config.db_dev_name
        elif config.operating_environment == 'local':
            db_host = config.db_local_host
            db_user = config.db_local_username
            db_password = config.db_local_password
            db_name = config.db_local_name
        else:
            raise Exception('config.ini文件operating_environment字段配置错误')
        # self.dbinfo = get_db_info()
        # 使用pymysql创建连接
        self.db = pymysql.connect(host=db_host, port=3306, user=db_user,password=db_password, db=db_name)
        # self.db = pymysql.connect(host='172.18.100.142', port=3306, user='yz_dev_taskorchestration', password='n2Q0eclF2CJFtFMr', db='yz_dev_taskorchestration')
        # 创建游标
        self.cursor = self.db.cursor()


    def docursor(self, sql):
        """# 游标执行sql"""
        try:
            rst = self.cursor.execute(sql)
        except Exception as e:
            raise e
        else:
            return rst

    def fetchall(self, sql):
        """# 查询sql"""
        try:
            self.cursor.execute(sql)
            rst_all = self.cursor.fetchall()    # 获取所有结果
        except Exception as e:
            raise e
        else:
            return rst_all

    def cleardb(self, sql):
        """# 删除操作"""
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.db.rollback()
            raise e
        else:
            self.db.commit()
        finally:
            self.closedb()

    def closedb(self):
        """# 断开db连接"""
        # self.session.close()
        self.cursor.close()
        self.db.close()


class TestTenantSetting():
    """
    租户管理任务配置测试模块
    """
    def __init__(self):
        self.config = Config()
        self.log = Logging()
        self.pysql = PySQLDB()

        # 常量属性
        self.curl = '/yingzi-app-taskorchestration/api/v1/tenantsetting/task/'   # 接口url
        self.success_code = 0           # 成功返回code
        self.success_msg = 'SUCCESS'    # 成功返回msg
        # host地址
        if self.config.operating_environment == 'test':
            self.host = self.config.test_host
        elif self.config.operating_environment == 'dev':
            self.host = self.config.dev_host
        elif self.config.operating_environment == 'local':
            self.host = self.config.local_host
        else:
            self.host = '111'

    def get_run_config_info(self):
        """
        # 读取system_manage_run.txt文件,#开头的行过滤
        :return:返回需要执行的用例场景
        """
        file = os.path.join(self.config.refdata_dir, 'system_manage_run.txt')
        try:
            with open(file, 'r') as runfile:
                info = runfile.read().splitlines()
        except IOError:
            raise IOError
        else:
            config_info_list = []
            for line in info:
                if not line.startswith('#'):
                    # 拆分字符串
                    list1 = line.split(',')
                    # 字符串转字典
                    dict1 = json.loads(list1[2])
                    list1[2] = dict1
                    config_info_list.append(list1)
        finally:
            runfile.close()
        return config_info_list

    def get_data_info(self, interfacetype, casename='smoke', **kwargs):
        """
        # 生成租户管理任务配置模块各个接口不同场景下返回的入参
        :param interfacetype:接口
        :param casename:场景
        :return:接口入参
        """
        page = kwargs['page'] if 'page' in kwargs.keys() else None  # 页码
        page_size = kwargs['page_size'] if 'page_size' in kwargs.keys() else None    # 每页查询数量,默认20
        code = kwargs['code'] if 'code' in kwargs.keys() else None        # 任务编码
        status = 'ENABLE' if 'status' in kwargs.keys() else None    # 状态（ENABLE-启用, DISABLE-禁用）

        # 1.系统管理模块-1.1获取任务项配置接口
        if interfacetype == 'queryPage':
            data = {'page': page, 'page_size': page_size}
            if casename == 'smoke':
                pass
            elif casename == 'page_is_null':
                data['page'] = None
            elif casename == 'page_size_is_null':
                data['page_size'] = None
            return data
        # 1.系统管理模块-1.2更新任务状态接口
        elif interfacetype == 'updateStatus':
            data = {'code': code, 'status': status}
            if casename == 'smoke':
                pass
            elif casename == 'code_is_null':
                data['code'] = None
            elif casename == 'status_is_null':
                data['status'] = None
            return data
        # 2.任务配置模块-2.1获取配置任务项列表
        elif interfacetype =='queryEnabledList':
            data = {}
            return data
        # 2.任务配置模块-2.2获取任务配置内容模板
        elif interfacetype == 'getTemplate':
            data = {'code': code}
            if casename == 'smoke':
                pass
            elif casename == 'code_is_null':
                data['code'] = None
            return data
        # 2.任务配置模块-2.3获取任务配置内容
        elif interfacetype == 'getConfig':
            data = {'code': code}
            if casename == 'smoke':
                pass
            elif casename == 'code_is_null':
                data['code'] = None
            return data

    def login_yunxi(self):
        """
        # 登录云徙
        @:return auth
        """
        url = 'http://test.yingzi.com//huieryun-identity/api/v1/auth/yingzi/user/breeding/auth'
        headers = {'Content-Type': 'x-www-form-urlencoded'}
        data = {'userCode': 'jgs2',
                'userPassword': 'eXo4ODg4ODg',
                'loginType': 'nameMobile',
                'trench': 'pc',
                'loginFlag': 1,
                'timestamp': 1541574621568}

        rsp = requests.post(url, data, headers)
        try:
            rsp.raise_for_status()
        except Exception as e:
            print("云徙登录响应返回异常:{}".format(e))
        else:
            auth = rsp.json()['data']['auth']
            return auth

    def get_operationUnitId(self):
        """
        # 调用人力中心接口,获取operationUnitId
        :return:
        """
        operationUnitId = None
        return operationUnitId

    # def test_systemmanage_gettasksetting(self, casename):
    #     """
    #     系统管理模块-全局配置;1.1获取任务项配置
    #     :return:
    #     """
    #     strtuple = ('http://', self.host, self.curl, casename)
    #     url = ''.join(strtuple)

    def run_testcase(self, interfacetype='queryPage', casename='smoke', needoperationUnitld=False):
        """
        # 调用测试接口请求
        :param interfacetype:被测接口
        :param casename:测试场景
        :param needoperationUnitld:header头是否需要获取operationUnitId
        :return:
        """
        # 组成请求头
        getauth = self.login_yunxi()
        headers = {'auth': getauth}
        if needoperationUnitld:
            getoperationUnitId = self.get_operationUnitId()
            headers['operationUnitId'] = getoperationUnitId

        # 请求data
        data = self.get_data_info(interfacetype, casename)
        # 请求url
        url = 'http://{}{}{}'.format(self.host, self.curl, interfacetype)
        # 发送接口请求
        rsp = requests.post(url=url, data=data, headers=headers)
        try:
            rsp.raise_for_status()
        except Exception as e:
            raise e
        else:
            assert rsp.json()['error_code'] == 0
            assert rsp.json()['error_msg'] == 'SUCCESS'



def main():
    """# 运行套件函数"""
    run_test = TestTenantSetting()
    # 获取system_manage_run.txt文件配置列表
    config_info = run_test.get_run_config_info()
    # 获取headers需要字段
    auth = run_test.login_yunxi()
    operationUnitId = run_test.get_operationUnitId()
    # 批量执行
    for info in config_info:
        # 组装不同接口类型不同测试场景下的data
        data = run_test.get_data_info(interfacetype=info[0], casename=info[1], **info[2])
        # 调用接口请求
        run_test.run_testcase(interfacetype=info[0], casename=info[1], **data)



if __name__ == '__main__':
    main()