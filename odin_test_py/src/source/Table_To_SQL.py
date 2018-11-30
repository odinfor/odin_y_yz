# -*- coding: utf-8 -*-
# @Time    : 2018-11-27 19:26
# @Author  : odin_y
# @Email   : 
# @File    : Table_To_SQL.py
# @Software: PyCharm
# @Comment : 文件数据转入SQL
import xlrd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from base import Config, Logging
import os, platform
import time

base = declarative_base()   # 创建基类
conf = Config()
log = Logging()


class ParamsAllTable(base):
    """# 接口请求配置保存表,一直保存,只能主动清除"""
    __tablename__ = 'params_all_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    caseID = Column(String(20), nullable=False, comment="测试案例ID")
    casename = Column(String(20), nullable=False, default='smoke', comment="测试案例名称")
    run = Column(String(5), nullable=False, default='True', comment="是否执行该案例")
    host = Column(String(50), nullable=True, comment="host地址")
    url = Column(String(50), nullable=True, comment="接口地址")
    comment = Column(Text, nullable=True, comment="测试场景说明")
    params_1 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_2 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_3 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_4 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_5 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_6 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_7 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_8 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_9 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_10 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_11 = Column(String(50), nullable=True, default=None, comment="请求入参")

    def __repr__(self):
        return ("<ParamsOnceTable(id={}, caseID={}, casename={}, run={}, host={}, url={}, comment={}, params_1={}, "
                "params_2={}, params_3={}, params_4={}, params_5={},params_6={}, params_7={}, params_8={}, "
                "params_9={}, params_10={}, params_11={})>".format(ParamsOnceTable.id, ParamsOnceTable.caseID,
                 ParamsOnceTable.casename, ParamsOnceTable.run, ParamsOnceTable.host, ParamsOnceTable.url,
                 ParamsOnceTable.comment, ParamsOnceTable.params_1, ParamsOnceTable.params_2, ParamsOnceTable.params_3,
                 ParamsOnceTable.params_4, ParamsOnceTable.params_5, ParamsOnceTable.params_6, ParamsOnceTable.params_7,
                 ParamsOnceTable.params_8, ParamsOnceTable.params_9, ParamsOnceTable.params_10,
                 ParamsOnceTable.params_11))


class ParamsOnceTable(base):
    """# 接口请求配置保存表,读取配置时触发清除,重新写入"""
    __tablename__ = 'params_once_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    caseID = Column(String(20), nullable=False, comment="测试案例ID")
    casename = Column(String(20), nullable=False, default='smoke', comment="测试案例名称")
    run = Column(String(5), nullable=False, default='True', comment="是否执行该案例")
    host = Column(String(50), nullable=False, comment="host地址")
    url = Column(String(50), nullable=True, comment="接口地址")
    comment = Column(Text, nullable=True, comment="测试场景说明")
    params_1 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_2 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_3 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_4 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_5 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_6 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_7 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_8 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_9 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_10 = Column(String(50), nullable=True, default=None, comment="请求入参")
    params_11 = Column(String(50), nullable=True, default=None, comment="请求入参")

    def __repr__(self):
        return ("<ParamsOnceTable(id={}, caseID={}, casename={}, run={}, host={}, url={}, comment={}, params_1={}, "
                "params_2={}, params_3={}, params_4={}, params_5={},params_6={}, params_7={}, params_8={}, "
                "params_9={}, params_10={}, params_11={})>".format(ParamsOnceTable.id, ParamsOnceTable.caseID,
                 ParamsOnceTable.casename, ParamsOnceTable.run, ParamsOnceTable.host, ParamsOnceTable.url,
                 ParamsOnceTable.comment, ParamsOnceTable.params_1, ParamsOnceTable.params_2, ParamsOnceTable.params_3,
                 ParamsOnceTable.params_4, ParamsOnceTable.params_5, ParamsOnceTable.params_6, ParamsOnceTable.params_7,
                 ParamsOnceTable.params_8, ParamsOnceTable.params_9, ParamsOnceTable.params_10,
                 ParamsOnceTable.params_11))


