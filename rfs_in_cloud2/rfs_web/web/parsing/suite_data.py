# -*- coding: utf-8 -*-
__author__ = 'libin'

from django.http import HttpResponse
from robot.parsing import ResourceFile, TestData

import json

'''
与前端交互的数据流
data = {
        "type": "file",
        "path": "D:/Robot/PC/登录/",
        "data": {
            "settings": {
                "test_timeout": "6 seconds",
                "imports": [
                    {
                        "comment": [
                            "# 接口调用库"
                        ],
                        "alias": "",
                        "args": [],
                        "library": "RequestsLibrary"
                    },
                    {
                        "comment": [],
                        "alias": "",
                        "args": [],
                        "library": "Collections"
                    },
                    {
                        "comment": [],
                        "alias": "",
                        "args": [],
                        "library": "OperatingSystem"
                    },
                    {
                        "comment": [],
                        "alias": "",
                        "args": [],
                        "library": "MyResource.txt"
                    }
                ],
                "suite_teardown": {
                    "comment": [
                        "# 阿发发顺丰"
                    ],
                    "args": [
                        "http://www.ctrip.com",
                        "ff"
                    ],
                    "keyword": "Open Browser"
                },
                "test_teardown": {
                    "comment": [
                        "# 靠"
                    ],
                    "args": [],
                    "keyword": "Close Browser"
                },
                "force_tags": [
                    "tag1",
                    "tag2"
                ],
                "doc": "我是Interface的文档啊，你妹",
                "test_setup": {
                    "comment": [
                        "# fuck"
                    ],
                    "args": [],
                    "keyword": "Close All Browsers"
                },
                "suite_setup": {
                    "comment": [
                    ],
                    "args": [
                        "http://www.ctrip.com",
                        "ff"
                    ],
                    "keyword": "Open Browser"
                },
                "default_tags": [
                    "默认标签",
                    "默认标签2"
                ],
                "type": "file",
                "metadata": [
                    {
                        "comment": [
                            "# haha"
                        ],
                        "name": "MetadataName",
                        "value": "1"
                    }
                ]
            },
            "variables": [
                {
                    "comment": [
                        "# fuck"
                    ],
                    "name": "${a}",
                    "value": [
                        "10"
                    ]
                },
                {
                    "comment": [
                        "# fuck2"
                    ],
                    "name": "@{b}",
                    "value": [
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8"
                    ]
                }
            ],
            "testcases": [
                {
                    "case_timeout": "1 second",
                    "case_doc": "我是Case的文档",
                    "case_tags": [
                        "case tag1",
                        "case tag2"
                    ],
                    "case_teardown": {
                        "comment": [
                            "# I Do"
                        ],
                        "args": [
                            "yrmao"
                        ],
                        "keyword": "Log"
                    },
                    "case_name": "VendorOrderService",
                    "case_setup": {
                        "comment": [
                            "# 321"
                        ],
                        "args": [
                            "123"
                        ],
                        "keyword": "Log"
                    },
                    "case_steps": [
                        {
                            "comment": [],
                            "args": [
                                "VendorOrderService",
                                "http://vendorws.package.uat.qa.nt.ctripcorp.com/Package-Vendor-OrderSvc/"
                            ],
                            "assign": [],
                            "keyword": "Create Session"
                        },
                        {
                            "comment": [],
                            "args": [
                                "{ \\ \\ \\ \\ \"ProviderId\": 0, \\ \\ \\ \\ \"UserGroupIds\": [ \\ \\ \\ \\ \\ \\ \\ \\ 0 \\ \\ \\ \\ ], \\ \\ \\ \\ \"OrderIds\": [ \\ \\ \\ \\ \\ \\ \\ \\ 0 \\ \\ \\ \\ ], \\ \\ \\ \\ \"Includes\": \"String\" }"
                            ],
                            "assign": [
                                "${data}="
                            ],
                            "keyword": "Set Variable"
                        },
                        {
                            "comment": [],
                            "args": [
                                "Content-Type",
                                "application/json",
                                "Host",
                                "vendorws.package.uat.qa.nt.ctripcorp.com"
                            ],
                            "assign": [
                                "${headers}="
                            ],
                            "keyword": "Create Dictionary"
                        },
                        {
                            "comment": [],
                            "args": [
                                "VendorOrderService",
                                "/json/GetOrder",
                                "${data}",
                                "headers=${headers}"
                            ],
                            "assign": [
                                "${resp}="
                            ],
                            "keyword": "Post"
                        },
                        {
                            "comment": [],
                            "args": [
                                "${resp.status_code}",
                                "200"
                            ],
                            "assign": [],
                            "keyword": "Should Be Equal As Strings"
                        },
                        {
                            "comment": [],
                            "args": [
                                "${resp.content}"
                            ],
                            "assign": [],
                            "keyword": "Log"
                        },
                        {
                            "comment": [],
                            "args": [
                                "Should Be Equal As Strings",
                                "${resp.json()['ResponseStatus']['Ack']}",
                                "Failure"
                            ],
                            "assign": [],
                            "keyword": "Comment"
                        },
                        {
                            "comment": [],
                            "args": [
                                "Dictionary Should Contain Key",
                                "${resp.json()}",
                                "ResponseStatus"
                            ],
                            "assign": [],
                            "keyword": "Comment"
                        },
                        {
                            "comment": [],
                            "args": [
                                "Dictionary Should Contain Value",
                                "${resp.json()['ResponseStatus']}",
                                "Failure"
                            ],
                            "assign": [],
                            "keyword": "Comment"
                        },
                        {
                            "comment": [],
                            "args": [
                                "Dictionary Should Not Contain Key",
                                "${resp.json()['ResponseStatus']}",
                                "haha"
                            ],
                            "assign": [],
                            "keyword": "Comment"
                        },
                        {
                            "comment": [],
                            "args": [
                                "Dictionary Should Not Contain Value",
                                "${resp.json()['ResponseStatus']}",
                                "aaa"
                            ],
                            "assign": [],
                            "keyword": "Comment"
                        },
                        {
                            "comment": [],
                            "args": [
                                "Directory Should Be Empty",
                                "${resp.json()['ResponseStatus']}"
                            ],
                            "assign": [],
                            "keyword": "Comment"
                        },
                        {
                            "comment": [],
                            "args": [
                                "Directory Should Not Be Empty",
                                "${resp.json()['ResponseStatus']}"
                            ],
                            "assign": [],
                            "keyword": "Comment"
                        },
                        {
                            "comment": [],
                            "args": [
                                "Directory Should Exist",
                                "${resp.json()['ResponseStatus']}"
                            ],
                            "assign": [],
                            "keyword": "Comment"
                        },
                        {
                            "comment": [],
                            "args": [
                                "Directory Should Not Exist",
                                "1111"
                            ],
                            "assign": [],
                            "keyword": "Comment"
                        }
                    ]
                }
            ],
            "keywords": [],
            "path": "D:/Robot/Cases/report"
        }
    }
'''
def suite_parser(data,path):
    suite_parser_data = {}
    suite_parser_data["path"] = path
    #setting
    settings = {}
    test_timeout = data.setting_table.test_timeout.value
    settings["test_timeout"] = test_timeout
    doc = data.setting_table.doc.value
    settings["doc"] = doc

    imports = []
    for each_import in data.imports:
        import_dict = {}
        import_dict["comment"] = each_import.comment.as_list()
        alias = each_import.alias
        if not alias:
            alias = ""
        import_dict["alias"] = alias
        import_dict["args"] = each_import.args
        import_dict["library"] = each_import.name
        import_dict["type"] = each_import.type
        imports.append(import_dict)

    settings["imports"] = imports
    settings["suite_setup"] = {
        "name":data.setting_table.suite_setup.name,
        "args":data.setting_table.suite_setup.args,
        "assign":data.setting_table.suite_setup.assign,
    }
    settings["suite_teardown"] = {
        "name":data.setting_table.suite_teardown.name,
        "args":data.setting_table.suite_teardown.args,
        "assign":data.setting_table.suite_teardown.assign,
    }
    settings["test_setup"] = {
        "name":data.setting_table.test_setup.name,
        "args":data.setting_table.test_setup.args,
        "assign":data.setting_table.test_setup.assign,
    }
    settings["test_teardown"] = {
        "name":data.setting_table.test_teardown.name,
        "args":data.setting_table.test_teardown.args,
        "assign":data.setting_table.test_teardown.assign,
    }

    settings["force_tags"] = data.setting_table.force_tags.value
    settings["default_tags"] = data.setting_table.default_tags.value

    #cases
    testcases = []
    for each_case in data.testcase_table:
        testcase = {}
        testcase["case_name"] = each_case.name
        testcase["case_doc"] = each_case.doc.value
        testcase["case_setup"] = {
                                    "name":each_case.setup.name,
                                    "args":each_case.setup.args,
                                    "assign":each_case.setup.assign,}
        testcase["case_teardown"] = {
                                    "name":each_case.teardown.name,
                                    "args":each_case.teardown.args,
                                    "assign":each_case.teardown.assign,}
        testcase["case_timeout"] = each_case.timeout.value
        testcase["case_tags"] = each_case.tags.value
        testcase["case_steps"] = []

        #显示的顺序为 assign>keyword(name)>args
        for step in each_case.steps:
            if type(step).__name__ == 'Step':
                step_dict = {}
                step_dict["comment"] = []
                step_dict["args"] = step.args
                step_dict["assign"] = step.assign
                try:
                    step_dict["keyword"] = step.name
                except:
                    step_dict["keyword"] = step.keyword
                step_dict['type'] = step.is_for_loop()
                testcase["case_steps"].append(step_dict)
            elif type(step).__name__ == 'ForLoop':
                forloop = {}
                forloop['as_list'] = step.as_lsit
                forloop['type'] = step.is_for_loop()
                for each_step in step.steps:
                    forloop_dict = {}
                    forloop_dict["comment"] = []
                    forloop_dict["args"] = each_step.args
                    forloop_dict["assign"] = each_step.assign
                    forloop_dict["keyword"] = each_step.name
                    forloop['steps'].append(forloop_dict)
                testcase['case_steps'].append(forloop)

        testcases.append(testcase)

    suite_parser_data["type"] = "suite"
    suite_parser_data["setting"] = settings
    suite_parser_data["testcases"] = testcases

    return suite_parser_data


def suite_data(request):
    if request.method == "GET":
        flag = True
        path = request.GET.get("path")
        try:
            #path = u'/Users/libin/Desktop/robot/PC/trunk/testcase/我的资产.html'
            data = TestData(source=path)
            suite_parser_data = suite_parser(data,path)
        except ValueError, e:
            flag = False

        response = HttpResponse(json.dumps({
            "flag": flag,
            "data": suite_parser_data
        }))
        response["Content-Type"] = "application/json; charset=utf-8"
        response['Access-Control-Allow-Origin'] = '*'

        return response





