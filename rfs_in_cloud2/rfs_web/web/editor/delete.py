# -*- coding: utf-8 -*-
__author__ = 'libin'

from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from robot.parsing import TestCaseFile, TestDataDirectory, ResourceFile, TestData

import os
import json

def delete(request):
    if request.method == "GET":
        delete_type = request.method.GET("type")
        path = request.method.GET("path")
        name = request.method.GET("name")
        if delete_type == 'suite':
            os.remove(path)
        if delete_type == 'case':
            data = TestData(source=path)
            for each_case in data.testcase_table:
                if each_case.name == name:
                    data.testcase_table.tests.remove(each_case)
                    data.save(format='html')
        if delete_type == "resource":
            os.remove(path)
        if delete_type == "resource_case":
            data = ResourceFile(source=path).populate()
            pass
