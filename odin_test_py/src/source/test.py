# -*- coding:utf-8 -*-
import requests
import json
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymysql
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from base import Logging, Config


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

class ProcessAPI:
    """
    # 流程管理API
    """
    def __init__(self, args):
        self.id = args['id'] if 'id' in args.keys() else None
        self.name = args['name'] if 'name' in args.keys() else None
        self.code = args['code'] if 'code' in args.keys() else None
        self.nodeSetting = args['nodeSetting'] if 'nodeSetting' in args.keys() else None
        self.status = args['status'] if 'status' in args.keys() else None
        self.comment = args['comment'] if 'comment' in args.keys() else None
        self.pageNum = args['pageNum'] if 'pageNum' in args.keys() else None
        self.pageSize = args['pageSize'] if 'pageSize' in args.keys() else None

        self.PySQL = PySQLDB()
        self.log = Logging()
        self.config = Config()

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

    def run_case(self, interfacetype, rsptype='json'):
        """
        # 调用接口方法
        :param interfacetype: 接口类型<getinputdata方法返回>
        :param rsptype:返回响应类型,默认json.支持text/json/raw
        :return:响应返回结果
        """
        get_auth = self.login_yunxi()
        headers = {'Content-Type': 'application/json',
                   'auth': get_auth}
        if interfacetype not in ['addprocess', 'updateprocess', 'updatestatus', 'queryPage']:
            self.log.error("interfacetype传入值不符合要求,请使用:'addprocess', 'updateprocess', 'updatestatus', 'queryPage'四个中的值")
            raise Exception("手动抛出异常,终止执行")

        # 新增流程
        if interfacetype == 'addprocess':
            if self.config.operating_environment == 'test':
                url = 'http://' + self.config.test_host + '/api/v1/globalsetting/process/insert'
            elif self.config.operating_environment == 'dev':
                url = 'http://' + self.config.dev_host + '/api/v1/globalsetting/process/insert'
            else:
                url = 'http://' + self.config.local_host
            data = {'name': self.name, 'code': self.code, 'nodeSetting': self.nodeSetting,
                    'status': self.status, 'comment': self.comment}

            self.log.debug('开始addprocess流程数据库检查,检查data传入code:{}是否存在'.format(self.code))
            #countcode = self.PySQL.docursor("select count(code) from toc_global_setting_process where code='{}'".format(self.code))
            fetcode = self.PySQL.fetchall("select code from toc_global_setting_process where code='{}'".format(self.code))
            if len(fetcode) == 0:
                self.log.debug('code:{}数据不存在数据库中')
            else:
                self.log.error('code:{}的数据已存在数据库中')
            self.log.debug('addprocess流程数据库检查结束')

        # 更新流程
        elif interfacetype == 'updateprocess':
            if self.config.operating_environment == 'test':
                url = 'http://' + self.config.test_host + '/api/v1/globalsetting/process/update'
            elif self.config.operating_environment == 'dev':
                url = 'http://' + self.config.dev_host + '/api/v1/globalsetting/process/update'
            else:
                url = 'http://' + self.config.local_host
            data = {'id': self.id, 'name': self.name, 'code': self.code, 'nodeSetting': self.nodeSetting,
                    'status': self.status, 'comment': self.comment}
            # 略过id为空的校验,防止更新接口id为空的测试场景被sql检查略过
            if data['id']:
                self.log.debug('开始updateprocess流程数据库检查,检查data传入id:{}是否存在'.format(self.id))
                # countid = self.PySQL.docursor("select count(id) from toc_global_setting_process where id='{}'".format(self.id))
                fetid = self.PySQL.fetchall("select id from toc_global_setting_process where id='{}'".format(self.id))
                if len(fetid) > 0:
                    self.log.info('库中查询到id={}的数据,继续执行更新流程接口')
                else:
                    self.log.error('库中没有找到id={}的数据,手动抛出异常,不执行更新流程接口')
                    raise Exception('手动抛出raise')
        # 更新流程状态
        elif interfacetype == 'updatestatus':
            if self.config.operating_environment == 'test':
                url = 'http://' + self.config.test_host + '/api/v1/globalsetting/process/updateStatus'
            elif self.config.operating_environment == 'dev':
                url = 'http://' + self.config.dev_host + '/api/v1/globalsetting/process/updateStatus'
            else:
                url = 'http://' + self.config.local_host
            data = {'id': self.id,
                    'status': self.status}

            self.log.debug('开始updatestatus流程数据库检查,检查data传入id:{}是否存在'.format(self.id))

            # countid = self.PySQL.docursor("select count(id) from toc_global_setting_process where id='{}'".format(self.id))
            fetid = self.PySQL.fetchall("select id from toc_global_setting_process where id='{}'".format(self.id))
            if len(fetid) > 0:
                self.log.info('库中查询到id={}的数据,继续执行更新流程状态接口')
            else:
                self.log.error('库中没有找到id={}的数据,手动抛出异常,不执行更新流程状态接口')
                raise Exception('手动抛出raise')
        # 分页查询
        elif interfacetype == 'queryPage':
            if self.config.operating_environment == 'test':
                url = 'http://' + self.config.test_host + '/api/v1/globalsetting/process/queryPage'
            elif self.config.operating_environment == 'dev':
                url = 'http://' + self.config.dev_host + '/api/v1/globalsetting/process/queryPage'
            else:
                url = 'http://' + self.config.local_host
            data = {'name': self.name, 'code': self.code,
                    'status': self.status, 'pageNum': self.pageNum, 'pageSize': self.pageSize}

            self.log.debug('queryPage无需检查库数据')

        self.log.info("\n当前执行流程:{},\n调用接口:{},\npost参数表单:{}".format(interfacetype, url, data))
        rsp = requests.post(url, json.dumps(data), headers=headers)
        try:
            rsp.raise_for_status()
        except Exception as e:
            print("调用:{}方法响应返回发现异常:{}".format(self.__class__.__name__, e))
            self.log.error("调用:{}方法响应返回发现异常:{}".format(self.__class__.__name__, e))
        else:
            if rsptype == 'json':
                return rsp.json()
            elif rsptype == 'raw':
                return rsp.raw
            elif rsptype == 'text':
                return rsp.text

    def after_run_check(self, rsp, interfacetype):
        """
        # 调用接口后的校验方法,检查数据库字段
        :param rsp:响应返回
        :param interfacetype:接口流程类型
        :return:
        """
        if rsp['error_code'] == 0:
            if interfacetype == 'addprocess':
                # 新增流程接口校验,只查询数据库中该code数据已写入库
                self.log.debug('新增流程接口校验,只查询数据库中该code数据已写入库')
                self.log.info('开始检查库')
                fetcode = self.PySQL.fetchall(sql="select * from toc_global_setting_process where code='{}'".format(self.code))
                if len(fetcode) > 0:
                    self.log.info('库中检查到该数据:{}'.format(fetcode))
                    self.log.info('新增流程接口校验结束,查询数据库中数据已写入库')
                    return True
                else:
                    self.log.error('库中未检查到该数据')
                    self.log.error('新增流程接口校验结束,查询数据库中数据写入库失败')
                    return False

            elif interfacetype == 'updateprocess':
                # 更新流程接口校验,只检查所有字段数据是否和修改字段数据一致
                pass

            elif interfacetype == 'updatestatus':
                # 更新流程状态接口,检查修改id的status状态字段
                self.log.debug('更新流程状态接口,检查修改id的status状态字段')
                self.log.info('开始检查库')
                fetstatus = self.PySQL.fetchall(sql="select status from toc_global_setting_process where id='{}'".format(self.id))
                if fetstatus == self.status:
                    self.log.info('status字段状态与data传入一致')
                    return True
                else:
                    self.log.error('status字段状态与data传入一致,库中status={},data传入status={}'.format(fetstatus, self.status))
                    return False
            elif interfacetype == 'queryPage':
                # 分页查询接口,检查list长度是否与data传入pageSize一致
                self.log.debug('分页查询接口,检查list长度是否与data传入pageSize一致')
                self.log.info('开始检查库')
                if self.pageSize == None:
                    pass
                self.log.warring('没有设置校验场景,人工检查')
                return True
        else:
            self.log.debug('接口响应返回失败,不执行调用接口后数据库检查')


