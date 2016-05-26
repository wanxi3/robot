# -*- coding: utf-8 -*-
__author__ = 'libin'

from robot import run
from django.http import HttpResponse

import json
import os
import threading
import time
import datetime
import subprocess


class RunData(object):
    caseId = 0
    CaseData = {}

    def __init__(self):
        RunData.caseId += 1
        RunData.CaseData.setdefault(
            str(RunData.caseId), {"datasources": None, "options": None})


def run_case_api(request):
    """
    执行test case
    :param request:
    :return:

    post_data = {
        "sources":["D:/libin//Robot/testcases"],
        "testcases":["testcases.我的资产.html.未登录用户","testcases.我的资产.html.一登陆"],
        "include":[],
        "exclude":[],
        "loglevel":"TRACE"}
    """
    result = True
    message = u""
    data = {}
    timestamp = ""
    username = request.user.username
    # LISTENER = 'F:/cat/rfs_in_cloud3/static' + '/resource_home/' + username + '/Listener.py'
    LISTENER = os.path.join(
        os.path.dirname(__file__),
        '../../static/resource_house',
        username,
        'Listener.py')

    if not request.body:
        result = False
        message = u"请求报文不能为空"
    else:
        try:
            post_data = json.loads(request.body)

            sources = post_data.get("sources", [])
            test_cases = post_data.get("testcase", [])
            # todo 这里
            test_cases2 = []
            for each_test in test_cases:
                test_cases2.append('testcase' + each_test)
            test_cases = test_cases2
            if not sources:
                result = False
                message = u"sources不能为空"
            else:
                path = os.path.dirname(__file__)
                # 创建输出文件夹
                reportpath = os.path.join(path, "../../../static/report/")
                runcase_data_path = os.path.join(
                    path, '../../../static/runcase_data/')
                flag = True
                for each_dir in os.listdir(reportpath):
                    if each_dir == username:
                        flag = False
                        break

                reportpath = os.path.join(reportpath, username)
                if flag:
                    try:
                        os.mkdir(reportpath.decode('utf-8').encode('gb18030'))
                    # except WindowsError,e:
                    except ValueError as e:
                        result = False
                        message = u"创建输出文件夹" + reportpath + u"失败：" + e.message
                timestamp = time.mktime(datetime.datetime.now().timetuple())
                output_path = os.path.join(reportpath, str(timestamp)[:-2])
                try:
                    os.mkdir(output_path.decode('utf-8').encode('gb18030'))
                # except WindowsError,e:
                except ValueError as e:
                    result = False
                    message = u"创建输出文件夹" + output_path + u"失败：" + e.message
                if result:
                    stdout_path = os.path.join(output_path, "stdout.txt")
                    stderr_path = os.path.join(output_path, "stderr.txt")
                    data_path = os.path.join(
                        runcase_data_path, '%s.%s.txt' %
                        (str(timestamp)[
                            :-2], username))

                    # listen_path = os.path.join(output_path,"listen.txt")
                    listen_path = output_path + "/listen.txt"

                    def run_case_daemon():
                        stdout = open(stdout_path, "w")
                        stderr = open(stderr_path, "w")
                        stdoptions = open(data_path, 'w')

                        datasources = sources
                        # test_cases = ','.join(test_cases).decode('utf-8').encode('utf-8')
                        # test_cases = test_cases.split(',')
                        options = {"test": test_cases,
                                   "outputdir": output_path,
                                   "stdout": stdout_path,
                                   "stderr": stderr_path,
                                   # "listener": LISTENER + ":" + listen_path + ":" + "TRACE",
                                   }
                        stdoptions.write(str(options))
                        stdoptions.close()
                        # run_code = run(datasources, **options)
                        # stdout.close()
                        # stderr.close()
                        # return run_code
                        # options = "'''" + json.dumps(options) + "'''"
                        subprocess.Popen(
                            'python rfs_web/web/running/run_case_process.py %s %s.%s.txt' %
                            (sources, str(timestamp)[
                                :-2], username), shell=True)
                        # subprocess.Popen('python rfs_web/web/running/run_case_process.py {0} {1}'.format(datasources,options),shell=True)
                    run_case_daemon()

                    # t = threading.Thread(target=run_case_daemon,name=timestamp)
                    # t.setDaemon(True)
                    # t.start()
        except ValueError as e:
            result = False
            message = u"无法解析的报文格式：" + e.message

    r = HttpResponse(json.dumps({
        "result": result,
        "message": message,
        "timestamp": timestamp
    }))
    r["Content-Type"] = "application/json; charset=utf-8"
    return r