class CheckOnceTable(base):
    """# 接口校验配置保存表,读取配置时触发清除,重新写入"""
    __tablename__ = 'check_once_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    caseID = Column(String(20), nullable=False, comment="测试案例ID")
    casename = Column(String(20), nullable=True, default='smoke', comment="测试案例名称")
    comment = Column(Text, nullable=True, comment="测试场景说明")
    error_code = Column(Integer, default=0, comment="响应返回预期code")
    check_1 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_2 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_3 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_4 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_5 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_6 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_7 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_8 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_9 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_10 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_11 = Column(String(50), nullable=True, default=None, comment="校验参数")

    def __repr__(self):
        return "<CheckAllTable(caseID={}, casename={}, error_code={}, check_1={}, check_2={}, check_3={}, check_4={}, " \
               "check_5={},check_6={}, check_7={}, check_8={}, check_9={}, check_10={}, check_11={})>".format(
                CheckAllTable.caseID, CheckAllTable.casename, CheckAllTable.error_code, CheckAllTable.check_1,
                CheckAllTable.check_2, CheckAllTable.check_3, CheckAllTable.check_4, CheckAllTable.check_5,
                CheckAllTable.check_6, CheckAllTable.check_7, CheckAllTable.check_8, CheckAllTable.check_9,
                CheckAllTable.check_10, CheckAllTable.check_11)


class CheckAllTable(base):
    """# 接口校验配置保存表,一直保存,只能主动清除"""
    __tablename__ = 'check_all_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    caseID = Column(String(20), nullable=False, comment="测试案例ID")
    casename = Column(String(20), nullable=True, default='smoke', comment="测试案例名称")
    comment = Column(Text, nullable=True, comment="测试场景说明")
    error_code = Column(Integer, default=0, comment="响应返回预期code")
    check_1 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_2 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_3 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_4 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_5 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_6 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_7 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_8 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_9 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_10 = Column(String(50), nullable=True, default=None, comment="校验参数")
    check_11 = Column(String(50), nullable=True, default=None, comment="校验参数")

    def __repr__(self):
        return "<CheckAllTable(caseID={}, casename={}, error_code={}, check_1={}, check_2={}, check_3={}, check_4={}, " \
               "check_5={},check_6={}, check_7={}, check_8={}, check_9={}, check_10={}, check_11={})>".format(
                CheckAllTable.caseID, CheckAllTable.casename, CheckAllTable.error_code, CheckAllTable.check_1,
                CheckAllTable.check_2, CheckAllTable.check_3, CheckAllTable.check_4, CheckAllTable.check_5,
                CheckAllTable.check_6, CheckAllTable.check_7, CheckAllTable.check_8, CheckAllTable.check_9,
                CheckAllTable.check_10, CheckAllTable.check_11)


class RspTable(base):
    """# 响应结果表"""
    __tablename__ = 'rsp_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    caseID = Column(String(20), nullable=False, comment="测试案例id")
    casename = Column(String(20), nullable=True, default='smoke', comment="测试case名称")
    comment = Column(Text, nullable=True, comment="测试场景说明")
    rsp = Column(String(500), nullable=True, default=None, comment="接口响应返回")
    is_pass = Column(Boolean, nullable=True, default=False, comment="是否通过")
    log = Column(String(500), nullable=True, default=None, comment="校验说明")

    def __repr__(self):
        return "<RspTable(caseID={}, casename={}, comment={}, rsp={}, is_pass={}, log={}>".format(RspTable.caseID,
                RspTable.casename, RspTable.comment, RspTable.rsp, RspTable.is_pass, RspTable.log)