def getinputdata(type, case, isaddallcode=False, **kwargs):
    inputlist = []
    # 新增流程
    if type == 'addprocess':
        inputdata = {'name': kwargs['name'], 'code': kwargs['code'], 'nodeSetting': kwargs['nodeSetting'],
                     'status': kwargs['status'], 'comment': kwargs['comment']}
        if case == 'smoke':
            pass
        elif case == 'name_is_null':
            inputdata['name'] = None
        elif case == 'code_is_null':
            inputdata['code'] = None
        elif case == 'nodeSetting_is_null':
            inputdata['nodeSetting'] = None
        elif case == 'status_is_null':
            inputdata['status'] = None
        elif case == 'comment_is_null':
            inputdata['comment'] = None
        inputlist.append(inputdata)
        return type, inputlist
    # 修改流程
    elif type == 'updateprocess':
        inputdata = {'id': kwargs['id'], 'name': kwargs['name'], 'code': kwargs['code'], 'nodeSetting': kwargs['nodeSetting'],
                     'status': kwargs['status'], 'comment': kwargs['comment']}
        if case == 'smoke':
            pass
        elif case == 'id_is_null':
            inputdata['id'] = None
        elif case == 'name_is_null':
            inputdata['name'] = None
        elif case == 'code_is_null':
            inputdata['code'] = None
        elif case == 'nodeSetting_is_null':
            inputdata['nodeSetting'] = None
        elif case == 'status_is_null':
            inputdata['status'] = None
        elif case == 'comment_is_null':
            inputdata['commet'] = None
        return type, inputdata
    # 更新流程状态
    elif type == 'updatestatus':
        inputdata = {'id': kwargs['id'], 'status': kwargs['status']}
        if case == 'smoke':
            pass
        elif case == 'id_is_null':
            inputdata['id'] = None
        elif case == 'status_is_null':
            inputdata['status'] = None
        return type, inputdata
    # 分页查询流程
    elif type == 'queryPage':
        inputdata = {'code': kwargs['code'], 'name': kwargs['name'], 'status': kwargs['status'],
                     'pageNum': kwargs['pageNum'], 'pageSize': kwargs['pageSize']}
        if case == 'smoke':
            pass
        elif case == 'code_is_null':
            inputdata['code'] = None
        elif case == 'name_is_null':
            inputdata['name'] = None
        elif case == 'status_is_null':
            inputdata['statis'] = None
        elif case == 'pageNum_is_null':
            inputdata['pageNum'] = None
        elif case == 'pageSize_is_null':
            inputdata['pageSize'] = None
        return type, inputdata

