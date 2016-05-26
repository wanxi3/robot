# coding=utf-8

__author__ = 'libin'

from django.shortcuts import render_to_response
from django.template import RequestContext

def cathelp(request):
    if request.method == 'GET':

        return render_to_response("cathelp.html", locals(), context_instance=RequestContext(request))
