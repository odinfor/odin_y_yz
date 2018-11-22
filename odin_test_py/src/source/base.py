#-*- coding:utf-8 -*-
import os
import sys
import configparser
import xlrd, xlwt, xlutils
import time
import logging
import requests
from kazoo.client import KazooClient
import json
import pymysql
import platform

'''
Created on 2018-11-11

@author:odin_y
'''

class Config():
    """
    # 读取config.ini文件
    """
    def __init__(self):
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))     #src路径
        PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.path.pardir))                   #工程目录
        # config目录
        config_dir = PROJECT_DIR + '/config'
        # config.ini文件路径
        config = os.path.join(config_dir, 'config.ini')

        if os.path.exists(config):
            # 读取config.ini文件
            conf = configparser.ConfigParser()
            conf.read(config, encoding='utf-8')

            # config.ini文件配置
            self.operating_environment = conf.get('dir_base', 'operating_environment')          # 运行环境
            self.testhost = os.path.join(PROJECT_DIR, conf.get('dir_base', 'host_test'))        # 测试接口host
            self.log_dir = os.path.join(PROJECT_DIR, conf.get('dir_base', 'log_dir'))           # 日志文件路径
            self.refdata_dir = os.path.join(PROJECT_DIR, conf.get('dir_base', 'refdata_dir'))   # 配置文件路径
            self.report_dir = os.path.join(PROJECT_DIR, conf.get('dir_base', 'report_dir'))     # 测试报告输出路径

            # zookeeper配置
            self.zkp_host = conf.get('zookeeper_base', 'zkp_host')  # zookeeper host地址

            # url host
            self.dev_host = conf.get('operating_base', 'dev_host')
            self.test_host = conf.get('operating_base', 'test_host')
            self.local_host = conf.get('operating_base', 'local_host')

            # 预留db配置
            self.db_local_host = conf.get('db_local_base', 'db_local_host')           # db host地址
            self.db_local_port = conf.get('db_local_base', 'db_local_port')           # db 端口
            self.db_local_username = conf.get('db_local_base', 'db_local_username')   # db 用户名
            self.db_local_password = conf.get('db_local_base', 'db_local_password')   # db 密码
            self.db_local_name = conf.get('db_local_base', 'db_local_name')           # 数据库名称

            self.db_test_host = conf.get('db_other_base', 'db_test_host')           # db host地址
            self.db_test_port = conf.get('db_other_base', 'db_test_port')           # db 端口
            self.db_test_username = conf.get('db_other_base', 'db_test_username')   # db 用户名
            self.db_test_password = conf.get('db_other_base', 'db_test_password')   # db 密码
            self.db_test_name = conf.get('db_other_base', 'db_test_name')           # 数据库名称

            self.db_dev_host = conf.get('db_other_base', 'db_dev_host')           # db host地址
            self.db_dev_port = conf.get('db_other_base', 'db_dev_port')           # db 端口
            self.db_dev_username = conf.get('db_other_base', 'db_dev_username')   # db 用户名
            self.db_dev_password = conf.get('db_other_base', 'db_dev_password')   # db 密码
            self.db_dev_name = conf.get('db_other_base', 'db_dev_name')           # 数据库名称

        else:
            raise Exception("缺少config.ini文件")


class Logging():
    """
    # 日志模块,输出在log目录下,以日期分割
    """
    def __init__(self):
        config = Config()
        self.logname = config.log_dir + '/' + time.strftime('%Y-%m-%d') + '.log'    # log文件

    def printconsole(self, level, message):
        # 创建一个log
        logger = logging.getLogger(__name__)
        # 设置日志级别
        logger.setLevel(logging.DEBUG)

        # 创建一个handler,用于写入日志文件
        fh = logging.FileHandler(self.logname, 'a')
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s- %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给log添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)

        # 记录一条日志
        if level == 'info':
            logger.info(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'warring':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)
        logger.removeHandler(fh)
        logger.removeHandler(ch)

    def debug(self, message):
        self.printconsole('debug', message)

    def info(self, message):
        self.printconsole('info', message)

    def warring(self, message):
        self.printconsole('warring', message)

    def error(self, message):
        self.printconsole('error', message)


class DB_Connect():
    """
    # 连接db方法
    """
    def __init__(self):
        self.conf = Config()

    def mysql_creat(self):
        # 创建db连接
        db = pymysql.connect(self.conf.db_host, self.conf.db_prot,
                             self.conf.db_username, self.conf.db_password,
                             self.conf.db_name)
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        sql_exists = ''
        cursor.execute()


