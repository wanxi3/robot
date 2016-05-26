# coding=utf-8
__author__ = 'libin'

from django.http import HttpResponse

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def output(request):
    if request.method == "GET":
        flag = True
        message = u"正常"
        timestamp = request.GET.get("timestamp","")
        if not timestamp:
            message = u"没有找到时间戳"
        else:
            path = '/Users/libin/rfs_in_cloud2/static/report/'
            path += (timestamp + "/listen.txt")
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
