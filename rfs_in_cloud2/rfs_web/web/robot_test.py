# coding=utf-8
__author__ = 'libin'

from django.http import HttpResponse

import json


#测试robotframework的接口测试
def robot_test(request):
	if request.method == "GET":
		result = {"1":'libin',}
		response = HttpResponse(json.dumps(result), content_type="application/json")
		response['Access-Control-Allow-Origin'] = '*'
		return response

from copy import deepcopy
l = range(10)

for i in deepcopy(l):
    print i
    if i % 2 == 0:
        l.remove(i)
print l