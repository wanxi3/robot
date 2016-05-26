# coding=utf-8

__author__ = 'libin'

from django.http import HttpResponse
from rfs_web.app.android.Case import Case
from app_phone_data import Devices,AppManager
from app_phone_data import phone_data_parsing
from ios import app_suite_data as ios_data
from android import app_suite_data as android_data
from common import *
from copy import deepcopy

import copy
import json
import threading
import time
import traceback

class RunDevices(object):
    '''
        {udid:{'obj':obj,'thread':t}
    '''
    devices_data = {}

def run(data,host,case_dict,type):
    # host = 'localhost' if host == '127.0.0.1' else host
    udid = data['udid']
    port = data['port']
    name = data['name']
    if type == 'android':
        obj = Case('Android','4.3','',udid,'com.tongbanjie.android','TBJWelcomeActivity',host,int(port))
        case_match = android_data.case_match
    elif type == 'ios':
        obj = Case('IOS','7.1','',udid,'','',host,int(port),bundleId='com.tongbanjie.pro')
        case_match = ios_data.case_match
    else:
        return False
    if obj.init_drive_error:
        return obj.init_drive_error
    for each_suite,each_case in case_dict.items():
        for case_name in each_case:
            try:
                function_name = case_match[each_suite.encode('utf-8')][case_name.encode('utf-8')]
                obj.add_case(case_name,eval('obj.'+function_name))
            except:
                print "err case data: ",each_suite,case_name

    def run_case_daemon():
        stdout = obj.run()

    def check_case_is_finished():
        while True:
            if obj.finish_flag:
                device = {"name":name,"port":port,'udid':udid}
                Devices.device_data[host][type]['do_devices'].remove(device)
                Devices.device_data[host][type]['finish_devices'].append(device)
                app_object = AppManager(host)
                app_object.communicate('POST','finish_devices',Devices.device_data[host][type])
                break
            time.sleep(1)

    t = threading.Thread(target=run_case_daemon,name='')
    t.setDaemon(True)
    t.start()

    t1 = threading.Thread(target=check_case_is_finished,name='')
    t1.setDaemon(True)
    t1.start()

    Devices.phone_type.setdefault(udid,{})
    Devices.phone_type[udid]['host'] = host

    RunDevices.devices_data.setdefault(udid,{'obj':obj,'thread':t,'name':name, 'port':port})
    return False

def run_app_case(request):
    result = {}
    result.setdefault('android',deepcopy(DataStructInit.basestruct_copy))
    result.setdefault('ios',deepcopy(DataStructInit.basestruct_copy))

    if request.method == "POST":
        try:
            host = request.META['REMOTE_ADDR']
            case_dict = {}
            type = ''
            phone_list = {}
            post_data = json.loads(request.body)
            for key,value in post_data.iteritems():
                if key == 'case_dict':
                    case_dict = value
                elif key == 'type':
                    type = value
                else:
                    phone_list[key] = value

            for each_host,p_list in phone_list.iteritems():
                app_object = AppManager(each_host)
                Devices.device_data[each_host][type]['select_devices'] = p_list

                copy_finish_devices = copy.deepcopy(Devices.device_data[host][type]['finish_devices'])
                for each_device in p_list:
                    for do_device in Devices.device_data[each_host][type]['do_devices']:
                        if each_device['udid'] == do_device['udid']:
                            Devices.device_data[each_host][type]['select_devices'].remove(each_device)
                    for finish_device in copy_finish_devices:
                        if each_device['udid'] == finish_device['udid']:
                            Devices.device_data[each_host][type]['finish_devices'].remove(finish_device)
                            if RunDevices.devices_data.has_key(each_device['udid']):
                                del RunDevices.devices_data[each_device['udid']]

                    data = app_object.communicate("POST","fetch_appium_port",Devices.device_data[each_host][type])
                    data = phone_data_parsing(data)
                    Devices.device_data[each_host][type]['select_devices'] = []
                    Devices.device_data[each_host][type]['do_devices'] = copy.deepcopy(data['data'][type]['do_devices'])
                    Devices.device_data[each_host][type]['undo_devices'] = copy.deepcopy(data['data'][type]['undo_devices'])

                    if not data['code']:
                        for each_ready in data['data'][type]['ready_devices']:
                            udid = each_ready['udid']
                            port = each_ready['port']
                            name = each_ready['name']
                            errmsg = run(each_ready,each_host,case_dict,type)
                            if errmsg:
                                t = {}
                                result[type].setdefault('err_devices',[])
                                t.setdefault('udid',udid)
                                t.setdefault('port',port)
                                t.setdefault('name',name)
                                t.setdefault('msg',errmsg)
                                for each_do in Devices.device_data[each_host][type]['do_devices']:
                                    if each_do['udid'] == udid:
                                        Devices.device_data[each_host][type]['do_devices'].remove(each_do)
                                        Devices.device_data[each_host][type]['err_devices'].append(each_do)
                                        result[type]['err_devices'].append(t)
                                        break
                        if result[type]['err_devices']:
                            app_object.communicate("POST","err_devices",Devices.device_data[each_host][type])
                        Devices.device_data[each_host][type]['err_devices'] = []

                    #返回do undo
                    if data['socket_code']:
                        result[type]['code'] = data['socket_code']
                        result[type]['msg'] = '本地服务未开启，请启动本地服务'
                    else:
                        code = data['code']
                        if code:
                            result[type]['code'] = code
                            result[type]['msg'] = data['msg'].encode('utf-8')
                        else:
                            result[type]['do_devices'] = copy.deepcopy(Devices.device_data[each_host][type]['do_devices'])
                            result[type]['undo_devices'] = copy.deepcopy(Devices.device_data[each_host][type]['undo_devices'])
                            result[type]['offline_devices'] = copy.deepcopy(data['data'][type]['offline_devices'])
            print "="*50
            print result
            print "="*50

            response = HttpResponse(json.dumps(result), content_type="application/json")
            response['Access-Control-Allow-Origin'] = '*'
        except:
            traceback.print_exc()
            response = {}
        return response

def app_report(request):
    if request.method == "POST":
        post_data = json.loads(request.body)
        type = post_data.get("type",'')
        platform = post_data.get('platform','')

        result = {}
        line = []
        host = request.META['REMOTE_ADDR']
        result['data'] = []

        result['flag'] = False if Devices.device_data[host][platform]['do_devices'] else True
        try:
            if type == 'line':
                for udid,data in RunDevices.devices_data.iteritems():
                    line = data['obj'].stdout.readline()
                    finish_flag = data['obj'].stdout.mark_finish
                    if not data['obj'].stdout.mark_finish:
                        result['flag'] = data['obj'].stdout.mark_finish
                    result['data'].append({'udid':udid,"line":line,'name':data['name'],"flag":finish_flag})
            else:
                udid_list = post_data.get('udid_list',[])

                for udid in udid_list:
                    data = RunDevices.devices_data[udid]
                    line = data['obj'].stdout.mark_read
                    finish_flag = data['obj'].stdout.mark_finish
                    if not data['obj'].stdout.mark_finish:
                        result['flag'] = data['obj'].stdout.mark_finish
                    result['data'].append({'udid':udid,"line":line,'name':data['name'],"flag":finish_flag})
            result['code'] = 0

        except Exception,e:
            traceback.print_exc()
            result['code'] = 1
        response = HttpResponse(json.dumps(result), content_type="application/json")
        response['Access-Control-Allow-Origin'] = '*'
        return response


