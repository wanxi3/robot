
from robot import run
import sys
import json
import os

datasources = sys.argv[1]
timestamp = sys.argv[2]
base_path = os.path.dirname(__file__)
path = os.path.join(base_path,'../../../static/runcase_data/',timestamp)
with open(path) as datafile:
    options = datafile.read()
options = eval(options)

options['stdout'] = open(options['stdout'],'w')
options['stderr'] = open(options['stderr'],'w')
run(datasources,**options)

