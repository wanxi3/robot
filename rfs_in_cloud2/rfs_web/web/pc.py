__author__ = 'libin'


from django.shortcuts import render,render_to_response
from django.template import RequestContext
from robot.parsing import ResourceFile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import os

@login_required(login_url="/login/")
def pc(request):
	if request.method == 'GET':
		username = request.user.username
		base_path = os.path.dirname(__file__)
		private_path = os.path.join("../../static/resource_house/",username)
		resource_path = os.path.join(base_path,private_path)
		resource_path = os.path.join(resource_path,'robot/PC/trunk/resource')
		resource_list = os.listdir(resource_path)
		for rm_dir in [u'.DS_Store',u'.svn']:
			if rm_dir in resource_list:
				resource_list.remove(rm_dir)
		result = {}

		for each_resource in resource_list:
			case_name_list = []
			path = os.path.join(resource_path,each_resource)

			data = ResourceFile(source=path).populate()
			name_list = []

			for each_keyword in data.keyword_table:
				name_list.append(each_keyword.name)

			for each_variable in data.variable_table.variables:
				name_list.append(each_variable.name)

			result[each_resource[:-5]] = name_list

		return render_to_response("pc.html", locals(), context_instance=RequestContext(request))


