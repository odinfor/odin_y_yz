#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/23 上午11:01
# @Author  : odin_y
# @Site    : 
# @File    : TaskOS_tenantsetting_test.py
# @Comment : 租户管理任务配置接口

import sys
sys.path.append('..')
# from .base import Logging, Config
from source.base import Logging, Config
import pymysql
import os
import json
import requests
import random


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
        self.db = pymysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_name)
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
        self.curl = '/api/v1/tenantsetting/task/'   # 接口url
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
                    list1 = line.split(';')
                    # 字符串转字典
                    dict1 = json.loads(list1[3])
                    list1[3] = dict1
                    config_info_list.append(list1)
                    yield list1
        # finally:
        #     runfile.close()
        # return config_info_list

    def get_data_info(self, interfacetype, casename='smoke', **kwargs):
        """
        # 生成租户管理任务配置模块各个接口不同场景下返回的入参
        :param interfacetype:接口
        :param casename:场景
        :return:接口入参
        """
        '''
        流程管理code字段码
        精准配种：ACCURATE_MATING    普通配种：NORMAL_MATING  粗放配种：ROUGH_MATING   上产床：NORMAL_PREFARROW
        背膘：NORMAL_BACKFAT   母猪淘汰：NORMAL_CULLING     母猪死亡：SOW_DEATH  小猪死亡：PIGLET_DEATH
        分娩：NORMAL_FARROW    孕检：NORMAL_PREGNANCY_DIAGNOSIS   母猪保健：SOW_HEALTH     小猪保健：PIGLET_HEALTH
        发情鉴定：NORMAL_HEAT    母猪免疫：SOW_IMMUNE     小猪免疫：PIGLET_IMMUNE      母猪断奶：NORMAL_WEANING
        仔猪断奶：PIGLET_WEANING     位置变动(转栏)：NORMAL_LOCATION_CHANGE
        '''
        # taskcode码
        task_code_dict = ('NC_WeanedWeight', 'NC_WeanedBackfat')
        businessCode = kwargs['businessCode'] if 'businessCode' in kwargs.keys() else None      # 业务编码,不传则查全部
        name = kwargs['name'] if 'name' in kwargs.keys() else None      # 名称
        page = kwargs['page'] if 'page' in kwargs.keys() else None  # 页码
        page_size = kwargs['page_size'] if 'page_size' in kwargs.keys() else 1    # 每页查询数量,默认20
        # code = kwargs['code'] if 'code' in kwargs.keys() else random.choice(code_alldict)        # 任务编码
        status = 'ENABLE' if 'status' in kwargs.keys() else 'ENABLE'    # 状态（ENABLE-启用, DISABLE-禁用）
        # 任务编码,特殊处理,支持传random随机生成code
        if 'code' in kwargs.keys():
            if kwargs['code'] == 'random':
                code = random.choice(task_code_dict)
            else:
                code = kwargs['code']
        else:
            code = None

        """# 以下字段只在2. 任务配置模块-2.4更新配置接口中用到"""
        configType = kwargs['configType'] if 'configType' in kwargs.keys() else None    # 任务项配置类型，TENANT：租户，OPERATION_UNIT:管理单元
        locationGroup = kwargs['locationGroup'] if 'locationGroup' in kwargs.keys() else None   # 任务组合规则，单个任务位置,ROOM：舍，FARM：场
        timeGroup = kwargs['timeGroup'] if 'timeGroup' in kwargs.keys() else None   # 任务组合规则，单个任务时间，DAY：同一天，HALFDAY：分上下午（半天
        taskDisplayTimeRange = kwargs['taskDisplayTimeRange'] if 'taskDisplayTimeRange' in kwargs.keys() else None  # 显示计划任务的时间范围，0：当天，1：明天，以此类推
        sowMaxCount = kwargs['sowMaxCount'] if 'sowMaxCount' in kwargs.keys() else None     # -1：不限制，1：1头母猪，以此类推
        processCode = kwargs['processCode'] if 'processCode' in kwargs.keys() else None     # 任务流程编码
        unexecuteAlarmTimeOut = kwargs['unexecuteAlarmTimeOut'] if 'unexecuteAlarmTimeOut' in kwargs.keys() else None   # 任务超过X小时未执行产生报警
        unexecuteUpgradeAlarmTimeOut = kwargs['unexecuteUpgradeAlarmTimeOut'] if 'unexecuteUpgradeAlarmTimeOut' in kwargs.keys() else None  # 任务超过X小时未执行升级报警
        executeAlarmTimeOut = kwargs['executeAlarmTimeOut'] if 'executeAlarmTimeOut' in kwargs.keys() else None     # 任务执行超过X小时未完成产生报警
        targetCodeList = kwargs['targetCodeList'] if 'targetCodeList' in kwargs.keys() else None    # 目标编码
        capabilityCodeList = kwargs['capabilityCodeList'] if 'capabilityCodeList' in kwargs.keys() else None    # 能力编码

        # 1.系统管理模块-1.1获取任务项配置接口
        if interfacetype == 'queryPage':
            data = {'code': code, 'businessCode': businessCode, 'name': name, 'status': status,
                    'page': page, 'page_size': page_size}
            if casename == 'smoke':
                pass
            # 使用配置入参
            elif casename == 'useconfig':
                data = kwargs
            # 设置入参字段为None
            elif '_is_null' in casename:
                caselist = casename.split('_is_null')
                data[caselist[0]] = None
            # 设置入参字段超长
            elif '_long_outside_' in casename:
                caselist = casename.split('_long_outside_')
                data[caselist[0]] = caselist[0] + 's'*int(caselist[1])
            self.log.info('执行:{}方法,\n当前接口类型interfacetype:{},\n测试场景interfacetype:{}\n返回入参data={}'.format(
                self.get_data_info.__name__, interfacetype, casename,  data))
            return data
        # 1.系统管理模块-1.2查询业务下拉了列表
        elif interfacetype == 'queryBusinessList':
            data = {}
            self.log.info('执行:{}方法,\n当前接口类型interfacetype:{},\n测试场景interfacetype:{}\n返回入参data={}'.format(
                self.get_data_info.__name__, interfacetype, casename,  data))
        # 1.系统管理模块-1.3更新任务状态接口
        elif interfacetype == 'updateStatus':
            data = {'code': 'BC_Insemination', 'status': status}
            if casename == 'smoke':
                pass
            # 使用配置入参
            elif casename == 'useconfig':
                data = kwargs
                # 设置入参字段为None
            elif '_is_null' in casename:
                caselist = casename.split('_is_null')
                data[caselist[0]] = None
            # 设置入参字段超长
            elif '_long_outside_' in casename:
                caselist = casename.split('_long_outside_')
                data[caselist[0]] = caselist[0] + 's'*int(caselist[1])
            self.log.info('执行:{}方法,\n当前接口类型interfacetype:{},\n测试场景interfacetype:{}\n返回入参data={}'.format(
                self.get_data_info.__name__, interfacetype, casename,  data))
            return data
        # 1.系统管理模块-1.4任务项配置恢复默认
        elif interfacetype == 'resetStatus':
            data = {}
            self.log.info('执行:{}方法,\n当前接口类型interfacetype:{},\n测试场景interfacetype:{}\n返回入参data={}'.format(
                self.get_data_info.__name__, interfacetype, casename,  data))
            return data

        # 2.任务配置模块-2.1获取配置任务项列表
        elif interfacetype == 'queryEnabledList':
            data = {}
            self.log.info('执行:{}方法,\n当前接口类型interfacetype:{},\n测试场景interfacetype:{}\n返回入参data={}'.format(
                self.get_data_info.__name__, interfacetype, casename,  data))
            return data
        # 2.任务配置模块-2.2获取任务配置内容模板
        elif interfacetype == 'queryConfigTemplate':
            data = {'code': code}
            if casename == 'smoke':
                pass
            # 使用配置入参
            elif casename == 'useconfig':
                data = kwargs
            elif casename == 'code_is_null':
                data['code'] = None
            elif '_long_outside_' in casename:
                caselist = casename.split('_long_outside_')
                data[caselist[0]] = caselist[0] + 's'*int(caselist[1])
            self.log.info('执行:{}方法,\n当前接口类型interfacetype:{},\n测试场景interfacetype:{}\n返回入参data={}'.format(
                self.get_data_info.__name__, interfacetype, casename,  data))
            return data
        # 2.任务配置模块-2.3获取任务配置内容
        elif interfacetype == 'queryConfig':
            data = {'code': code}
            if casename == 'smoke':
                pass
            # 使用配置入参
            elif casename == 'useconfig':
                data = kwargs
            elif casename == 'code_is_null':
                data['code'] = None
            elif '_long_outside_' in casename:
                caselist = casename.split('_long_outside_')
                data[caselist[0]] = caselist[0] + 's'*int(caselist[1])
            self.log.info('执行:{}方法,\n当前接口类型interfacetype:{},\n测试场景interfacetype:{}\n返回入参data={}'.format(
                self.get_data_info.__name__, interfacetype, casename,  data))
            return data
        # 2.任务配置模块-2.4更新配置
        elif interfacetype == 'updateConfig':
            data = {'code': code, 'configType': configType, 'locationGroup': locationGroup, 'timeGroup': timeGroup,
                    'taskDisplayTimeRange': taskDisplayTimeRange, 'sowMaxCount': sowMaxCount, 'processCode': processCode,
                    'unexecuteAlarmTimeOut': unexecuteAlarmTimeOut, 'unexecuteUpgradeAlarmTimeOut': unexecuteUpgradeAlarmTimeOut,
                    'executeAlarmTimeOut': executeAlarmTimeOut, 'targetCodeList': targetCodeList,
                    'capabilityCodeList': capabilityCodeList}
            if casename == 'smoke':
                pass
            # 使用配置入参
            elif casename == 'useconfig':
                data = kwargs
            elif '_is_null' in casename:
                caselist = casename.split('_is_null')
                data[caselist[0]] = None
            elif '_long_outside_' in casename:
                caselist = casename.split('_long_outside_')
                data[caselist[0]] = caselist[0] + 's'*int(caselist[1])
            self.log.info('执行:{}方法,\n当前接口类型interfacetype:{},\n测试场景interfacetype:{}\n返回入参data={}'.format(
                self.get_data_info.__name__, interfacetype, casename,  data))
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

    def run_testcase(self, urlpart, data, interfacetype='queryPage', casename='smoke', needoperationUnitld=False, comment='这是默认测试场景说明'):
        """
        # 调用测试接口请求
        :param interfacetype:被测接口
        :param data:入参
        :param needoperationUnitld:header头是否需要获取operationUnitId
        :return:
        """
        # 当前执行任务说明
        self.log.info('执行用例:{}'.format(comment))
        # 组成请求头
        getauth = self.login_yunxi()
        headers = {'auth': getauth, 'Content-Type': 'application/json'}
        if needoperationUnitld:
            getoperationUnitId = self.get_operationUnitId()
            headers['operationUnitId'] = getoperationUnitId

        # 请求url
        url = 'http://{}{}{}'.format(self.host, urlpart, interfacetype)
        # 发送接口请求
        rsp = requests.post(url=url, data=json.dumps(data), headers=headers)
        try:
            rsp.raise_for_status()
        except Exception as e:
            raise e
        else:
            self.log.info('执行{}, \n接口请求地址:{},\n请求入参data:{},\n接口返回rsp={}'.format(self.run_testcase.__name__,
                                                                           url, data, rsp.json()))
            if casename == 'smoke' or casename == 'useconfig':
                assert rsp.json()['error_code'] == 0
                assert rsp.json()['error_msg'] == 'SUCCESS' or rsp.json()['error_msg'] == 'success'
            elif casename.find('_long_outside_') > 0:
                assert rsp.json()['error_code'] == 30100
            elif casename.find('_is_null') > 0:
                assert rsp.json()['error_code'] == 30100


def cut_off_rule(func):
    log = Logging()

    def warper():
        log.info('='*32 + '这是分界线' + '='*32)
        log.info('*'*30 + '执行:{}方法'.format(main.__name__) + '*'*30)
        func()
        log.info('='*32 + '这是分界线' + '='*32)
        log.info('*'*30 + '结束:{}方法'.format(main.__name__) + '*'*30)
    return warper


@cut_off_rule
def main():
    """# 运行套件函数"""
    # log = Logging()
    run_test = TestTenantSetting()
    # 获取system_manage_run.txt文件配置列表
    config_info = run_test.get_run_config_info()

    # 获取headers需要字段
    auth = run_test.login_yunxi()
    operationUnitId = run_test.get_operationUnitId()
    # 批量执行
    for info in config_info:
        # log.info('='*30 + '这是分界线' + '*'*30)
        # log.info('*'*30 + '执行:{}方法'.format(main.__name__) + '*'*30)
        # 组装不同接口类型不同测试场景下的data
        data = run_test.get_data_info(interfacetype=info[1], casename=info[2], **info[3])
        # 调用接口请求
        run_test.run_testcase(urlpart=info[0], data=data, interfacetype=info[1], casename=info[2], comment=info[4])




if __name__ == '__main__':
    main()
