# -*- coding:utf-8 -*-
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.source.base import Config

base = declarative_base()   # 创建基类


class ParamsTable(base):
    __tablename__ = 'params_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
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

    def __init__(self, id, explain, *args):
        self.id = id
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


class CheckTable(base):
    __tablename__ = 'check_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    explain = Column(Text, nullable=True)
    check_1 = Column(String(50), nullable=True)
    check_2 = Column(String(50), nullable=True)
    check_3 = Column(String(50), nullable=True)
    check_4 = Column(String(50), nullable=True)
    check_5 = Column(String(50), nullable=True)
    check_6 = Column(String(50), nullable=True)
    check_7 = Column(String(50), nullable=True)
    check_8 = Column(String(50), nullable=True)
    check_9 = Column(String(50), nullable=True)
    check_10 = Column(String(50), nullable=True)
    check_11 = Column(String(50), nullable=True)

    def __init__(self, id, explain, *args):
        self.id = id
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


def create_table():
    conf = Config()
    db_adress = 'mysql+pymysql://' + conf.db_username + ':' + conf.db_password + '@' + conf.db_host + ':' + conf.db_prot + '/' + conf.db_name
    print('db_adress:', db_adress)
    # 初始化连接mysqldb, 不显示sql logging
    engine = create_engine(db_adress, echo=False)

    base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)     # 创建与数据库会话
    session = Session()

if __name__ == '__main__':
    create_table()



