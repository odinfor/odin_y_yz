# -*- coding:utf-8 -*-
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.source.base import Config

base = declarative_base()   # 创建基类


class ParamsTable(base):
    __tablename__ = 'params_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    indexID = Column(Integer, nullable=True)
    explain = Column(Text, nullable=True)
    params_1 = Column(String(50), nullable=True)
    params_2 = Column(String(50), nullable=True)
    params_3 = Column(String(50), nullable=True)
    params_4 = Column(String(50), nullable=True)
    params_5 = Column(String(50), nullable=True)
    params_6 = Column(String(50), nullable=True)
    params_7 = Column(String(50), nullable=True)
    params_8 = Column(String(50), nullable=True)
    params_9 = Column(String(50), nullable=True)
    params_10 = Column(String(50), nullable=True)
    params_11 = Column(String(50), nullable=True)

    def __init__(self,indexID, explain, *args):
        self.indexID = indexID
        self.explain = explain
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

    # def __repr__(self):
    #     return "<ParamsTable(indexID=%, explain=%, params_1=%, params_2=%, params_3=%, params_4=%, params_5=%," \
    #            "params_6=%, params_7=%, params_8=%, params_9=%, params_10=%, params_11=%)>"%(self.indexID, self.explain,
    #             self.params_1, self.params_2, self.params_3, self.params_4, self.params_5, self.params_6, self.params_7,
    #             self.params_8, self.params_9, self.params_10, self.params_11)

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
        argslen = len(args)
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

    def insert(self, obj):
        self.session.add(obj)
        self.session.commit()




if __name__ == '__main__':
    # create_table()
    # test = DBControl()
    # test()
    obj1 = CheckTable(1, 'this is explain', *[1,2])

    dbcontrol = DBControl()
    dbcontrol.create_table()
    #
    # def test1(id, *args):
    #     id = id
    #     a1 = args[0]
    #     print('args:', args)
    #     #print('kwargs:', kwargs)
    #     print('='*10)
    #     print(a1)
    # test1(2, *['gd', 'gdg'])

