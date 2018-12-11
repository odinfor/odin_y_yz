#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/23 上午11:01
# @Author  : odin_y
# @Site    :
# @File    : TaskOS_tenantsetting_test.py
# @Comment : 租户管理任务配置接口

import pymysql
import os
import json
import requests
import random
import threading
from functools import wraps
import sys
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
sys.path.append("..")
from base import Logging, Config, UseingExcel
import Table_To_SQL
import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta


def cut_off_rule(func):
    """# main方法装饰器"""
    log = Logging()
    def warper():
        log.info('='*32 + '这是分界线' + '='*32)
        log.info('*'*30 + '执行:{}方法'.format(main.__name__) + '*'*30)
        func()
        log.info('='*32 + '这是分界线' + '='*32)
        log.info('*'*30 + '结束:{}方法'.format(main.__name__) + '*'*30 + '\n')
    return warper


def assertFail(function):
    """# 执行run_testcase请求装饰器"""
    log = Logging()
    @wraps(function)
    def wrapper(self, *args, **kwargs):

        try:
            function(self, *args, **kwargs)
        except Exception as msg:
            log.error('case error\n')
        else:
            log.info('case pass\n')
    return wrapper


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
        self.error_code = 0           # 返回code
        self.error_msg = 'SUCCESS'    # 返回msg
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
        :return:生成器,返回需要执行的用例场景
        """
        file = os.path.join(self.config.refdata_dir, 'system_manage_run.txt')
        try:
            with open(file, 'r') as runfile:
                info = runfile.read().splitlines()
        except IOError:
            raise IOError
        else:
            for line in info:
                if not line.startswith('#'):
                    # 拆分字符串
                    list1 = line.split(';')
                    # 字符串转字典
                    dict1 = json.loads(list1[3])
                    list1[3] = dict1
                    yield list1

    def get_data_info(self, interfacetype, casename='smoke', **kwargs):
        """
        # 生成租户管理任务配置模块各个接口不同场景下返回的入参
        :param interfacetype:接口
        :param casename:场景
        :param kwargs:config入参
        :return:接口入参
        """
        # taskcode码
        task_code_dict = ('NC_WeanedWeight', 'NC_WeanedBackfat')
        businessCode = kwargs['businessCode'] if 'businessCode' in kwargs.keys() else None      # 业务编码,不传则查全部
        name = kwargs['name'] if 'name' in kwargs.keys() else None      # 名称
        page = kwargs['page'] if 'page' in kwargs.keys() else None  # 页码
        page_size = kwargs['page_size'] if 'page_size' in kwargs.keys() else 1    # 每页查询数量,默认20
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
        :return:operationUnitId
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

    # @assertFail
    def run_testcase(self, urlpart, data, interfacetype='queryPage', casename='smoke', needoperationUnitld=False,
                     comment='这是默认测试场景说明'):
        """
        # 调用测试接口请求
        :param interfacetype:被测接口
        :param data:入参
        :param casename:接口场景<smoke, *_is_null, *_long_outside_*, usecofig>
        :param needoperationUnitld:header头是否需要获取operationUnitId
        :return:接口响应返回
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
        rsp_json = rsp.json()
        self.log.info('执行{}, \n接口请求地址:{},\n请求入参data:{},\n接口返回rsp={}'.format(self.run_testcase.__name__,
                                                                            url, data, rsp.json()))
        try:
            rsp.raise_for_status()
        except Exception as e:
            raise e
        else:
            if casename == 'smoke' or casename == 'useconfig':
                self.error_code = rsp_json['error_code']
                self.error_msg = rsp_json['error_msg']
                if rsp_json['error_code'] == 0 and (rsp_json['error_msg'] == 'SUCCESS' or rsp_json['error_msg'] == 'success'):
                    return True, rsp_json
                else:
                    self.error_code = rsp_json['error_code']
                    self.error_msg = rsp_json['error_msg']
                    return False, rsp_json
            elif '_long_outside_' in casename:
                if rsp.json()['error_code'] == 30100:
                    self.error_code = rsp_json['error_code']
                    self.error_msg = rsp_json['error_msg']
                    return True, rsp_json
                else:
                    self.error_code = rsp_json['error_code']
                    self.error_msg = rsp_json['error_msg']
                    return False, rsp_json
            elif '_is_null' in casename:
                if rsp.json()['error_code'] == 30100:
                    self.error_code = rsp_json['error_code']
                    self.error_msg = rsp_json['error_msg']
                    return True, rsp_json
                else:
                    self.error_code = rsp_json['error_code']
                    self.error_msg = rsp_json['error_msg']
                    return False, rsp_json


