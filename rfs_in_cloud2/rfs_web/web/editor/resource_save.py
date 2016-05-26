# -*- coding: utf-8 -*-
__author__ = 'libin'

from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from robot.parsing import TestCaseFile, TestDataDirectory, ResourceFile, TestData

import os
import json


def resource_save(request):
    if request.method == "GET":
        resorce_data = request.method.GET("resource_data")

        path = resorce_data.get("path","")
        #setings
        settings = resorce_data.get("settings",{})
        doc = settings.get("doc","")
        imports = settings.get("imports",[])

        #variables
        variables = resorce_data.get("variables",[])

        #keywords
        keywords = resorce_data.get("keywords",[])

        data = ResourceFile(source=u'/Users/libin/Desktop/robot/PC/trunk/testcase/我的资产.html').populate()

        #设置doc
        data.setting_table.doc.populate(doc)

        #设置import
        data.setting_table.imports.data = []
        for each_import in imports:
            if each_import["type"] == "Library":
                data.setting_table.add_library(each_import["name"])
            if each_import["type"] == "Resource":
                data.setting_table.add_resource(each_import["name"])
            if each_import["type"] == "variable":
                data.setting_table.add_resource(each_import["name"])

        #设置variables
        data.variable_table.variables = []
        for each_variable in variables:
            name = each_variable["variable_name"]
            value = each_variable["variable_value"]
            comment = each_variable["variable_comment"]
            data.variable_table.add(name,value,comment)

        #设置keywords
        for keyword_object in data.keyword_table:
            for each_keyword in keywords:
                teardown = each_keyword["keyword_teardown"]
                steps = each_keyword["keyword_steps"]
                if keyword_object.name == each_keyword["keyword_name"]:
                    #设置doc
                    keyword_object.doc.populate(each_keyword["keyword_doc"])
                    #设置arguments
                    keyword_object.args.populate(each_keyword["keyword_args"])
                    #设置return value
                    keyword_object.return_.populate(each_keyword["keyword_return"])
                    #设置timeout
                    timeout_value = each_keyword["keyword_timeout"].split(" ")
                    keyword_object.timeoutpopulate(timeout_value)
                    #设置teardown
                    keyword_object.teardown.name = None
                    keyword_object.teardown.args = []
                    keyword_object.teardown.assign = ()
                    teardown_value = []
                    teardown_value.append(teardown["name"])
                    teardown_value.append(teardown["args"])
                    keyword_object.teardown.populate(teardown_value)
                    #设置steps
                    if steps:
                        #先清空
                        keyword_object.steps = []
                        row_list = []
                        for each_step in steps:
                            type = each_step.get('type',False)
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
                                keyword_object.add_step(row_list)
                            else:
                                as_list = each_step.get('as_list',"")
                                forloop = each_step.get('setps',[])
                                forloop_obj = keyword_object.add_for_loop(as_list)
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
        data.save(format="html")













