# -*- coding: utf-8 -*-
__author__ = 'libin'

from django.http import HttpResponse
from robot.parsing import ResourceFile

import sys
import json


def resource_parser(data,path):
    resource_parser_data = {}
    resource_parser_data["path"] = path

    #setting
    settings = {}
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

    #variable
    variables = []
    for each_variable in data.variable_table.variables:
        variable_dict = {}
        variable_dict["variable_name"] = each_variable.name
        variable_dict["variable_value"] = each_variable.value
        variable_dict["variable_comment"] = each_variable.comment.as_list()
        variable_dict["variable_type"] = "variable"
        variables.append(variable_dict)

    #keywords
    keywords = []
    for each_keyword in data.keyword_table:
        keyword = {}
        keyword["keyword_name"] = each_keyword.name
        keyword["keyword_doc"] = each_keyword.doc.value
        keyword["keyword_args"] = each_keyword.args.value
        keyword["keyword_return"] = each_keyword.return_.value
        keyword["keyword_timeout"] = each_keyword.timeout.value
        keyword["keyword_teardown"] = {
                            "name":each_keyword.teardown.name,
                            "args":each_keyword.teardown.args,}
        keyword["keyword_steps"] = []

        for step in each_keyword.steps:
            if type(step).__name__ == 'Step':
                step_dict = {}
                step_dict["comment"] = []
                step_dict["args"] = step.args
                step_dict["assign"] = step.assign
                try:
                    step_dict["keyword"] = step.name
                except:
                    step_dict["keyword"] = step.keyword
                step_dict["type"] = step.is_for_loop()
                keyword["keyword_steps"].append(step_dict)
            elif type(step).__name__ == 'ForLoop':
                forloop = {}
                forloop['as_list'] = step.as_lsit
                forloop['type'] = step.is_for_loop()
                for each_step in step.steps:
                    step_dict = {}
                    step_dict["comment"] = []
                    step_dict["args"] = each_step.args
                    step_dict["assign"] = each_step.assign
                    step_dict["keyword"] = each_step.name
                    forloop['steps'].append(step_dict)
                keyword['case_steps'].append(forloop)

        keywords.append(keyword)

    resource_parser_data["type"] = "resource"
    resource_parser_data["settings"] = settings
    resource_parser_data["variables"] = variables
    resource_parser_data["keywords"] = keywords

    return resource_parser_data

def resource_data(request):
    if request.method == "GET":
        path = request.GET.get("path")
        resource_file = ResourceFile(path).populate()
        data = resource_parser(resource_file,path)

        response = HttpResponse(json.dumps(data), content_type="application/json")
        response['Access-Control-Allow-Origin'] = '*'
        return response