@cut_off_rule
def main():
    """# 运行套件函数"""
    # log = Logging()
    run_test = TestTenantSetting()
    # 获取system_manage_run.txt文件配置列表
    config_info = run_test.get_run_config_info()
    # excel方法类
    use_excel = UseingExcel()

    # 获取headers需要字段
    auth = run_test.login_yunxi()
    operationUnitId = run_test.get_operationUnitId()

    # 记录字段
    # list_line_case = []     # 单个case结果记录
    list_all_cases = []     # 所有case结果记录

    #======
    casename_list = []
    comment_list = []
    reqdata_list = []
    rspdata_list = []
    rsp_data = []
    is_pass_list = []

    # 批量执行
    for info in config_info:
        # log.info('='*30 + '这是分界线' + '*'*30)
        # log.info('*'*30 + '执行:{}方法'.format(main.__name__) + '*'*30)
        # 组装不同接口类型不同测试场景下的data
        data = run_test.get_data_info(interfacetype=info[1], casename=info[2], **info[3])
        # 调用接口请求
        rsp = run_test.run_testcase(urlpart=info[0], data=data, interfacetype=info[1], casename=info[2], comment=info[4])

        casename_list.append(info[2])
        comment_list.append(info[4])
        reqdata_list.append(data)
        rspdata_list.append(rsp[1])
        is_pass_list.append(rsp[0])
    # 写入文件
    use_excel.api_result_excel(casename=casename_list, comment=comment_list, data_request=reqdata_list,
                               data_return=rspdata_list,is_pass=is_pass_list, len=len(casename_list))


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:  # 添加了对datetime的处理
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.date):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.timedelta):
                        fields[field] = (datetime.datetime.min + data).time().isoformat()
                    else:
                        fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


