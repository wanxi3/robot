# -*- coding: utf-8 -*-
__author__ = 'libin'

from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from robot.parsing import TestCaseFile, TestDataDirectory, ResourceFile, TestData

import os
import json

def new_test_case(request):
    if request.method == "GET":
        source = ""
        case_name = ""
        data = TestData(source=source)
        data.testcase_table.add(case_name)

        data.save(format='html')
        #刷新一下主界面

        r = HttpResponse(json.dumps({
            "message": "创建成功",
            }))
        r["Content-Type"] = "application/json; charset=utf-8"
        return r