class Base_Method():
    """
    # 基础公共方法
    """
    def __init__(self):
        self.conf = Config()
        self.log = Logging()
        self.zkp = KazooClient(hosts=self.conf.zkp_host)

    def get_excel_content(self, filename='TaskOs_api_refdata.xlsx'):
        """
        # 解析excel文件
        :param filename:文件路径
        :return: 返回存储excel内容列表
        """
        filepath = os.path.join(self.conf.refdata_dir, filename)
        system = platform.system()  # 获取系统环境
        if system == 'Windows' or system == 'Linux':
            # Windows、Linux系统环境
            openfile = xlrd.open_workbook(filename=filepath, encoding_override='utf-8')
        elif system == 'Darwin':
            # MacOSX系统环境
            openfile = xlrd.open_workbook(filename=filepath)
        else:
            self.log.error("不支持的系统环境")
            return False
        # 配置参数sheet
        table_params = openfile.sheet_by_name('input')
        rows_params = table_params.nrows        # 行
        ncols_params = table_params.ncols       # 列

        # 配置校验sheet
        table_check = openfile.sheet_by_name('check')
        rows_check = table_check.nrows
        ncols_check = table_check.ncols

        # excel头行
        row_params_head = table_params.row_values(1)
        row_check_head = table_check.row_values(1)

        # 去除空单元格
        while '' in row_params_head:
            row_params_head.remove('')
        while '' in row_check_head:
            row_check_head.remove('')

        get_params_sheet = []   # 空列表存储参数配置sheet
        get_check_sheet = []    # 空列表存储校验配置sheet
        # excel params sheet配置内容
        for rownum in range(2, rows_params):
            row = table_params.row_values(rownum)
            # 去除空单元格
            if row:
                while '' in row:
                    row.remove('')
            # 组合头字段与行单元格
            dictparams = {row_params_head[0]:row[0], row_params_head[1]:row[1], row_params_head[2]:row[2],
                          row_params_head[3]:row[3], row_params_head[4]:row[4], row_params_head[5]:row[5:]}
            get_params_sheet.append(dictparams)
        # excel check sheet配置内容
        for rownum in range(2, rows_check):
            row = table_check.row_values(rownum)
            # 去除空单元格
            if row:
                while '' in row:
                    row.remove('')
            dictcheck = {row_check_head[0]:row[0], row_check_head[1]:row[1], row_check_head[2]:row[2], row_check_head[3]:row[3:]}   # 组合头字段与行单元格
            get_check_sheet.append(dictcheck)

        dict_excel = {'params_sheet': get_params_sheet, 'check_sheet': get_check_sheet}
        return dict_excel

    def analysis_content(self, data):
        """
        # 解析读取excel的内容,将参数配置组装,且与校验配置对应
        # 依赖请求参数通过{}识别，后续增加支持
        :param data:字典类型
        :return:
        """
        paramssheetlist = data['params_sheet']     # 参数配置sheet数据
        checksheetlist = data['check_sheet']       # 校验配置sheet数据



        pass

    def write_excel(self, filename, data):
        """
        # 执行接口测试结果写入excel
        :param filename:
        :param data:
        :return:
        """
        pass

    def login_url(self, func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper

    def getdict(self, *args, **kwargs):
        print(*args)
        print(**kwargs)
        # return dict(zip(*args, **kwargs))


    def resquest_login(self, username, password):
        """
        # 登录
        :param username: 用户名
        :param password: 登录密码
        :return:
        """
        params = {'username':username,
                  'password':password}

        rsponse = requests.post(url=self.conf.testhost, data=params, timeout=10)


    def resquest_url(self, url, params, resq_type, cookies, rsp_type='json'):
        """
        # 请求url
        :param url: 请求url地址
        :param params: 请求参数
        :param resq_type: 请求发送方式('get'/'post')
        :param cookies: cookies
        :param rsp_type: 可选参数，默认以json返回.响应返回类型('text'/'json'/'raw'/'content')
        :return:请求响应
        """
        # 解析请求参数,转换为字典形式
        if params == '':
            params_dict = ''
        else:
            paramslist = params.split('&')  # 以&分割参数
            keys = []
            values = []
            for i in paramslist:
                newlist = i.split('=')      # 以=分割参数key和value
                keys.append(newlist[0])
                values.append((newlist[1]))
            # 得到组装后的参数字典
            params_dict = dict(zip(keys, values))

        # 组装响应头

        # 发送请求
        try:
            if resq_type == 'get':
                response = requests.get(url=url, params=params_dict, cookies=cookies, timeout=10)
            elif resq_type == 'post':
                response = requests.post(url=url, data=params_dict, cookies=cookies, timeout=10)
            else:
                raise Exception("resq_type={},不支持的请求方式".format(resq_type))
        except TimeoutError:
            self.log.error("请求超时")
        except Exception as e:
            self.log.error("请求出现异常：%s"%e)
        else:
            response.raise_for_status()     # 返回响应非200抛出异常
            # 以text返回
            if rsp_type == 'text':
                return response.text
            # 以原始返回
            elif rsp_type == 'raw':
                return response.raw
            # 以二进制返回
            elif resq_type == 'content':
                return response.content
            # 以json返回
            else:
                return response.json()


    def connect_zkp(self, func):
        """
        # zookeeper操作连接装饰器
        :param func:
        :return:
        """
        # 创建连接
        # zkp = KazooClient(hosts=self.conf.zkp_host)
        # 判断连接状态,当前连接断开重新开启连接
        if not self.zkp.connected:
            self.zkp.start(timeout=6)
        def warpper():
            if self.zkp.connected:
                func()
                self.zkp.close()
            else:
                raise Exception('zookeeper 连接失败')
        return warpper

    # @connect_zkp()
    def base_zkp(self, basedir, id, pid):
        """
        # zkp基础
        :param basedir:
        :param id:当前节点的id,ID的组成是 深度+兄弟节点序号+父节点ID
        :param pid:父亲节点ID
        :return:
        children:子节点个数
        deep:深度
        """
        try:
            if basedir == '/':
                children = ['redis', 'game', 'uc']
            else:
                children = self.zkp.get_children(path=basedir)
            cut = basedir.split('/')
            deep = len(cut) - 1
            name = cut[deep]
            if len(children) == 0:
                childrenlen = 0
            else:
                childrenlen = len(children)
            item = {'id':id, 'pid':pid, 'name':name, 'children':childrenlen, 'deep':deep, 'ur': basedir}
            datas = []
            datas.append(item)
            for i in range(len(children)):
                path = os.path.join(basedir, children[i])
                cut = path.split('/')
                n_id = str(len(cut) - 1) + str(i) + str(id)
                basedir(path, n_id, id)
        except Exception as e:
            data = str(e)


















if __name__ == "__main__":
    test = Base_Method()
    exceldict = test.get_excel_content()
    print(exceldict)

