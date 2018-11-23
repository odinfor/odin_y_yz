#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/23 上午9:51
# @Author  : odin_y
# @Site    : 
# @File    : test_TaskOS_tenantsetting.py
# @Comment : 租户管理任务配置接口

import unittest
import sys
sys.path.append('..')
from source.base import Logging, Config
from source.connect_db import DBControl
import json

class TestTenantSetting(unittest.TestCase):
    """
    租户管理任务配置测试模块
    """
    def setUp(self):
        self.config = Config()
        self.log = Logging()
        self.connectdb = DBControl()

        # 常量属性
        self.curl = 'yingzi-app-taskorchestration/api/v1/tenantsetting/task'   # 接口url
        self.success_code = 0           # 成功返回code
        self.success_msg = 'SUCCESS'    # 成功返回msg
        print('1')
        # host地址
        if self.config.operating_environment == 'test':
            self.host = self.config.test_host
        elif self.config.operating_environment == 'dev':
            self.host = self.config.dev_host
        elif self.config.operating_environment == 'local':
            self.host = self.config.local_host
        else:
            self.host = '111'

    def tearDown(self):
        self.connectdb.close_db()

    def test_systemmanage_gettasksetting(self, casename):
        """
        系统管理模块-全局配置;1.1获取任务项配置
        :return:
        """
        strtuple = (self.host, self.curl, casename)
        url = '/'.join(strtuple)
        print(url)

if __name__ == '__main__':
    run = TestTenantSetting()
    run.test_systemmanage_gettasksetting(casename='queryPage')