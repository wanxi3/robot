# coding=utf-8
__author__ = 'libin'


from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import os


def copyFiles(sourceDir,targetDir):
    if sourceDir.find(".svn") > 0:
        return
    for file in os.listdir(sourceDir):
        targetDir = targetDir.encode('utf-8')
        sourceFile = os.path.join(sourceDir,file)
        targetFile = os.path.join(targetDir,file)
        if os.path.isfile(sourceFile):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                open(targetFile, "wb").write(open(sourceFile, "rb").read())
        if os.path.isdir(sourceFile):
            copyFiles(sourceFile, targetFile)

@login_required(login_url="/login/")
def index(request):
    if request.method == 'GET':
        flag = True
        username = request.user.username
        base_path = os.path.dirname(__file__)
        path = os.path.join(base_path,"../../static/resource_house/")
        for each_dir in os.listdir(path):
            if each_dir == username:
                flag = False
                break
        if flag:
            private_path = os.path.join(path,username)
            try:
                os.mkdir(private_path.decode('utf-8').encode('gb18030'))
                # os.mkdir(os.path.join(private_path,'robot').decode('utf-8').encode('gb18030'))
                base_resource = os.path.join(base_path,'../../static/base_resource')
                copyFiles(base_resource,private_path)
                #except WindowsError,e:
            except ValueError, e:
                message = u"创建输出文件夹" + private_path + u"失败：" + e.message


        return render_to_response("index.html", locals(), context_instance=RequestContext(request))


