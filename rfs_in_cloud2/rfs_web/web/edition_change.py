# coding=utf-8

__author__ = 'libin'

from django.shortcuts import render_to_response
from django.template import RequestContext

def edition_change(request):
    if request.method == 'GET':
        cat_version = \
            [
                # {
                #     "title":"Cloud Automation Test v2.1",
                #     "class":"panel-primary",
                #     "versionInfo":
                #         [
                #             "1、支持模块注册、登录、理财产品、购买、资产模块的展示",
                #             "1、支持模块注册、登录、理财产品、购买、资产模块的展示"
                #         ]
                # },
                {
                    "title":'Cloud Automation Test v3.0 上线时间:2016/3/10',
                    "class":"panel-info",
                    "versionInfo":[
                        "1、app端手机共享功能上线",
                        "2、remote支持一键安装",
                        "3、web端一些bug修复",
                        "4、界面调整",

                    ]
                },
                {
                    "title":'Cloud Automation Test v2.0 上线时间:2016/1/14',
                    "class":"panel-warning",
                    "versionInfo":[
                        "1、ios端上线",
                        "2、android端代码优化",
                        "3、项目结构调整",
                        "4、增加关键字帮助模块",
                    ]
                },
                {
                  "title":'Cloud Automation Test v1.2 上线时间:2015/12/17',
                  "class":"panel-success",
                  "versionInfo":[
                                "1、app端状态机代码优化",
                                "2、增加app运行日志输出",
                                "3、修改remote和后台状态机的BUG",
                                ]
                },
                {
                    "title":'Cloud Automation Test v1.2 上线时间:2015/12/8',
                    "class":"panel-primary",
                    "versionInfo":[
                                "1、app端测试用例调整",
                                "2、app端后端代码优化",
                                ]
                },
                {
                    "title":'Cloud Automation Test v1.1',
                    "class":"panel-info",
                    "versionInfo":[
                                "1、支持PC端case运行后的日志查看",
                                "2、支持公共资源套件的展示",
                                "3、增加登录功能",
                                "4、多用户分流支持",
                                "5、接入APP端,支持app端的case勾选，运行",
                                "6、支持APP端的日志查看",
                                ]
                },
                {
                    "title":'Cloud Automation Test v1.0',
                    "class":"panel-warning",
                    "versionInfo":[
                                "1、支持PC模块注册、登录、理财产品、购买、资产套件的展示",
                                "2、支持支持case勾选，运行"
                    ]
                }
            ]
        return render_to_response("edition.html", locals(), context_instance=RequestContext(request))
