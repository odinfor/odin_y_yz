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


class UseingExcel:
    """ Excel 文件操作类"""
    log = Logging()
    config = Config()
    apifile = os.path.join(config.refdata_dir, 'test_api_resquest.xls')

    def open_excel(self):
        """#打开test_api_resquest.xlsx"""
        try:
            data = xlrd.open_workbook(self.apifile)
        except Exception as e:
            self.log.error(u"发现异常:%s" % e)
        else:
            return data

    def excel_byindex(self, colnameindex=1, byindex=0):
        """
        #根据索引获取Excel表中的数据
        #colnameindex:表头所在的行 ，byindex:表的索引
        :param colnameindex:表头列名所在行的所以
        :param byindex:表的索引
        """
        data = self.open_excel()
        # 表的sheet
        table = data.sheets()[byindex]
        # 表的行与列
        nrows = table.nrows
        ncols = table.ncols
        # 表某一行数据
        colsname = table.row_values(colnameindex)

        list = []
        for rownum in range(2, nrows):
            row = table.row_values(rownum)
            if row:
                app = {}
                for i in range(len(colsname)):
                    app[colsname[i]] = row[i]
                list.append(app)
        return list

    def excel_table_byname(self, colnameindex=1, by_name=u'test_api'):
        """
        #根据名称获取Excel表格中的数据
        :param colnameindex:表头列名所在行的所以
        :param by_name:Sheet1名称
        """
        data = self.open_excel()
        table = data.sheet_by_name(by_name)
        # 行数
        nrows = table.nrows
        print
        nrows
        # 某一行数据
        colnames = table.row_values(colnameindex)
        list = []
        for rownum in range(2, nrows):
            row = table.row_values(rownum)
            if row:
                app = {}
                for i in range(len(colnames)):
                    app[colnames[i]] = row[i]
                    list.append(app)
        return list

    def set_style(self, patternid, fontid, bold=False, center=None, wrap=0):
        """
        #初始化样式
        :param patternid:单元格背景颜色id
        ":param fontid:字体颜色id
        :param bold:字体是否加粗<默认不加粗>
        :param cneter:单元格居中方式,<默认不设置,'horz':水平居中,'vert':垂直居中,'all':水平和垂直居中>
        """

        # 单元格背景颜色设置为黑色
        pattern = xlwt.Pattern()  # 创建一个模式
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # 设置其模式为实型
        # 设置单元格背景颜色 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta,  the list goes on...
        pattern.pattern_fore_colour = patternid
        # 单元格字体颜色
        fnt = xlwt.Font()  # 创建一个文本格式，包括字体、字号和颜色样式特性
        fnt.name = u'微软雅黑'  # 设置其字体为微软雅黑
        fnt.colour_index = fontid  # 设置其字体颜色
        fnt.bold = bold  # 设置其字体加粗

        # 设置居中格式
        alignment = xlwt.Alignment()
        if center == None:
            pass
        elif center == 'horz':
            alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平居中
        elif center == 'vert':
            alignment.vert = xlwt.Alignment.VERT_CENTER  # 垂直居中
        elif center == 'all':
            alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平居中
            alignment.vert = xlwt.Alignment.VERT_CENTER  # 垂直居中

        # 设置单元格边框,DASHED:虚线/NO_LINE:没有/THIN:实线
        broders = xlwt.Borders()
        broders.left = xlwt.Borders.THIN
        broders.right = xlwt.Borders.THIN
        broders.top = xlwt.Borders.THIN
        broders.bottom = xlwt.Borders.THIN
        # 边框颜色
        broders.left_colour = 0x3A
        broders.right_colour = 0x3A
        broders.top_colour = 0x3A
        broders.bottom_colour = 0x3A

        # 设置自动换行
        if wrap == 0:
            pass
        elif wrap == 1:
            alignment.wrap = 1

        style = xlwt.XFStyle()
        # 将赋值好的模式参数导入Style
        style.pattern = pattern
        style.font = fnt
        style.alignment = alignment
        style.broders = broders
        return style

    def api_result_excel(self, explain, msg_request, msg_return, is_pass=[], check_explain=None,
                         csvfile='test_api_resquest.xlsx'):
        """
        #接口执行结果写入excel文件
        #explain:说明,msg_request:请求参数,msg_return:返回,is_pass:是否通过
        #explain/msg_request/msg_return列表类型
        """
        # 接口执行结果写入文件路径
        excel_dir = self.config.excel_dir + '\\' + 'api_result.xls'
        try:
            # 创建xls文件对象
            wb = xlwt.Workbook(encoding='utf-8')
            """
            #打开excel文件
            openfile = xlrd.open_workbook(excel_dir)
            """
        except Exception as e:
            self.log.error(u"%s" % e)
        else:
            # 创建sheet
            sheet1 = wb.add_sheet(u'api_results', cell_overwrite_ok=True)
            """#第一行"""
            # 写入单元格内容
            sheet1.write_merge(0, 0, 0, 5, u"接口执行结果", self.set_style(21, 1, bold=True))
            """#第二行"""
            sheet1.write_merge(1, 1, 0, 5, u"使用get/post请求,打印返回", self.set_style(21, 1, bold=True))
            """#第三行"""
            # 标题行
            row3 = ['ID', u'说明', u'请求参数', u'返回', u"是否通过", u"校验说明"]
            for i in row3:
                # 设置列宽
                if row3.index(i) == 1:
                    consol = sheet1.col(row3.index(i))
                    consol.width = 256 * 40
                if row3.index(i) == 2 or row3.index(i) == 3:
                    consol = sheet1.col(row3.index(i))
                    consol.width = 256 * 80
                if row3.index(i) == 5:
                    consol = sheet1.col(row3.index(i))
                    consol.width = 256 * 50
                sheet1.write(2, row3.index(i), i, self.set_style(20, 1, bold=True, center='horz'))
            """#写入行"""
            # 自增变量
            indexid = 0
            # 起始行
            row_start = 2
            # test_api_request.xlsx文件配置行数
            data = xlrd.open_workbook(self.config.excel_dir + '\\' + csvfile)
            table = data.sheets()[0]
            nrows = table.nrows
            while True:
                indexid += 1
                row_start += 1
                if row_start > (len(msg_return) + 2):
                    break
                else:
                    # caseid自增id写入
                    sheet1.write(row_start, 0, indexid, self.set_style(1, 0, center='all'))
                    # 写入说明
                    sheet1.write(row_start, 1, explain[indexid - 1], self.set_style(1, 0, center='vert'))
                    # 写入参数
                    sheet1.write(row_start, 2, msg_request[indexid - 1], self.set_style(1, 0, center='vert', wrap=1))
                    # 写入返回
                    sheet1.write(row_start, 3, msg_return[indexid - 1], self.set_style(1, 0, center='vert', wrap=1))
                    # 写入是否通过,通过则标绿色底色,未通过则标红色底色
                    if is_pass == []:
                        sheet1.write(row_start, 4, '', self.set_style(23, 0))
                    else:
                        if (indexid) > len(is_pass):
                            raise (u"test_api_request.xlsx文件code字段有未填项")
                        else:
                            if is_pass[indexid - 1]:
                                sheet1.write(row_start, 4, '√', self.set_style(3, 0, center='all'))
                            elif is_pass[indexid - 1] == None:
                                sheet1.write(row_start, 4, '', self.set_style(23, 0))
                            else:
                                sheet1.write(row_start, 4, '×', self.set_style(2, 0, center='all'))
                    # 写入校验说明
                    if check_explain == None:
                        pass
                    else:
                        sheet1.write(row_start, 5, check_explain[indexid - 1],
                                     self.set_style(1, 0, center='all', wrap=1))
            try:
                wb.save(excel_dir)
            except Exception as e:
                self.log.error(u"先关闭文件api_result.xls")
                raise e


if __name__ == "__main__":
    # test = Base_Method()
    # exceldict = test.get_excel_content()
    # print(exceldict)
    a = 'aaa'
    c = ('g', '1')
    print(a.join(c))
