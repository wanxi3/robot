# coding=utf-8
__author__ = 'libin'

from django.http import HttpResponse

import os
import json


def output(request):
    if request.method == "GET":
        username = request.user.username
        base_path = os.path.dirname(__file__)
        reportpath = os.path.join(base_path,"../../../static/report/")
        reportpath = os.path.join(reportpath,username)
        flag = True
        message = u"正常"
        timestamp = request.GET.get("timestamp","")
        if not timestamp:
            message = u"没有找到时间戳"
        else:
            path = os.path.join(reportpath,timestamp)
            path = os.path.join(path,'stdout.txt')
            with open(path,"r+") as stdout:
                lines = stdout.readlines()
                if lines:
                    if lines[-1].find('Report') != -1:
                        flag = False
        r = HttpResponse(json.dumps({
                "output": lines,
                "flag": flag,
                "message":message,
        }))
        r["Content-Type"] = "application/json; charset=utf-8"
        return r
