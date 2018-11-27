# -*- coding:utf-8 -*-
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from base import Config, Base_Method

base = declarative_base()   # 创建基类
basemethod = Base_Method().get_excel_content()


def make_paramdict(sheetname):
    """
    # 生成插入列表
    :param sheetname: excel sheet名称
    :return:
    """
    if sheetname in ['input', 'check']:
        basemethod = Base_Method().get_excel_content()
        if sheetname == 'input':
            listsheet = basemethod['params_sheet']
        else:
            listsheet = basemethod['check_sheet']
        list1 = []
        if len(listsheet) > 0:
            for i in listsheet:
                list2 = i['params']
                while len(list2) <= 11:
                    list2.append(None)
                list1.append(list2)
        return list1
    else:
        raise Exception('调用make_paramdict方法输入sheet名称不存在')

params_list = make_paramdict(sheetname='input')
check_list = make_paramdict(sheetname='check')


class ParamsAllTable(base):
    """# 接口请求配置保存表,一直保存,只能主动清除"""
    __tablename__ = 'params_all_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    caseID = Column(Integer, nullable=True, comment="测试案例ID")
    casename = Column(String(20), nullable=False, default='smoke', comment="测试案例名称")
    isrun = Column(String(5), nullable=False, default='True', comment="是否执行该案例")
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

    def __init__(self, caseID, casename, isrun, host, url, comment=None, *args):
        self.caseID = caseID
        self.casename = casename
        self.isrun = isrun
        self.host = host
        self.url = url
        self.comment = comment
        self.params_1 = args[0]
        self.params_2 = args[1]
        self.params_3 = args[2]
        self.params_4 = args[3]
        self.params_5 = args[4]
        self.params_6 = args[5]
        self.params_7 = args[6]
        self.params_8 = args[7]
        self.params_9 = args[8]
        self.params_10 = args[9]
        self.params_11 = args[10]

    def __repr__(self):
        return "<ParamsTable(caseID=%, casename=%, isrun=%, host=%, url=%, comment=%, params_1=%, params_2=%, " \
               "params_3=%, params_4=%, params_5=%,params_6=%, params_7=%, params_8=%, params_9=%, params_10=%, " \
               "params_11=%)>"%(self.caseID, self.casename, self.isrun, self.host, self.url, self.comment,
                                self.params_1, self.params_2, self.params_3, self.params_4, self.params_5,
                                self.params_6,self.params_7,self.params_8, self.params_9, self.params_10,
                                self.params_11)


class ParamsOnceTable(base):
    """# 接口请求配置保存表,读取配置时触发清除,重新写入"""
    __tablename__ = 'params_once_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    caseID = Column(Integer, nullable=True, comment="测试案例ID")
    casename = Column(String(20), nullable=False, default='smoke', comment="测试案例名称")
    isrun = Column(String(5), nullable=False, default='True', comment="是否执行该案例")
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

    def __init__(self, caseID, casename, isrun, host, url, comment=None, *args):
        self.caseID = caseID
        self.casename = casename
        self.isrun = isrun
        self.host = host
        self.url = url
        self.comment = comment
        self.params_1 = args[0]
        self.params_2 = args[1]
        self.params_3 = args[2]
        self.params_4 = args[3]
        self.params_5 = args[4]
        self.params_6 = args[5]
        self.params_7 = args[6]
        self.params_8 = args[7]
        self.params_9 = args[8]
        self.params_10 = args[9]
        self.params_11 = args[10]

    def __repr__(self):
        return "<ParamsTable(caseID=%, casename=%, isrun=%, host=%, url=%, comment=%, params_1=%, params_2=%, " \
               "params_3=%, params_4=%, params_5=%,params_6=%, params_7=%, params_8=%, params_9=%, params_10=%, " \
               "params_11=%)>"%(self.caseID, self.casename, self.isrun, self.host, self.url, self.comment,
                                self.params_1, self.params_2, self.params_3, self.params_4, self.params_5,
                                self.params_6,self.params_7,self.params_8, self.params_9, self.params_10,
                                self.params_11)


class CheckOnceTable(base):
    """# 接口校验配置保存表,读取配置时触发清除,重新写入"""
    __tablename__ = 'check_once_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    caseID = Column(Integer, nullable=True, comment="测试案例ID")
    casename = Column(String(20), nullable=True, default='smoke', comment="测试案例名称")
    comment = Column(Text, nullable=True, comment="测试场景说明")
    code = Column(Integer, default=200, comment="响应返回预期code")
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

    def __init__(self, caseID, casename, code, *args):
        self.caseID = caseID
        self.casename = casename
        self.code = code
        self.check_1 = args[0]
        self.check_2 = args[1]
        self.check_3 = args[2]
        self.check_4 = args[3]
        self.check_5 = args[4]
        self.check_6 = args[5]
        self.check_7 = args[6]
        self.check_8 = args[7]
        self.check_9 = args[8]
        self.check_10 = args[9]
        self.check_11 = args[10]

    def __repr__(self):
        return "<ParamsTable(caseID=%, casename=%, code=%, check_1=%, check_2=%, check_3=%, check_4=%, check_5=%,check_6=%, " \
               "check_7=%, check_8=%, check_9=%, check_10=%, check_11=%)>"%(self.caseID, self.casename, self.code,
                self.check_1,self.check_2, self.check_3, self.check_4, self.check_5, self.check_6, self.check_7,
                self.check_8,self.check_9, self.check_10, self.check_11)


