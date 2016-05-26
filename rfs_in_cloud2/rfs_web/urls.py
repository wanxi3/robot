__author__ = 'libin'

from django.conf.urls import patterns, include, url

from web import index
from web import cathelp
from web.parsing import tree_data
from web.parsing import suite_data
from web.parsing import resource_data
from web.running import run_case
from web.output import output
from web import login
from web import pc
from app import app_phone_data
from web import robot_test
from web.output import report
from web import edition_change
from app import run_app_case


urlpatterns = patterns('',
        url('^$',index.index),
        url('^index/$', index.index),
        url('^tree_data/$', tree_data.tree_data),
        url('^suite_data/$', suite_data.suite_data),
        url('^resource_data/$', resource_data.resource_data),
        url('^run_case/$', run_case.run_case_api),
        url('^output/$', output.output),
        url('^login/$', login.cat_login),
        url('^logout/$', login.cat_logout),
        url('^pc/$', pc.pc),
        url('^app_phone_data/$', app_phone_data.app_phone_data),
        url('^app_suite_data/', app_phone_data.app_suite_data),
        url('^robot/', robot_test.robot_test),
        url('^report/', report.report),
        url('^edition_change/', edition_change.edition_change),
        url('^run_app_case/', run_app_case.run_app_case),
        url('^app_report/', run_app_case.app_report),
        url('^cathelp/', cathelp.cathelp),
        url('^each_phone/', app_phone_data.each_phone),
        url('^set_phone_state/',app_phone_data.set_phone_state),
)