class RunTestCase():
    def __init__(self):
        self.rsp_status = False
        self.rep_fail = ''
        self.rspjson = ''

    def runtest(self):
        '''
        流程管理code字段码
        精准配种：ACCURATE_MATING    普通配种：NORMAL_MATING  粗放配种：ROUGH_MATING   上产床：NORMAL_PREFARROW
        背膘：NORMAL_BACKFAT   母猪淘汰：NORMAL_CULLING     母猪死亡：SOW_DEATH  小猪死亡：PIGLET_DEATH
        分娩：NORMAL_FARROW    孕检：NORMAL_PREGNANCY_DIAGNOSIS   母猪保健：SOW_HEALTH     小猪保健：PIGLET_HEALTH
        发情鉴定：NORMAL_HEAT    母猪免疫：SOW_IMMUNE     小猪免疫：PIGLET_IMMUNE      母猪断奶：NORMAL_WEANING
        仔猪断奶：PIGLET_WEANING     位置变动(转栏)：NORMAL_LOCATION_CHANGE
        '''
        log = Logging()
        # 流程管理code码
        code_alldict = ('ACCURATE_MATING', 'NORMAL_MATING', 'ROUGH_MATING', 'NORMAL_PREFARROW', 'NORMAL_BACKFAT', 'NORMAL_CULLING',
                        'SOW_DEATH', 'PIGLET_DEATH', 'NORMAL_FARROW', 'NORMAL_PREGNANCY_DIAGNOSIS', 'SOW_HEALTH',
                        'PIGLET_HEALTH', 'NORMAL_HEAT', 'SOW_IMMUNE', 'PIGLET_IMMUNE', 'NORMAL_WEANING', 'PIGLET_WEANING',
                        'NORMAL_LOCATION_CHANGE')

        inputcode = random.choice(code_alldict)     # 随机选取code码
        # 传入参数
        inputdata = {'id': 115, 'name': '新增流程测试', 'code': inputcode, 'nodeSetting': '开始-选猪精-配种-总结',
                     'status': 'ENABLE', 'comment': '这是新增流程的描述内容', 'pageNum': None, 'pageSize': None}

        # test = getinputdata(type='addprocess', case='smoke', **inputdata)     # 新增流程smoke测试场景<code存在和不存在两种场景>
        test = getinputdata(type='addprocess', case='name_is_null', **inputdata)      # 新增流程name为空测试场景
        # test = getinputdata(type='addprocess', case='code_is_null', **inputdata)      # 新增流程code为空测试场景
        # test = getinputdata(type='addprocess', case='nodeSetting_is_null', **inputdata)  # 新增流程nodeSetting为空测试场景
        # test = getinputdata(type='addprocess', case='status_is_null', **inputdata)  # 新增流程status为空测试场景
        # test = getinputdata(type='addprocess', case='comment_is_null', **inputdata)  # 新增流程comment为空测试场景
        # test = getinputdata(type='updateprocess', case='smoke', **inputdata)        # 修改流程接口smoke测试场景<所有字段内容与之前一样,修改code为已存在code>
        # test = getinputdata(type='updateprocess', case='id_is_null', **inputdata)   # 修改流程接口id为空测试场景
        # test = getinputdata(type='updateprocess', case='name_is_null', **inputdata)     # 修改流程接口name为空测试场景
        interfacetype = test[0]     # 流程接口类型
        interfacedata = test[1]     # 流程接口传入参数

        log.debug('*' * 30 + '这是分割线开始' + '*' * 30)
        # 列表新
        if isinstance(interfacedata, list):
            for data in interfacedata:
                log.info('调用接口传入data={}'.format(data))
                # 调用接口方法
                testprocess = ProcessAPI(data)
                self.rspjson = testprocess.run_case(interfacetype)
                if self.rspjson['error_code'] == 0:
                    # 调用校验检查方法
                    testprocess.after_run_check(rsp=self.rspjson, interfacetype=interfacetype)
                    log.info('接口响应返回成功')
                    log.info('接口返回内容:{}'.format(self.rspjson))
                    self.rsp_status = True
                else:
                    log.debug('接口响应返回失败,不调用数据库校验检查方法')
                    log.error('接口返回内容:{}'.format(self.rspjson))
                    log.error('接口返回错误码:{}'.format(self.rspjson['error_code']))
                    log.error('接口返回错误内容:{}'.format(self.rspjson['error_msg']))
        else:
            log.info('调用接口传入data={}'.format(interfacedata))
            # 调用接口方法
            testprocess = ProcessAPI(interfacedata)
            self.rspjson = testprocess.run_case(interfacetype)
            if self.rspjson['error_code'] == 0:
                # 调用校验检查方法
                testprocess.after_run_check(rsp=self.rspjson, interfacetype=interfacetype)
                log.info('接口响应返回成功')
                log.info('接口返回内容:{}'.format(self.rspjson))
                self.rsp_status = True
            else:
                log.debug('接口响应返回失败,不调用数据库校验检查方法')
                log.error('接口返回内容:{}'.format(self.rspjson))
                log.error('接口返回错误码:{}'.format(self.rspjson['error_code']))
                log.error('接口返回错误内容:{}'.format(self.rspjson['error_msg']))
        log.debug('*' * 30 + '这是分割线结束' + '*' * 30)

    # def rsp_check(self, error_code, error_msg):
    #     """
    #     # 响应返回与预期校验
    #     :param runtest_rst: 调用runtest方法的返回结果
    #     :return:
    #     """
    #     log = Logging()
    #     log.info('开始调用{}'.format(self.rsp_check.__name__))
    #     # 响应返回成功
    #     if self.rsp_status:





if __name__ == '__main__':
    run = RunTestCase()
    run.runtest()