class NewRequests:

    _base_data = {}

    def __init__(self):
        self.sqldb = Table_To_SQL.SqlalchemyControlDB()
        self.sqldb.connect_db()
        self.params_once_table = Table_To_SQL.ParamsOnceTable
        self.check_once_table = Table_To_SQL.CheckOnceTable
        self.params_all_table = Table_To_SQL.ParamsAllTable
        self.check_all_table = Table_To_SQL.CheckAllTable
        self.rsp_table = Table_To_SQL.RspTable

        self.login_result = ''
        self.config = Config()
        self.log = Logging()

    def get_all_params_caseID(self, type='once'):
        if type == 'once':
            caseID = self.sqldb.session.query(self.params_once_table.caseID).all()

            for case in caseID:
                line = self.sqldb.session.query(self.params_once_table).filter(self.params_once_table.caseID == case[0]).all()
            return caseID
        elif type == 'all':
            caseID = self.sqldb.session.query(self.params_all_table.caseID).all()
            return caseID

    def get_once_url(self):
        """
        # 获取params_once_table表url
        :return: 生成器返回
        """
        cases = self.get_all_params_caseID()
        for case in cases:
            db_host = self.sqldb.session.query(self.params_once_table.host).filter(self.params_once_table.caseID == case[0]).all()
            db_url = self.sqldb.session.query(self.params_once_table.url).filter(self.params_once_table.caseID == case[0]).all()

            url = '{}/{}'.format(db_host[0][0], db_url[0][0])
            yield url

    def get_all_url(self):
        """
        # 获取params_all_table表url
        :return: 生成器返回
        """
        cases = self.get_all_params_caseID()
        for case in cases:
            db_host = self.sqldb.session.query(self.params_all_table.host).filter(self.params_all_table.caseID == case[0]).all()
            db_url = self.sqldb.session.query(self.params_all_table.url).filter(self.params_all_table.caseID == case[0]).all()
            # host有数据使用该host地址
            if db_host:
                if db_host[0][0]:
                    url = '{}/{}'.format(db_host[0][0], db_url[0][0])
                else:
                    url = 'http://127.0.0.1/{}'.format(db_host[0][0], db_url[0][0])
            # 没有使用config文件配置地址
            else:
                if self.config.operating_environment == 'test':
                    url = '{}/{}'.format(db_host, self.config.test_host)
                elif self.config.operating_environment == 'dev':
                    url = '{}/{}'.format(db_host, self.config.dev_host)
                elif self.config.operating_environment == 'local':
                    url = '{}/{}'.format(db_host, self.config.local_host)
            yield url

    def run_login(self):
        """# 5分钟重新获取一次auth"""
        global timer
        timer = threading.Timer(300, self.login_yunxi)

    def login_yunxi(self):
        """
        # 登录云徙
        @:return auth
        """
        rspdata = {'error_code': 10000, 'error_msg': '登录接口响应返回异常', 'auth': ''}
        url = self.config.login_url
        headers = {'Content-Type': 'application/json;charset=UTF-8'}
        data = {'username': self.config.login_username, 'userPassword': self.config.login_pwd}
        try:
            rsp = requests.post(url, data, headers)
            rsp.raise_for_status()
        except Exception as e:
            print("云徙登录响应返回异常:{}".format(e))
            return rspdata
        else:
            if rsp.json()['error_code'] == 0:
                rspdata['error_code'] = rsp.json()['error_code']
                rspdata['error_code'] = rsp.json()['error_msg']
                rspdata['auth'] = rsp.json()['data']['auth']
                return rspdata
            else:
                rspdata['error_code'] = rsp.json()['error_code']
                rspdata['error_code'] = rsp.json()['error_msg']
                return rspdata

    def send_requests(self, auth, type='post'):
        """
        # 调用接口请求
        :param type:请求方式
        :return:
        """
        caseidlist = self.get_all_params_caseID()
        headers = {'auth': auth, 'Content-Type': 'application/json'}

        for caseid in caseidlist:
            error_code = 0  # 请求错误码<请求错误码范围100~109>,成功为0
            error_msg = 'SUCESS'  # 请求返回msg,成功为:'SUCESS'
            is_pass = True  # 通过结果
            log = []

            casequery = self.sqldb.session.query(self.params_once_table).filter(self.params_once_table.caseID == caseid[0]).all()
            # query转dict
            casejson = json.loads(json.dumps(casequery[0], cls=AlchemyEncoder))

            urladdress = 'http://{}/{}'.format(casejson['host'], casejson['url'])   # 请求地址

            params_data = {}       #入参
            # 取参数字段,去空
            for k, v in casejson.items():
                if 'params_' in k and v != '':
                    params_data[k] = v
            # 组装参数
            params_key_list = []
            params_value_list = []
            params_data_value_list = params_data.values()
            for value in params_data_value_list:
                newlist = value.split('=')
                params_key_list.append(newlist[0])
                params_value_list.append(newlist[1])
            # 组装完成的入参
            input_dict = dict(zip(params_key_list, params_value_list))
            print('请求入参input_dict={}'.format(input_dict))

            if casejson['run']:
                try:
                    # 发送请求
                    if type == 'post':
                        rsp = requests.post(url=urladdress, data=json.dumps(input_dict), headers=headers, timeout=10)
                    elif type == 'get':
                        rsp = requests.get(url=urladdress, params=input_dict, headers=headers, timeout=10)
                    rsp_json = rsp.json()
                    print('rsp_json={}'.format(rsp_json))
                    rsp.raise_for_status()
                # HTTP错误
                except requests.exceptions.HTTPError as msg:
                    error_code = 100
                    error_msg = msg
                    rlt_data = {'caseID': caseid[0], 'error_code': error_code, 'error_msg': error_msg, 'rsp_data': rsp_json,
                            'is_pass': is_pass}
                    yield rlt_data
                # 连接超时
                except requests.exceptions.ConnectTimeout as msg:
                    error_code = 101
                    error_msg = msg
                    rlt_data = {'caseID': caseid[0], 'error_code': error_code, 'error_msg': error_msg, 'rsp_data': rsp_json,
                            'is_pass': is_pass}
                    yield rlt_data
                # 连接错误
                except requests.exceptions.ConnectionError as msg:
                    error_code = 102
                    error_msg = msg
                    rlt_data = {'caseID': caseid[0], 'error_code': error_code, 'error_msg': error_msg, 'rsp_data': rsp_json,
                            'is_pass': is_pass}
                    yield rlt_data
                # 其他异常
                except Exception as msg:
                    error_code = 103
                    error_msg = msg
                    rlt_data = {'caseID': caseid[0], 'error_code': error_code, 'error_msg': error_msg, 'rsp_data': rsp_json,
                            'is_pass': is_pass}
                    yield rlt_data
                else:
                    # 组装返回data
                    rlt_data = {'caseID': caseid[0], 'error_code': error_code, 'error_msg': error_msg, 'rsp_data': rsp_json}

                    # 校验表
                    checkquery = self.sqldb.session.query(self.check_once_table).filter(self.check_once_table.caseID == caseid[0]).all()
                    checkjson = json.loads(json.dumps(checkquery[0], cls=AlchemyEncoder))

                    check_data = {'code': checkjson['error_code']}  # 校验
                    # 取参数字段,去空
                    for k, v in checkjson.items():
                        if 'check_' in k and v != '':
                            check_data[k] = v
                    if len(check_data) > 1:
                        # 组装check_table需要校验内容
                        check_key_list = []
                        check_value_list = []
                        for value in check_data:
                            check_newlist = value.split('=')
                            check_key_list.append(check_newlist[0])
                            check_value_list.append(check_newlist[1])
                        # 组装完成的需要检验内容
                        check_dict = dict(zip(check_key_list, check_value_list))
                    else:
                        check_dict = {}

                    if rlt_data['rsp_data']['error_code'] == checkjson['error_code']:
                        log.append('响应返回code={}与期望一致;'.format(rlt_data['error_code']))
                        if not check_dict:
                            is_pass = True
                            log.append('校验参数列表为空,结束参数校验;'.format(
                                rlt_data['rsp_data']['error_code'], checkjson['error_code']))
                            back_data = {'caseID': caseid[0], 'casename': casejson['casename'],
                                         'comment': casejson['comment'], 'rsp': rlt_data['rsp_data'], 'is_pass': is_pass,
                                         'log': log}
                            yield back_data
                        for check_key_1, check_value_1 in check_dict:
                            checktime = 0
                            # 响应返回data结构体为字典类型
                            if isinstance(rlt_data['rsp_data']['data'], dict):
                                if check_key_1 in rlt_data['rsp_data']['data'].keys():
                                    if rlt_data['data'][check_key_1] == check_value_1:
                                        log.append('响应返回参数:{}的值=预期值:{};'.format(check_key_1, check_value_1))
                                        checktime += 1
                                        if checktime == len(rlt_data.keys()):
                                            log.append('所有校验完成;')
                                            back_data = {'caseID': caseid[0], 'casename': casejson['casename'],
                                                         'comment': casejson['comment'], 'rsp': rlt_data['rsp_data'], 'is_pass': is_pass,
                                                         'log': log}
                                            yield back_data
                                    else:
                                        log.append('响应返回参数:{}的值!=预期值:{}.响应返回参数的值为:{};'.format(check_key_1,
                                                                                             check_value_1,
                                                                                             rlt_data['rsp_data'][check_key_1]))
                                        is_pass = False
                                        back_data = {'caseID': caseid[0], 'casename': casejson['casename'],
                                                     'comment': casejson['comment'], 'rsp': rlt_data['rsp_data'], 'is_pass': is_pass,
                                                     'log': log}
                                        yield back_data
                                else:
                                    log.append('接口响应返回中未找到预期参数:{};'.format(check_key_1))
                                    is_pass = False
                                    back_data = {'caseID': caseid[0], 'casename': casejson['casename'],
                                                 'comment': casejson['comment'], 'rsp': rlt_data['rsp_data'], 'is_pass': is_pass,
                                                 'log': log}
                                    yield back_data
                            # 响应返回data结构体为列表类型
                            elif isinstance(rlt_data['rsp_data']['data'], list):
                                print('列表类型暂无校验')
                                pass
                    else:
                        is_pass = False
                        log.append('响应返回code={}与期望code={}不相符,结束参数校验;'.format(rlt_data['rsp_data']['error_code'], checkjson['error_code']))
                        back_data = {'caseID': caseid[0], 'casename': casejson['casename'],
                                     'comment': casejson['comment'], 'rsp': rlt_data['rsp_data'], 'is_pass': is_pass,
                                     'log': log}
                        yield back_data

    def record_rsp_to_db(self, data):
        """
        # 响应校验返回入库
        :param data:send_requests方法返回
        :return:
        """
        # data数据类型转化
        data['rsp'] = json.dumps(data['rsp'], ensure_ascii=False)
        data['log'] = str(data['log'])[1:-1]

        rsp_obj = self.rsp_table(**data)
        try:
            self.sqldb.session.add(rsp_obj)
        except:
            self.sqldb.session.roll_back()
        else:
            self.sqldb.session.commit()

    def final_done(self):
        self.sqldb.close_db()


if __name__ == '__main__':
    # main()
    test = NewRequests()
    #test.get_all_params_caseID()
    # once执行,清空开始内容和返回表
    test.sqldb.delete_table('rsp_table')
    test.sqldb.delete_table('params_once_table')
    test.sqldb.delete_table('check_once_table')
    # 配置文件写入库
    test.sqldb.insertdict()

    login_rsp = test.login_yunxi()
    if login_rsp['error_code'] == 0:
        # 调用请求
        data = test.send_requests(auth=login_rsp['auth'])
        for line in data:
            # 请求结果写入库
            test.record_rsp_to_db(line)
    else:
        data1 = {'caseID': 1, 'casename': '', 'comment': '', 'rsp': login_rsp, 'is_pass': False, 'log': login_rsp['error_msg']}
        test.record_rsp_to_db(data1)
    # 结束关闭session连接
    test.final_done()
