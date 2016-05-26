# -*- coding: utf-8 -*-
__author__ = 'libin'

from django.http import HttpResponse

import os
import json

def report(request):
    if request.method == 'GET':
        result = []
        flag = True
        username = request.user.username
        path = os.path.dirname(__file__)
        base_path = os.path.join(path,"../../../static/report/")
        report_path = os.path.join(base_path,username)
        try:
            report_list = os.listdir(report_path)
        except Exception,e:
            flag = False

        if flag:
            if '.DS_Store' in report_list:
                report_list.remove('.DS_Store')
            report_list.sort(reverse=True)
            for report_name in report_list:
                each_report = {}
                each_report['name'] = report_name
                each_report['path'] = "/static/report/" + username + '/' + report_name + "/report.html"
                result.append(each_report)

        r = HttpResponse(json.dumps(result))
        r["Content-Type"] = "application/json; charset=utf-8"
        return r
