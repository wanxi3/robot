# -*- coding: utf-8 -*-
__author__ = 'libin'

from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from robot.parsing import TestCaseFile, TestDataDirectory, ResourceFile, TestData

import os
import json


def suite_save(request):
    if request.method == "GET":
        file_data = request.method.GET("file_data")

        path = file_data["path"]
        #setings
        settings = file_data["settings"]
        doc = settings["doc"]
        suite_setup = settings["suite_setup"]
        suite_teardown = settings["suite_teardown"]
        test_setup = settings["test_setup"]
        test_teardown = settings["test_teardown"]
        test_timeout = settings["test_timeout"]
        force_tags = settings["force_tags"]
        default_tags = settings["default_tags"]
        imports = settings["imports"]
        #testcases
        testcases = file_data["testcases"]

        test_data = TestData(source=u'/Users/libin/Desktop/robot/PC/trunk/testcase/我的资产.html')

        #设置doc
        test_data.setting_table.doc.populate(doc)

        #设置suite setup
        suite_setup_object = test_data.setting_table.suite_setup
        suite_setup_object.name = None
        suite_setup_object.args = []
        suite_setup_object.assign = ()
        suite_setup_value = []
        suite_setup_value.append(suite_setup.get("name",""))
        suite_setup_value.append(suite_setup["args"])
        suite_setup_object.populate(suite_setup_value)

        #设置suite teardown
        suite_teardown_object = test_data.setting_table.suite_teardown
        suite_teardown_object.name = None
        suite_teardown_object.args = []
        suite_teardown_object.assign = ()
        suite_teardown_value = []
        suite_setup_value.append(suite_teardown["name"])
        suite_setup_value.append(suite_teardown["args"])
        suite_teardown_object.populate(suite_teardown_value)

        #设置test setup
        test_setup_object = test_data.setting_table.test_setup
        test_setup_object.name = None
        test_setup_object.args = []
        test_setup_object.assign = ()
        test_setup_value = []
        test_setup_value.append(test_setup["name"])
        test_setup_value.append(test_setup["args"])
        test_setup_object.populate(test_setup_value)

        #设置test teardown
        test_teardown_object = test_data.setting_table.test_teardown
        test_teardown_object.name = None
        test_teardown_object.args = []
        test_teardown_object.assign = ()
        test_teardown_value = []
        test_teardown_value.append(test_teardown["name"])
        test_teardown_value.append(test_teardown["args"])
        test_teardown_object.populate(test_teardown_value)

        #设置test timeout
        test_timeout_value = test_timeout.split(" ")
        test_data.setting_table.test_timeout.populate(test_timeout_value)

        #设置force tags
        if force_tags:
            test_data.setting_table.force_tags.value = None
            test_data.setting_table.force_tags.populate(force_tags)

        #设置default tags
        if default_tags:
            test_data.setting_table.default_tags.value = None
            test_data.setting_table.default_tags.populate(default_tags)

        #设置import
        test_data.setting_table.imports.data = []
        for each_import in imports:
            if each_import["type"] == "Library":
                test_data.setting_table.add_library(each_import["name"])
            if each_import["type"] == "Resource":
                test_data.setting_table.add_resource(each_import["name"])
            if each_import["type"] == "variable":
                test_data.setting_table.add_resource(each_import["name"])

        #设置case
        for case_object in test_data.testcase_table:
            for each_case in testcases:
                case_setup = each_case["case_setup"]
                case_teardown = each_case["case_teardown"]
                case_timeout = each_case["case_timeout"]
                case_tags = each_case["case_tags"]
                case_steps = each_case["case_steps"]
                if case_object.name == each_case["case_name"]:
                    #设置doc
                    case_object.doc.populate(each_case["case_doc"])
                    #设置name
                    case_object.name = each_case["case_name"]
                    #设置setup
                    case_object.setup.name = None
                    case_object.setup.args = []
                    case_object.setup.assign = ()
                    case_setup_value = []
                    case_setup_value.append(case_setup["name"])
                    case_setup_value.append(case_setup["args"])
                    case_object.setup.populate(case_setup_value)
                    #设置teardown
                    case_object.teardown.name = None
                    case_object.teardown.args = []
                    case_object.teardown.assign = ()
                    case_teardown_value = []
                    case_teardown_value.append(case_teardown["name"])
                    case_teardown_value.append(case_teardown["args"])
                    case_object.teardown.populate(case_teardown_value)
                    #设置timout
                    case_timeout_value = case_timeout.split(" ")
                    case_object.test_timeout.populate(case_timeout_value)
                    #设置tags
                    if case_tags:
                        case_object.tags.value = None
                        case_object.tags.populate(each_case["case_tags"])
                    #设置steps
                    if case_steps:
                        #先清空
                        case_object.steps = []
                        row_list = []
                        for each_step in case_steps:
                            type = each_step.get('type','')
                            #没有forloop
                            if not type:
                                assign = each_step.get("assign",[])
                                keyword = each_step.get("keyword","")
                                comment = each_step.get("comment",[])
                                args = each_step.get("args",[])
                                if assign:
                                    for each_assign in assign:
                                        row_list.append(each_assign)
                                if keyword:
                                    row_list.append(keyword)
                                if args:
                                    for each_args in args:
                                        row_list.append(each_args)
                                if comment:
                                    for each_comment in comment:
                                        row_list.append(each_comment)
                                case_object.add_step(row_list)
                            else:
                                as_list = each_step.get('as_list',[])
                                forloop = each_step.get('steps',[])
                                forloop_obj = case_object.add_for_loop(as_list)
                                for each_loop in forloop:
                                    assign = each_loop.get("assign",[])
                                    keyword = each_loop.get("keyword","")
                                    comment = each_loop.get("comment",[])
                                    args = each_loop.get("args",[])
                                    if assign:
                                        for each_assign in assign:
                                            row_list.append(each_assign)
                                    if keyword:
                                        row_list.append(keyword)
                                    if args:
                                        for each_args in args:
                                            row_list.append(each_args)
                                    if comment:
                                        for each_comment in comment:
                                            row_list.append(each_comment)
                                    forloop_obj.add_step(row_list)

        test_data.save(format="html")













