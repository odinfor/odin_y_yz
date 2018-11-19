# -*- coding:utf-8 -*-
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.source.base import Config, Base_Method

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
            listparams = basemethod['params_sheet']
        else:
            listparams = basemethod['check_sheet']
        list1 = []
        if len(listparams) > 0:
            for i in listparams:
                list2 = i['params']
                while len(list2) <= 11:
                    list2.append(None)
                list1.append(list2)
        return list1
    else:
        raise Exception('调用make_paramdict方法输入sheet名称不存在')

params_list = make_paramdict(sheetname='input')
check_list = make_paramdict(sheetname='check')


class ParamsTable(base):
    __tablename__ = 'params_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    indexID = Column(Integer, nullable=True)
    explain = Column(Text, nullable=True)
    url = Column(String(50), nullable=False, default='http://127.0.0.1')
    params_1 = Column(String(50), nullable=True, default=None)
    params_2 = Column(String(50), nullable=True, default=None)
    params_3 = Column(String(50), nullable=True, default=None)
    params_4 = Column(String(50), nullable=True, default=None)
    params_5 = Column(String(50), nullable=True, default=None)
    params_6 = Column(String(50), nullable=True, default=None)
    params_7 = Column(String(50), nullable=True, default=None)
    params_8 = Column(String(50), nullable=True, default=None)
    params_9 = Column(String(50), nullable=True, default=None)
    params_10 = Column(String(50), nullable=True, default=None)
    params_11 = Column(String(50), nullable=True, default=None)

    def __init__(self, indexID, explain, url, *args):
        self.indexID = indexID
        self.explain = explain
        self.url = url
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
        return "<ParamsTable(indexID=%, explain=%, url=%, params_1=%, params_2=%, params_3=%, params_4=%, params_5=%," \
               "params_6=%, params_7=%, params_8=%, params_9=%, params_10=%, params_11=%)>"%(self.indexID, self.explain,
                self.url, self.params_1, self.params_2, self.params_3, self.params_4, self.params_5, self.params_6,
                self.params_7,self.params_8, self.params_9, self.params_10, self.params_11)

class CheckTable(base):
    __tablename__ = 'check_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    indexID = Column(Integer, nullable=True)
    explain = Column(Text, nullable=True)
    check_1 = Column(String(50), nullable=True, default=None)
    check_2 = Column(String(50), nullable=True, default=None)
    check_3 = Column(String(50), nullable=True, default=None)
    check_4 = Column(String(50), nullable=True, default=None)
    check_5 = Column(String(50), nullable=True, default=None)
    check_6 = Column(String(50), nullable=True, default=None)
    check_7 = Column(String(50), nullable=True, default=None)
    check_8 = Column(String(50), nullable=True, default=None)
    check_9 = Column(String(50), nullable=True, default=None)
    check_10 = Column(String(50), nullable=True, default=None)
    check_11 = Column(String(50), nullable=True, default=None)

    def __init__(self, indexID, explain, *args):
        self.indexID = indexID
        self.explain = explain
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
        return "<ParamsTable(indexID=%, explain=%, check_1=%, check_2=%, check_3=%, check_4=%, check_5=%,check_6=%, " \
               "check_7=%, check_8=%, check_9=%, check_10=%, check_11=%)>"%(self.indexID, self.explain,self.check_1,
                self.check_2, self.check_3, self.check_4, self.check_5, self.check_6, self.check_7,self.check_8,
                self.check_9, self.check_10, self.check_11)


class DBControl():
    def __init__(self):
        conf = Config()
        self.db_adress = 'mysql+pymysql://' + conf.db_username + ':' + conf.db_password + '@' + conf.db_host + ':' \
                    + conf.db_prot + '/' + conf.db_name
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
                obj = ParamsTable(param['id'], param['explain'], param['url'], *params_list[paramsheet.index(param)])
                print(params_list[paramsheet.index(param)])
                self.insert(obj)
        if len(checksheet) > 0:
            for check in checksheet:
                obj = CheckTable(check['id'], check['explain'], *check_list[checksheet.index(check)])
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
    test.insert_all_table()
    test.close_db()



