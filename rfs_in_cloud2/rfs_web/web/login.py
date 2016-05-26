# coding=utf-8

__author__ = 'libin'

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate,login,logout
import json


def cat_login(request):
    if request.method == 'GET':
        return render_to_response("login.html", locals(), context_instance=RequestContext(request))
    elif request.method == 'POST':
        if request.POST.get('flag') == 'login':
            username = request.POST.get('username')
            password = request.POST.get('passwd')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                result = {'code':0,'msg':'用户名或密码错误'}
            else:
                result = {'code':1,'msg':'用户名或密码错误'}
        elif request.POST.get('flag') == 'check_login':
            if request.user.is_authenticated():
                result = {'code':0}
            else:
                result = {'code':1}
        result =json.dumps(result)
        return HttpResponse(result)


def cat_logout(request):
    logout(request)
    return HttpResponseRedirect('../login')
