# -*- coding: utf-8 -*-
__author__ = 'libin'

from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from robot.api import TestData
from robot.errors import DataError

import os
import fnmatch
import json

class RobotParser(object):
	"""
	文件目录树结构解析类
	"""
	def __init__(self):
		self.project_list = []
		self.node_id = 0
		self.case_count = 0
		self.keyword_count = 0
		self.variable_count = 0
		self.file_count = 0
		self.dir_count = 0
		self.name_list = []
		self.json_tree = {"root": []}

	def project_parse(self, path, parent_dict=None):

		# 获取path路径下文件和目录的名称
		entry_list = os.listdir(path)
		entry_list.remove(u'.DS_Store')
		entry_list.remove(u'.svn')


		# 指定空文件夹的图标样式
		# if parent_dict and not files:
		#     parent_dict["iconCls"] = "icon-open-folder"

		for each_entry in entry_list:
			# 隐藏__init__.txt
			if each_entry.endswith("__init__.html"):
				if parent_dict:
					parent_dict["iconCls"] = "icon-folder"
				continue
			else:
				self.node_id += 1
				self.name_list.append(each_entry)
				tmp_dict = {"text": each_entry, "id": self.node_id, "state": "open"}

				each_entry_path = path + "/" + each_entry

				# 若入口为文件类型，则进行Robot Data解析
				if os.path.isfile(each_entry_path):
					tmp_dict["iconCls"] = "icon-file"
					self.file_count += 1
					try:
						robot_file_data = TestData(source=each_entry_path)

						# 解析test case
						case_list = []
						for each_case in robot_file_data.testcase_table:
							self.node_id += 1
							self.name_list.append(each_case.name)
							self.case_count += 1
							case_name = each_case.name
							case_list.append({"id": self.node_id,
											  "text": case_name,
											  "iconCls": "icon-robot",
											  # "state": "close",
											  "attributes": {"type": "case",
															 "path": each_entry_path}})

						# 解析keyword
						keyword_list = []
						for each_keyword in robot_file_data.keyword_table:
							self.node_id += 1
							self.name_list.append(each_keyword.name)
							self.keyword_count += 1
							keyword_name = each_keyword.name
							keyword_list.append({"id": self.node_id,
												 "text": keyword_name,
												 "iconCls": "icon-keyword",
												 "attributes": {"type": "keyword",
																"path": each_entry_path}})

						# 解析variable
						variable_list = []
						for each_variable in robot_file_data.variable_table:
							self.node_id += 1
							self.name_list.append(each_variable.name)
							self.variable_count += 1
							variable_name = each_variable.name
							variable_list.append({"id": self.node_id,
												  "text": variable_name,
												  "iconCls": "icon-variable",
												  "attributes": {"type": "variable",
																 "path": each_entry_path}})

						# Robot脚本文件的子节点由Case、Keyword、Variable组成
						tmp_dict["children"] = variable_list + keyword_list + case_list
						tmp_dict["attributes"] = {"type": "file", "path": each_entry_path}
						tmp_dict["state"] = "open"
					except DataError, e:
						print e.message

				elif os.path.isdir(each_entry_path):
					self.dir_count += 1
					tmp_dict["attributes"] = {"type": "directory", "path": each_entry_path}
					tmp_dict["children"] = []
					tmp_dict["state"] = "open"

					self.project_parse(each_entry_path, tmp_dict)

				# 如果是根节点，直接添加至project_list
				if not parent_dict:
					self.project_list.append(tmp_dict)
				# 否则，添加至父节点的子节点列表中
				else:
					parent_dict["children"].append(tmp_dict)

class TreeNode():
	def __init__(self,name,value):
		self.name = name
		self.value=value
		self.child=[]

remove_list = ['.svn','.DS_Store',]
#文件目录树解析
def	walkdir(dirname):

	try:
		ls = os.listdir(dirname)
		for each in remove_list:
			if each in ls:
				ls.remove(each)
	except:
		print 'access deny'
	else:
		newNode = TreeNode("",dirname)
		arr = dirname.split("/")
		newNode.name = arr[-1]
		for l in ls:
			if l.endswith('__init__'):
				continue
			temp = os.path.join(dirname,l)
			if (os.path.isdir(temp)):
				newNode.child.append(walkdir(temp))
			else:
				if fnmatch.fnmatch(temp, '*html'):
					leaf = TreeNode(l,temp)
					newNode.child.append(leaf)
		return newNode


def tree_data(request):
	if request.method == "GET":
		username = request.user.username
		base_path = os.path.dirname(__file__)
		private_path = os.path.join("../../../static/resource_house/",username)
		path = os.path.join(base_path,private_path)
		result = {}
		suite_path = os.path.join(path,'robot/PC/trunk/testcase/')
		suite_list = os.listdir(suite_path)
		for each_rm in [u'.DS_Store',u'.svn',u'__init__.html',]:
			if each_rm in suite_list:
				suite_list.remove(each_rm)
		for each_suite in suite_list:
			case_name_list = []
			path = os.path.join(suite_path,each_suite)
			data = TestData(source=path)
			for each_case in data.testcase_table:
				case_name_list.append(each_case.name)
			result[each_suite[:-5]] = case_name_list
		result["path"] = suite_path
		response = HttpResponse(json.dumps(result), content_type="application/json")
		response['Access-Control-Allow-Origin'] = '*'
		return response












