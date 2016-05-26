# coding=utf-8
__author__ = 'libin'

from collections import OrderedDict
from copy import deepcopy

import httplib
import socket
import json

SERVERHOST = '192.168.13.32'


def isOpen(host):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    flag = True
    try:
        sk.connect((host,5411))
    except Exception:
        flag = False
    sk.close()
    return flag

class AppManager(object):

    def __init__(self,host):
        self.data = {}
        self.host = host

        Devices.device_data.setdefault(host,
                                       {'android':deepcopy(DataStructInit.DEVICESANDROIDSTRUCT),
                                       'ios':deepcopy(DataStructInit.DEVICESIOSSTRUCT),
                                       "hostname":"",}
                                       )

    def communicate(self,type,message,data = {}):
        result = {}
        if not isOpen(self.host):
            result['socket_code'] = 60
            return result

        url = message
        conn = httplib.HTTPConnection(self.host,5411)
        try:
            conn.request(method=type,url=url,body=json.dumps(data))
            response = conn.getresponse()
            result = json.loads(response.read())
            result['socket_code'] = 0
        except socket.error,e:
            errno,err_msg = e
            result['socket_code'] = errno
        return result

class DataStructInit(object):
    '''

    '''
    BASESTRUCT = \
        {
            'do_devices':[],
            'undo_devices':[],
            'select_devices':[],
            'ready_devices': [],
            'finish_devices':[],
            'err_devices':[],
        }

    basestruct_copy = deepcopy(BASESTRUCT)

    DEVICESANDROIDSTRUCT = deepcopy(BASESTRUCT)
    DEVICESIOSSTRUCT = deepcopy(BASESTRUCT)

    basestruct_copy.setdefault("code",0)
    basestruct_copy.setdefault("msg","")

    init_base = \
        {
            'android':deepcopy(basestruct_copy),
            'ios':deepcopy(basestruct_copy),
            'host':""
        }

    LOCALSTRUCT = deepcopy(init_base)
    SERVERSTRUCT = deepcopy(init_base)

    #由于online的数据结构还需要在init_base数据结构前加上一个host的key值,所以此处的数据结构并非最终的结构
    init_base.setdefault("hostname","")
    ONLINESTRUCT = deepcopy(init_base)

class Devices(object):

    device_data = {} #用于存储在线的手机状态
    all_host = [SERVERHOST] #收集remote_server发送过来的host
    phone_state = {} #online中的手机列表属性(显示or不显示)
    phone_type = {} #手机列表的属性信息,目前只存储了手机的归属(本机 or 服务器 or online) {"udid":{"site":"local"}}
    host_name = {}


def init_appphonedata_result():
    result = OrderedDict()
    result["local"] = deepcopy(DataStructInit.LOCALSTRUCT)
    result["server"] = deepcopy(DataStructInit.SERVERSTRUCT)
    result["online"] = {} #最终的初始化将会在逻辑函数里面处理
    return result

