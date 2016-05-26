# coding=utf-8
__author__ = 'libin'

from django.http import HttpResponse
import json
from collections import OrderedDict

suite_data = OrderedDict()


suite_data['5.1.0'] = \
[
        '登录成功',
        '注册（109）',
        '余额转入成功',
        '余额转出成功',
        '精品推荐购买',
        '理财产品列表购买',
        '5.1.0铜宝转出',
        '5.1.0铜宝转入',
        '消息中心',
        '当前(今日)收益',
        '查看交易记录（滚动）',
        '查看铜宝收益',
        '查看资产详情',
        '更多查看',
        '我的资产查看'
    ]
suite_data['5.2.0'] = \
    [
        '登录成功',
        '注册（109）',
        '余额转入成功',
        '余额转出成功',
        '精品推荐购买',
        '理财产品列表购买',
        '5.2.0铜宝转出',
        '5.2.0铜宝转入',
        '消息中心',
        '当前(今日)收益',
        '查看交易记录（滚动）',
        '查看铜宝收益',
        '查看资产详情',
        '更多查看',
        '我的资产查看',
    ]
suite_data['5.3.0'] = \
    [
        '登录成功',
        '注册（109）',
        '余额转入成功',
        '余额转出成功',
        '精品推荐购买',
        '理财产品列表购买',
        '5.3.0铜宝转出',
        '5.3.0铜宝转入',
        '消息中心',
        '当前(今日)收益',
        '查看交易记录（滚动）',
        '查看铜宝收益',
        '查看资产详情',
        '更多查看',
        '我的资产查看',
    ]


case_match = {
        '5.1.0':
            {
                '登录成功':'myaccout_login',
                '注册（109）':'myaccout_sign',
                '余额转入成功':'balance_into5',
                '余额转出成功':'balance_out5',
                '精品推荐购买':'buy_hot_product_5',
                '理财产品列表购买':'',
                '5.1.0铜宝转出':'myproperty_tongbao_out51',
                '5.1.0铜宝转入':'myproperty_tongbao_in51',
                '消息中心':'myproperty_message_slide51',
                '当前(今日)收益':'myproperty_nowincome_slide51',
                '查看交易记录（滚动）':'myproperty_all_trade_record_slide51',
                '查看铜宝收益':'myproperty_tongbao_income_slide51',
                '查看资产详情':'check_my_investment51',
                '更多查看':'more_check53',
                '我的资产查看':'my_assert_other',
            },
        '5.2.0':
            {
                '登录成功':'myaccout_login51',
                '注册（109）':'myaccout_sign51',
                '余额转入成功':'balance_in51',
                '余额转出成功':'balance_out51',
                '精品推荐购买':'buy_hot_product_5',
                '理财产品列表购买':'',
                '5.1.0铜宝转出':'myproperty_tongbao_out51',
                '5.1.0铜宝转入':'myproperty_tongbao_in51',
                '消息中心':'myproperty_message_slide51',
                '当前(今日)收益':'myproperty_nowincome_slide51',
                '查看交易记录（滚动）':'myproperty_all_trade_record_slide51',
                '查看铜宝收益':'myproperty_tongbao_income_slide51',
                '查看资产详情':'check_my_investment51',
                '更多查看':'more_check53',
                '我的资产查看':'my_assert_other'
            },
        '5.3.0':
            {
                '登录成功':'myaccout_login51',
                '注册（109）':'myaccout_sign51',
                '余额转入成功':'balance_in51',
                '余额转出成功':'balance_out51',
                '精品推荐购买':'buy_hot_product_5',
                '理财产品列表购买':'',
                '5.1.0铜宝转出':'myproperty_tongbao_out51',
                '5.1.0铜宝转入':'myproperty_tongbao_in51',
                '消息中心':'myproperty_message_slide51',
                '当前(今日)收益':'myproperty_nowincome_slide51',
                '查看交易记录（滚动）':'myproperty_all_trade_record_slide51',
                '查看铜宝收益':'myproperty_tongbao_income_slide51',
                '查看资产详情':'check_my_investment51',
                '更多查看':'more_check53',
                '我的资产查看':'my_assert_other',
            },
        
    }