class CheckAllTable(base):
    """# 接口校验配置保存表,一直保存,只能主动清除"""
    __tablename__ = 'check_all_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    caseID = Column(Integer, nullable=True, comment="测试案例ID")
    casename = Column(String(20), nullable=True, default='smoke', comment="测试案例名称")
    comment = Column(Text, nullable=True, comment="测试场景说明")
    code = Column(Integer, default=200, comment="响应返回预期code")
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

    def __init__(self, caseID, casename, code, *args):
        self.caseID = caseID
        self.casename = casename
        self.code = code
        self.check_1 = args[0]
        self.check_2 = args[1]
        self.check_3 = args[2]
        self.check_4 = args[3]
        self.check_5 = args[4]
        self.check_6 = args[5]
        self.check_7 = args[6]
        self.check_8 = args[7]
        self.check_9 = args[8]
        self.check_10 = args[9]
        self.check_11 = args[10]

    def __repr__(self):
        return "<ParamsTable(caseID=%, casename=%, code=%, check_1=%, check_2=%, check_3=%, check_4=%, check_5=%,check_6=%, " \
               "check_7=%, check_8=%, check_9=%, check_10=%, check_11=%)>"%(self.caseID, self.casename, self.code,
                self.check_1,self.check_2, self.check_3, self.check_4, self.check_5, self.check_6, self.check_7,
                self.check_8,self.check_9, self.check_10, self.check_11)


class RspTable(base):
    """# 响应结果表"""
    __tablename__ = 'rsp_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    caseID = Column(Integer, nullable=True, comment="测试案例id")
    casename = Column(String(20), nullable=True, default='smoke', comment="测试case名称")
    comment = Column(Text, nullable=True, comment="测试场景说明")
    rsp = Column(String(500), nullable=True, default=None, comment="接口响应返回")
    is_pass = Column(Boolean, nullable=True, default=False, comment="是否通过")
    log = Column(String(500), nullable=True, default=None, comment="校验说明")

    def __init__(self, caseID, casename, comment, rsp, is_pass, log):
        self.caseID = caseID
        self.casename = casename
        self.comment = comment
        self.rsp = rsp
        self.is_pass = is_pass
        self.log = log

    def __repr__(self):
        return "<ParamsTable(caseID=%, casename=%, comment=%, rsp=%, is_pass=%, log=%>"%(self.caseID, self.casename,
                                                                                         self.comment, self.rsp,
                                                                                         self.is_pass, self.log)


class DBControl:
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
        # 初始化连接mysqldb, 不显示sql logging
        self.engine = create_engine(self.db_adress, echo=False)  # 建立数据库
        db_session = sessionmaker(bind=self.engine)  # 创建连接
        self.session = db_session()

    def create_table(self):
        """# 创建数据表"""
        base.metadata.create_all(self.engine)

    def close_db(self):
        self.session.close()

    def insert_all_table(self):
        objlist1 = []
        objlist2 = []
        paramsheet = basemethod['params_sheet']
        checksheet = basemethod['check_sheet']
        # if len(params_list) > 0:
        #     for param in paramsheet:
        #         obj = ParamsTable(param['id'], param['explain'], param['url'], *params_list[paramsheet.index(param)])
        #         objlist1.append(obj)
        #     print('objlist1:',objlist1)
        # if len(checksheet) > 0:
        #     for check in checksheet:
        #         obj = CheckTable(check['id'], check['explain'], *check_list[checksheet.index(check)])
        #         objlist2.append(obj)
        if len(params_list) > 0:
            for param in paramsheet:
                obj = ParamsOnceTable(param['id'], param['explain'], param['isrun'], param['host'], param['url'], *params_list[paramsheet.index(param)])
                self.insert(obj)
        if len(checksheet) > 0:
            for check in checksheet:
                obj = CheckOnceTable(check['id'], check['explain'], check['code'], *check_list[checksheet.index(check)])
                self.insert(obj)

    def drop_all_db(self):
        base.metadata.drop_all(self.engine)

    def insert(self, obj):
        try:
            self.session.add(obj)
        except:
            self.rollback()
        else:
            self.session.commit()

if __name__ == '__main__':
    # test = DBControl()
    # test.create_table()
    # for params in params_list:
    #     obj = ParamsTable(1, 'this is explain', *params)
    #     test.insert(obj)
    test = DBControl()
    test.create_table()
    # test.drop_all_db()
    # test.insert_all_table()
    test.close_db()



