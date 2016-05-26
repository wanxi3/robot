# -*- coding: utf-8 -*-
__author__ = 'libin'

from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from robot.parsing import TestCaseFile, TestDataDirectory, ResourceFile, TestData

import os
import json

def new_resource(request):
    if request.method == "GET":
        name = ''
        in_path = ""
        out_path = ""
        in_file = open(in_path,'rb')
        out_file = open(out_path,'wb')
        out_file.write(in_file.read().replace("Baseresource",name))
        in_file.close()
        out_file.close()
        data = TestData(source=out_path)
        data.save(format='html')
        #刷新一下主页
        r = HttpResponse(json.dumps({
            "message": "创建resource成功",
        }))
        r["Content-Type"] = "application/json; charset=utf-8"
        return r