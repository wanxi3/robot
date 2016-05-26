# coding=utf-8
__author__ = 'libin'

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from ios import app_suite_data as ios_data
from android import app_suite_data as android_data
from collections import OrderedDict
from common import *

import httplib
import json
import socket


def data_make_up(result,site,host,type,data):
    if site == 'online':
        site_data = result[site][host][type]
    else:
        site_data = result[site][type]

    if data['socket_code']:
        site_data['code'] = data['socket_code']
        site_data['msg'] = '本地服务未开启，请启动本地服务'
    else:
        code = data['code']
        if code == -1:
            site_data['code'] = data['code']
            site_data['msg'] = data['msg'].encode('utf-8')
        elif code == -2 and type == 'ios':
            site_data['code'] = data['code']
            site_data['msg'] = data['msg'].encode('utf-8')
        else:
            if len(data[u'data'][type]['undo_devices']) == 0 and len(data[u'data'][type]['do_devices']) == 0:
                site_data['code'] = -1
                site_data['msg'] = '未找到相关设备，请再次确认设备是否已经正常连接到本地'

        site_data['do_devices'] = data['data'][type]['do_devices']
        for device in data['data'][type]['undo_devices']:
            f = True
            for f_device in Devices.device_data[host][type]['finish_devices']:
                if device['udid'] == f_device['udid']:
                    f = False
                    break
            if f:
                site_data['undo_devices'].append(device)

        site_data['finish_devices'] = Devices.device_data[host][type]['finish_devices']

    return result



def app_phone_data(request):
    result = init_appphonedata_result()

    type = ''
    if request.method == "GET":
        type = request.GET.get("type")
    host = request.META['REMOTE_ADDR']
    result['local']['host'] = host
    if host not in Devices.all_host:
        Devices.all_host.append(host)

    #删除没有打开remote_server的host
    for each_host in deepcopy(Devices.all_host):
        if each_host == SERVERHOST: #保证服务器始终在host列表里
            continue
        if not isOpen(each_host):
            Devices.all_host.remove(each_host)

    for each_host in Devices.all_host:
        app_object = AppManager(each_host)
        data = app_object.communicate("POST","init_data",Devices.device_data[each_host][type])
        if data['socket_code'] == 0:
            data = phone_data_parsing(data)
            if not Devices.host_name.has_key(each_host):
                Devices.host_name.setdefault(each_host,data['hostname'])
        #判断该host是不是属于本机
        if each_host == host:
            site = 'local'
            result['local']['host'] = each_host
        #判断该host是不是属于服务器
        elif each_host == SERVERHOST:
            site = 'server'
            result['server']['host'] = each_host
        #其他都归类为online
        else:
            site = 'online'
            result["online"].setdefault(each_host,deepcopy(DataStructInit.ONLINESTRUCT))
            result["online"][each_host]["host"] = each_host
            result["online"][each_host]["hostname"] = Devices.host_name[each_host] if Devices.host_name.has_key(each_host) else ""

        result = data_make_up(result,site,each_host,type,data)



        if data.has_key('data'):
            Devices.device_data[each_host][type]['do_devices'] = data['data'][type]['do_devices']
            Devices.device_data[each_host][type]['undo_devices'] = data['data'][type]['undo_devices']
            Devices.device_data[each_host]['hostname'] = data["hostname"]
    if request.method == "GET":
        if type == 'android':
            return render_to_response("android.html", locals(), context_instance=RequestContext(request))
        else:
            return render_to_response("ios.html", locals(), context_instance=RequestContext(request))

    elif request.method == 'POST':

        response = HttpResponse(json.dumps(result), content_type="application/json")
        response['Access-Control-Allow-Origin'] = '*'
        return response

def app_suite_data(request):
    if request.method == "GET":
        platfrom = request.GET.get("platfrom")
        if platfrom == 'android':
            response = HttpResponse(json.dumps(android_data.suite_data), content_type="application/json")
        elif platfrom == 'ios':
            response = HttpResponse(json.dumps(ios_data.suite_data), content_type="application/json")
        response['Access-Control-Allow-Origin'] = '*'
        return response

def phone_data_parsing(data):
    new_data = {'android':{},'ios':{}}
    for each_class,each_data in data['data'].iteritems():
        new_data['ios'].setdefault(each_class,[])
        new_data['android'].setdefault(each_class,[])
        for each_phone in each_data:
            #ios
            if len(each_phone['udid']) == 40:
                new_data['ios'][each_class].append(each_phone)
            else:
                new_data['android'][each_class].append(each_phone)
    data['data'] = new_data
    return data

#每台机子的remote开启,都向服务端发host
def each_phone(request):
    if request.method == "POST":
        host = request.META['REMOTE_ADDR']
        if host not in Devices.all_host:
            Devices.all_host.append(host)
        post_data = json.loads(request.body)
        hostname = post_data.get('hostname','')
        Devices.host_name.setdefault(host,hostname)
        response = HttpResponse("success", content_type="application/json")
        response['Access-Control-Allow-Origin'] = '*'
        return response

#设置自己本地手机在别人那的显示状态
def set_phone_state(request):
    if request.method == "POST":
        post_data = json.loads(request.body)
        Devices.phone_state = post_data.get("phone_state",{})
        #{host:{udid:True,udid:False,},}

        response = HttpResponse("success", content_type="application/json")
        response['Access-Control-Allow-Origin'] = '*'
        return response