class TestTable(base):
    """# 响应结果表"""
    __tablename__ = 'test_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    caseID = Column(String(20), nullable=True, comment="测试案例id")
    casename = Column(String(20), nullable=True, default='smoke', comment="测试case名称")

    def __repr__(self):
        return "<TestTable(caseID=%, casename=%>"%(TestTable.caseID, TestTable.casename)


def get_excel_content(filename='TaskOs_api_refdata.xlsx'):
    """
    # 解析excel文件
    :param filename:文件路径
    :return: 以生成器返回excel内容列表
    """
    filepath = os.path.join(conf.refdata_dir, filename)
    system = platform.system()  # 获取系统环境
    if system == 'Windows' or system == 'Linux':
        # Windows、Linux系统环境
        openfile = xlrd.open_workbook(filename=filepath, encoding_override='utf-8')
    elif system == 'Darwin':
        # MacOSX系统环境
        openfile = xlrd.open_workbook(filename=filepath)
    else:
        log.error("不支持的系统环境")
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

    # excel params sheet配置内容
    for rownum in range(2, rows_params):
        row = table_params.row_values(rownum)
        # 组合头字段与行单元格
        dictparams = dict(zip(row_params_head, row))
        # excel文件host为空使用config配置
        if dictparams['host'] == '':
            if conf.operating_environment == 'test':
                dictparams['host'] = conf.test_host
            elif conf.operating_environment == 'dev':
                dictparams['host'] = conf.dev_host
            elif conf.operating_environment == 'local':
                dictparams['host'] = conf.local_host
            else:
                dictparams['host'] = '无效的配置'
        # excel check sheet配置内容
        row = table_check.row_values(rownum)
        dictcheck = dict(zip(row_check_head, row))

        dict_excel = {'params_sheet': dictparams, 'check_sheet': dictcheck}
        yield dict_excel


class SqlalchemyControlDB:
    """# sqlalchemy 操作db"""
    def __init__(self):
        conf = Config()
        if conf.operating_environment == 'test':
            self.db_adress = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(conf.db_test_username, conf.db_test_password,
                                                                     conf.db_test_host, conf.db_test_port,
                                                                     conf.db_test_name)
        elif conf.operating_environment == 'dev':
            self.db_adress = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(conf.db_dev_username, conf.db_dev_password,
                                                                     conf.db_dev_host, conf.db_dev_port,
                                                                     conf.db_dev_name)
        elif conf.operating_environment == 'local':
            self.db_adress = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(conf.db_local_username, conf.db_local_password,
                                                                     conf.db_local_host, conf.db_local_port,
                                                                     conf.db_local_name)

    def connect_db(self):
        # 初始化连接mysqldb, 不显示sql logging
        self.engine = create_engine(self.db_adress, echo=False, encoding='utf-8')  # 建立数据库
        db_session = sessionmaker(bind=self.engine)  # 创建连接
        self.session = db_session()

    def creat_all_table(self):
        base.metadata.create_all(self.engine)

    def insertdict(self):
        excelfile = get_excel_content()
        for line in excelfile:
            line['params_sheet']['caseID'] = '{}_{}'.format(int(time.time()), line['params_sheet']['caseID'])
            line['check_sheet']['caseID'] = '{}_{}'.format(int(time.time()), line['check_sheet']['caseID'])
            param_obj = ParamsOnceTable(**line['params_sheet'])
            check_obj = CheckOnceTable(**line['check_sheet'])
            try:
                self.session.add(param_obj)
                self.session.add(check_obj)
            except:
                self.session.roll_back()
        self.session.commit()

    def close_db(self):
        self.session.close()

    def delete_table(self, tablename):
        sql = 'delete from {}'.format(tablename)
        try:
            self.session.execute(sql)
        except Exception as msg:
            log.error(msg)
            self.session.roll_back()
        else:
            self.session.commit()


if __name__ == '__main__':
    run = SqlalchemyControlDB()
    run.connect_db()
    run.creat_all_table()
    run.del_rsp_table()
    # # run.insertdict()
    run.close_db()
