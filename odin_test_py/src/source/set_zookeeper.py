# -*- coding: utf-8 -*-
# @Time    : 2018-11-24 09:29
# @Author  : odin_y
# @Email   : 
# @File    : set_zookeeper.py
# @Software: PyCharm
# @Comment : zookeeper连接

import json
from kazoo.client import KazooClient, KazooState


class ZK:
    def __init__(self):
        self.zk_host = '172.19.100.40:2181,172.19.100.40:2182,172.19.100.40:2183'
        self.timeout = 100
        self.path = "/task_orchestration_center/taskConfig/global"

        self.zk = KazooClient(hosts=self.zk_host)
        self.zk.start()

    def jd_is_exists(self, path):
        # 判断节点是否存在
        if self.zk.exists(self.path + path):
            print (self.path + path, "存在")
        else:
            # 建立节点，成功后返回新节点路径
            childrenPath = self.zk.create(path + path, "test111")
            print ("创建节点：", childrenPath, "成功。")
            # 创建临时节点，连接断开则节点自动删除
            self.zk.create(path+"/test999", "test999", ephemeral=True)

    def zk_listener(self):
        if self.zk.state == 'LOST':
            print("is LOST")
        elif self.zk.state == "SUSPENDED":
            print("is SUSPENDED")

    def zk_get_children(self, path):
        print(self.zk.get_children(path))

    def set_zk(self, tenantid, value, type='mating', *args, **kwargs):
        if args:
            path1 = '/task_orchestration_center/taskConfig/global/tenantid_{}/operationUnitid_{}/{}'.format(tenantid, args[0], type)
        else:
            path1 = '/task_orchestration_center/taskConfig/global/tenantid_{}/{}'.format(tenantid, type)
        self.zk.set(path1, value)

    def creat_zk(self, path, addpath):
        self.zk.create(path, addpath)

    def stop_zk(self):
        self.zk.stop()


if __name__ == '__main__':
    run = ZK()
    run.zk_listener()
    children = run.zk.get_children('/task_orchestration_center/taskConfig/global/')
    print(children)
    run.zk_get_children('/task_orchestration_center/taskConfig/global/tenant_1192178272108020742/')