# _*_ coding:utf-8 _*_
__author__ = 'Eddie'

import ConfigParser,sql,datetime
import re,os,time,tbjpyios,TerminalHandle
from time import sleep
import urllib2
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException

class Case(TerminalHandle.AppHandle,TerminalHandle.Data):
    def __init__(self,platformName,platfromVersion,deviceName,app,udid,bundleId,appPackage,appActivity,port=None,timeout=None,**kwargs):
        super(Case,self).__init__(platformName,platfromVersion,deviceName,app,udid,bundleId,appPackage,appActivity,port=None,timeout=None,**kwargs)

    #测试数据实例化
    testdata=TerminalHandle.Data()

    #进入我的账户
    def myAccount(self):
        u"""进入我的账户"""
        self.click_more()
        #点击“我的账户”,然后进行账号的登录操作
        self.click_myaccount5()

    #登录功能
    def login(self,phone_num,passwd,expect=True,*args):
        actual=True
        code=111
        try:
            if self.isElement("xpath",tbjpyios.phoneId)==False:
                e='用户已登录'
                self.back()
            else:
                sleep(2)
                self.input_login_phone(phone_num)
                self.click_next()
                self.input_login_passwd(passwd)
                self.click_login_button()
                sleep(6)
                if self.isElement("name",tbjpyios.check_login_fail)==False:
                    self.screenshot()
                    actual=True
                    e='登录成功'
                elif self.isElement("name",tbjpyios.pwd_notsuite_acount)==True:
                    self.screenshot()
                    self.click_button((By.XPATH,tbjpyios.pwd_confirm_btn))
                    self.back()
                    self.back()
                    actual=False
                    e='账号和密码不符'
                else:
                    actual=False
                    e='登陆失败'
        except Exception,e:
            actual=False
        finally:
            result=e==expect
            ending={'code':code,'message':e,'result':result}
            return ending

    #注册
    def sign(self,phone_num,sign_pwd,expect,*args):
        code=111
        actual=None
        try:
            if self.isElement("xpath",tbjpyios.phoneId)==False:
                e='用户已登录'
                actual=False
                self.back()
            else:
                self.input_sign_Account(phone_num)
                if self.isElement("xpath",tbjpyios.verify_input)==False:
                    e='用户已注册'
                    actual=False
                    self.back()
                else:
                    sleep(3)
                    myms = sql.mysql_connect(sql.db_info)
                    yzm=myms.sql_assign_exec("select content from mdp_message WHERE recipients="+ phone_num+ " ORDER BY create_time DESC LIMIT 1")
                    yzm1=re.search('\d{4}', yzm)
                    yzm2=yzm1.group(0)
                    self.send_keys((By.XPATH,tbjpyios.verify_input),yzm2)
                    self.send_signpwd(sign_pwd)
                    self.click_button((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIAButton[4]'))
                    sleep(3)
                    if self.isElement("xpath",tbjpyios.sign_fail_check)==True:
                        self.screenshot()
                        actual=False
                        e='注册失败'
                    else:
                        self.screenshot()
                        actual=True
                        e='注册成功'
        except Exception,e:
            actual=False
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #进入密码管理模块
    def pwd_manager(self):
        self.click_myaccount()
        #u"""密码管理"""
        self.rl_pwd_manager()

    #修改登录密码
    def modify_login_pwd(self,old_pwd,set_pwd,repeat_pwd,expect):
        actual=None
        code=111
        try:
        #修改登录密码
            self.change_login_pwd_layout()
            self.send_old_pwd(old_pwd)
            self.set_pwd(set_pwd,repeat_pwd)
            if self.isElement("name",tbjpyios.check_pwd_success)==True:
                actual=True
                e='修改登录密码成功'
                self.click_button((By.XPATH,tbjpyios.pwd_confirm_btn))
                sleep(10)
            elif self.isElement("name",tbjpyios.check_modify_pwd_not_null)==True:
                actual=False
                e='密码不能空'
                self.click_button((By.XPATH,tbjpyios.pwd_confirm_btn))
            elif self.isElement("name",tbjpyios.check_modify_pwd_not_same)==True:
                actual=False
                e='两次密码不一样'
                self.click_button((By.XPATH,tbjpyios.pwd_confirm_btn))
            elif self.isElement("name",tbjpyios.first_pwd_error)==True:
                actual=False
                e='原始密码错误'
                self.click_button((By.XPATH,tbjpyios.pwd_confirm_btn))
        except Exception,e:
            actual=False
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #修改交易密码
    def modify_trade_pwd(self,old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect):
        actual=None
        code=111
        try:
            self.rlyt_update_trans_pwd()
            self.send_old_trade_pwd(old_trade_pwd)
            self.send_new_trade_pwd(new_trade_pwd)
            self.send_repeat_trade_pwd(repeat_trade_pwd)
            self.click_complete_btn()
            sleep(4)
            if self.isElement("name",tbjpyios.check_modify_trade_pwd)==True:
                actual=True
                e='修改交易密码成功'
            else:
                self.screenshot()
                actual=False
                e='修改交易密码失败'
        except Exception,e:
            actual=False
        finally:
            result=actual==expect
            ending={'code':code,'message':e,'result':result}
            return ending

    #找回交易密码
    def back_trade_pwd(self,phone_num,username,card,new_trade_pwd,repeat_trade_pwd,expect):
        actual=None
        code=111
        try:
            self.find_trade_pwd(phone_num,username,card)
            self.send_new_trade_pwd(new_trade_pwd)
            self.send_repeat_trade_pwd(repeat_trade_pwd)
            self.click_complete_btn()
            sleep(3)
            if self.isElement("name",tbjpyios.check_back_trade_pwd)==True:
                self.screenshot()
                actual=True
                e='找回交易密码成功'
            else:
                self.screenshot()
                actual=False
                e='找回交易密码失败'
        except Exception,e:
            actual=False
        finally:
            result=actual==expect
            ending={'code':code,'message':e,'result':result}
            return ending

    #进入余额模块
    def enter_balance(self):
        #点击我的账户
        self.click_myaccount()
        #点击账户余额
        self.click_account_balance()

    #账户余额一充值
    def top_up(self,topup_num,trade_pwd,expect):
        actual=None
        code=111
        try:
            self.rl_recharge(topup_num)
            #输入铜板街交易密码
            self.send_trade_pwd(trade_pwd)
            self.click_sure()
            sleep(6)
            if self.isElement("xpath",tbjpyios.check_money_success)==True:
                self.screenshot()
                actual=True
                self.click_button((By.XPATH,tbjpyios.check_money_success))
                if self.isElement("xpath",tbjpyios.check_money_success)==False:
                    self.back()
                    e='余额成功充值'
            else:
                actual=False
                e='账户余额充值失败'
        except Exception,e:
            actual=False
        finally:
            result=str(e)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    def cash(self,out_num,trade_pwd,expect):
        #余额转出
        actual=None
        code=111
        try:
            self.rl_balance_out(out_num)
            sleep(1)
            self.send_trade_pwd(trade_pwd)
            self.click_sure()
            sleep(5)
            if self.isElement("xpath",tbjpyios.check_money_success)==True:
                actual=True
                e='余额成功提现'
                self.click_button((By.XPATH,tbjpyios.check_money_success))
                if self.isElement("xpath",tbjpyios.check_money_success)==False:
                    self.back()
                else:
                    pass
            else:
                actual=False
                e='余额提现失败'
        except Exception,e:
            actual=False
        finally:
            result=str(e)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending


    #忘记密码后，找回密码
    def back_pwd(self,phone_num='13735865796',person_ID='330522199009256911',new_pwd='654321',expect=True):
        self.click_more()
        #点击“我的账户”,然后进行账号的登录操作
        self.click_myaccount()
        actual=None
        code=111
        try:
            #输入手机号
            self.input_login_phone(phone_num)
            self.click_next()
            #点击忘记密码
            self.click_forgetpwd()
            self.send_person_id(person_ID)
            self.click_back_pwd_nextbtn()
            myms = sql.mysql_connect(sql.db_info)
            yzm=myms.sql_assign_exec("select content from mdp_message WHERE recipients="+ phone_num + " ORDER BY create_time DESC LIMIT 1")
            yzm1=re.search('\d{4}', yzm)
            yzm2=yzm1.group(0)
            self.send_keys((By.ID,tbjpyios.verify_input),yzm2)
            self.click_back_pwd(new_pwd)
            self.click_complete_btn()
            if self.isElement("name",tbjpyios.check_find_pwd)==True:
                self.screenshot_True()
                actual=False
                e='找回密码设置失败'
            else:
                self.screenshot_Error()
                actual=True
                e='找回密码设置成功'
        except Exception,e:
            actual=False
        finally:
            result=actual==expect
            ending={'code':code,'message':e,'result':result}
            return ending

    #进入精品推荐模块
    def hot_product(self):
        self.click_hot_product()

    #进入理财产品模块
    def financing_products(self):
        self.tab_financing_products()

    #设置新用户交易密码是否成功功能
    def set_new_people_trade_pwd_check(self,new_people_trade_pwd,repeat_trade_pwd,expect):
        actual=None
        code=111
        try:
            self.set_new_people_trade_pwd(new_people_trade_pwd,repeat_trade_pwd)
            sleep(6)
            if self.isElement("name",tbjpyios.check_set_newpeople_tradepwd_fail)==True:
                actual=False
                e='购买失败'
            else:
                actual=True
                e='购买成功'
                self.click_button((By.ID,tbjpyios.complete_btn))
        except Exception,e:
            actual=False
        finally:
            result=actual==expect
            ending={'code':code,'message':e,'result':result}
            return ending


    #进入我的资产模块并进入铜宝
    def myasset(self):
        self.click_myasset()
        self.click_tongbao()
        sleep(5)

    #4.3-5.0版本账户余额入口
    def enter_balance5(self):
        self.click_myasset()
        self.click_balance5()

     #5.0版本理财产品铜宝入口
    def click_financing_products_tb(self):
        self.click_button((By.XPATH,tbjpyios.financing_products_tb))

    #理财产品页信息
    def financing_products_info(self):
        self.tab_financing_products()

    #未登录的情况下，进入我的资产模块
    def my_assets(self,phone_num='13735865796',passwd='654321'):
        self.click_myasset()
        self.start_earn_money()
        self.login(phone_num,passwd)

    '''重构后的组织用例'''
    #通过更多-我的帐号模块进入，登陆
    def myaccout_login(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect='登录成功',*args):
        self.myAccount()
        return self.login(phone_num,passwd,expect)

    #登陆失败的模块,手机号长度不满11位
    def myaccout_login_error1(self,phone_num='1111111111',passwd='654321',expect=True,*args):
        self.myAccount()
        self.login(phone_num,passwd,expect)

    #手机号未注册
    def myaccout_login_error2(self,phone_num='13735865793',passwd='654321',expect=True,*args):
        self.myAccount()
        self.login(phone_num,passwd,expect)

    #手机号和密码不匹配
    def myaccout_login_error3(self,phone_num='13735865796',passwd='123456',expect=True,*args):
        self.myAccount()
        self.login(phone_num,passwd,expect)

    #手机号为已注册号码，密码不满6位
    def myaccout_login_error4(self,phone_num='13735865796',passwd='1',expect=True,*args):
        self.myAccount()
        self.login(phone_num,passwd,expect)

    #通过更多-我的帐号模块进入，注册
    def myaccout_sign(self,phone_num=testdata.sign_num,sign_pwd=testdata.sign_pwd,expect=True):
        self.myAccount()
        return self.sign(phone_num,sign_pwd,expect)

    #登陆后修改登陆密码
    def modify_loginpwd_after_login(self,phone_num='13735865796',passwd='654321',old_pwd='654321',set_pwd='654321',repeat_pwd='654321',expect=True):
        self.myaccout_login(phone_num,passwd)
        sleep(3)
        self.click_set_btn()
        self.rl_pwd_manager()
        self.modify_login_pwd(old_pwd,set_pwd,repeat_pwd,expect)


    #修改登陆密码失败，原密码错误
    def modify_loginpwd_after_login_error1(self,phone_num='13735865796',passwd='654321',old_pwd='123456',set_pwd='',repeat_pwd='',expect=True):
        self.myaccout_login(phone_num,passwd)
        sleep(3)
        self.click_set_btn()
        self.rl_pwd_manager()
        self.modify_login_pwd(old_pwd,set_pwd,repeat_pwd,expect)

    #原密码正确，新置密码与重复新置密码不一致
    def modify_loginpwd_after_login_error2(self,phone_num='13735865796',passwd='654321',old_pwd='654321',set_pwd='654321',repeat_pwd='123456',expect=True):
        self.myaccout_login(phone_num,passwd)
        sleep(3)
        self.click_set_btn()
        self.rl_pwd_manager()
        self.modify_login_pwd(old_pwd,set_pwd,repeat_pwd,expect)

    #密码为空
    def modify_loginpwd_after_login_error3(self,phone_num='13735865796',passwd='654321',old_pwd='65432',set_pwd='',repeat_pwd='123456',expect=True):
        self.myaccout_login(phone_num,passwd)
        sleep(3)
        self.click_set_btn()
        self.rl_pwd_manager()
        self.modify_login_pwd(old_pwd,set_pwd,repeat_pwd,expect)

    #登陆后修改交易密码
    def modify_trade_pwd_after_login(self,phone_num='13735865796',passwd='654321',old_trade_pwd='654321',new_trade_pwd='654321',repeat_trade_pwd='654322',expect=True):
        self.myaccout_login(phone_num,passwd)
        sleep(3)
        self.click_set_btn()
        self.rl_pwd_manager()
        self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

    #原交易密码与手机号不匹配
    def modify_trade_pwd_after_login_error1(self,phone_num='13735865796',passwd='654321',old_trade_pwd='123456',new_trade_pwd='654321',repeat_trade_pwd='654321',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.click_myaccount()
        self.rl_pwd_manager()
        self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

    #原交易密码位数不够
    def modify_trade_pwd_after_login_error2(self,phone_num='13735865796',passwd='654321',old_trade_pwd='65432',new_trade_pwd='654321',repeat_trade_pwd='',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.click_myaccount()
        self.rl_pwd_manager()
        self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

    #原交易密码正确，新交易密码位数不够
    def modify_trade_pwd_after_login_error3(self,phone_num='13735865796',passwd='654321',old_trade_pwd='654321',new_trade_pwd='65432',repeat_trade_pwd='65432',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.click_myaccount()
        self.rl_pwd_manager()
        self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

    #原交易密码正确，新交易密码位数正确。重复新交易密码位数不够
    def modify_trade_pwd_after_login_error4(self,phone_num='13735865796',passwd='654321',old_trade_pwd='654321',new_trade_pwd='654321',repeat_trade_pwd='12345',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.click_myaccount()
        self.rl_pwd_manager()
        self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

    #原交易密码正确，新交易密码位数正确。重复新交易密码与新交易密码不匹配
    def modify_trade_pwd_after_login_error5(self,phone_num='13735865796',passwd='654321',old_trade_pwd='654321',new_trade_pwd='654321',repeat_trade_pwd='123456',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.click_myaccount()
        self.rl_pwd_manager()
        self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

    #登陆后找回交易密码
    def back_trade_pwd_after_login(self,phone_num='13735865796',passwd='654321',username=u'吴越欣',card='330522199009256911',new_trade_pwd='654321',repeat_trade_pwd='654321',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.click_myaccount()
        self.rl_pwd_manager()
        self.back_trade_pwd(username,card,new_trade_pwd,repeat_trade_pwd,expect)

    #4.2版本余额充值
    def balance_into4(self,phone_num='13735865796',passwd='654321',topup_num='100',trade_pwd='654321',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.enter_balance()
        self.click_recharge()
        self.top_up(topup_num,trade_pwd,expect)

    #转入金额错误
    def balance_into4_error1(self,phone_num='13735865796',passwd='654321',topup_num='-1',trade_pwd='654321',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.enter_balance()
        self.click_recharge()
        self.top_up(topup_num,trade_pwd,expect)

    #交易密码错误
    def balance_into4_error2(self,phone_num='13735865796',passwd='654321',topup_num='100',trade_pwd='123456',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.enter_balance()
        self.click_recharge()
        self.top_up(topup_num,trade_pwd,expect)

    #交易密码位数不够
    def balance_into4_error3(self,phone_num='13735865796',passwd='654321',topup_num='100',trade_pwd='12345',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.enter_balance()
        self.click_recharge()
        self.top_up(topup_num,trade_pwd,expect)

    #4.2以上版本余额充值
    def balance_into5(self,phone_num=testdata.phone_num,passwd=testdata.passwd,topup_num=testdata.topup_num,trade_pwd=testdata.trade_pwd,expect='余额成功充值'):
        #self.myaccout_login(phone_num,passwd)
        self.click_myasset()
        if self.isElement("xpath",tbjpyios.myasset_cancel)==True:
            self.click_button((By.XPATH,tbjpyios.myasset_cancel))
            if self.isElement("name",tbjpyios.earn_monkey)==False:
                self.click_balance5()
                self.click_recharge()
                return self.top_up(topup_num,trade_pwd,expect)
            else:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.click_balance5()
                self.click_recharge()
                return self.top_up(topup_num,trade_pwd,expect)
        else:
            if self.isElement("name",tbjpyios.earn_monkey)==False:
                self.click_balance5()
                self.click_recharge()
                return self.top_up(topup_num,trade_pwd,expect)
            else:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.click_balance5()
                self.click_recharge()
                return self.top_up(topup_num,trade_pwd,expect)

    #转入金额错误
    def balance_into5_error1(self,phone_num='13735865796',passwd='654321',topup_num='',trade_pwd='654321',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.enter_balance5()
        self.click_recharge()
        self.top_up(topup_num,trade_pwd,expect)

    #交易密码错误
    def balance_into5_error2(self,phone_num='13735865796',passwd='654321',topup_num='100',trade_pwd='123456',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.enter_balance5()
        self.click_recharge()
        self.top_up(topup_num,trade_pwd,expect)

    #交易密码位数不够
    def balance_into5_error3(self,phone_num='13735865796',passwd='654321',topup_num='100',trade_pwd='12345',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.enter_balance5()
        self.click_recharge()
        self.top_up(topup_num,trade_pwd,expect)

    #4.2版本余额提现
    def balance_out4(self,phone_num='13735865796',passwd='654321',out_num='100',trade_pwd='654321',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.enter_balance()
        self.click_balance_out()
        self.cash(out_num,trade_pwd,expect)

    #4.2版本余额提现，转出金额错误
    def balance_out4_error1(self,phone_num='13735865796',passwd='654321',out_num='-1',trade_pwd='654321',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.enter_balance()
        self.click_balance_out()
        self.cash(out_num,trade_pwd,expect)

    #4.2版本余额提现，交易密码与手机号不匹配
    def balance_out4_error2(self,phone_num='13735865796',passwd='654321',out_num='100',trade_pwd='123456',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.enter_balance()
        self.click_balance_out()
        self.cash(out_num,trade_pwd,expect)

    #4.2版本余额提现，交易密码位数不够
    def balance_out4_error3(self,phone_num='13735865796',passwd='654321',out_num='100',trade_pwd='12345',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.enter_balance()
        self.click_balance_out()
        self.cash(out_num,trade_pwd,expect)

    #4.2以上版本余额提现
    def balance_out5(self,phone_num=testdata.phone_num,passwd=testdata.passwd,out_num=testdata.out_num,trade_pwd=testdata.trade_pwd,expect='余额成功提现'):
        self.click_myasset()
        if self.isElement("xpath",tbjpyios.myasset_cancel)==True:
            self.click_button((By.XPATH,tbjpyios.myasset_cancel))
            if self.isElement("name",tbjpyios.earn_monkey)==False:
                self.click_balance5()
                self.click_balance_out()
                return self.cash(out_num,trade_pwd,expect)
            else:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.click_balance5()
                self.click_balance_out()
                return self.cash(out_num,trade_pwd,expect)
        else:
            if self.isElement("name",tbjpyios.earn_monkey)==False:
                self.click_balance5()
                self.click_balance_out()
                return self.cash(out_num,trade_pwd,expect)
            else:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.click_balance5()
                self.click_balance_out()
                return self.cash(out_num,trade_pwd,expect)

    #转入金额错误
    def balance_out5_error1(self,phone_num='13735865796',passwd='654321',out_num='',trade_pwd='65432',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.enter_balance5()
        self.click_balance_out()
        return self.cash(out_num,trade_pwd,expect)

    #交易密码错误
    def balance_out5_error2(self,phone_num='13735865796',passwd='654321',out_num='100',trade_pwd='123456',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.enter_balance5()
        self.click_balance_out()
        self.cash(out_num,trade_pwd,expect)

    #交易密码位数不够
    def balance_out5_error3(self,phone_num='13735865796',passwd='654321',out_num='100',trade_pwd='12345',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.enter_balance5()
        self.click_balance_out()
        self.cash(out_num,trade_pwd,expect)

    #5.1精品推荐
    def buy_hot_product_5(self,phone_num=testdata.phone_num,passwd=testdata.passwd,amount2=testdata.tongbaoin_num,amount3=testdata.normal_product_num,trade_num=testdata.trade_pwd,expect=True):
        sleep(3)
        self.hot_product()
        sleep(3)
        if self.isElement("name",tbjpyios.hot_product_login)==True:
            self.click_button((By.NAME,tbjpyios.hot_product_login))
            self.login(phone_num,passwd)
            return self.buy_hot_product51(amount2,amount3,trade_num,expect)
        else:
            return self.buy_hot_product51(amount2,amount3,trade_num,expect)

    #5.0理财产品铜宝转入
    def buy_financing_products_tongbao_in(self,phone_num=testdata.phone_num,passwd=testdata.passwd,amount=testdata.tongbaoin_num,trade_num=testdata.trade_pwd,expect='铜宝转入成功'):
        self.financing_products_info()
        sleep(3)
        self.click_financing_products_tb()
        sleep(3)
        if self.isElement("name",tbjpyios.buy_tongbao_login_check)==False:
            self.click_tongbao_login()
            self.login(phone_num,passwd)
            if self.isElement("name",tbjpyios.tongbao_in)==True:
                return self.tongbaoin(amount,trade_num,expect)
            else:
                pass
        else:
            if self.isElement("name",tbjpyios.tongbao_in)==True:
                return self.tongbaoin(amount,trade_num,expect)
            else:
                pass

    #5.0以上我的资产，铜宝转入
    def myassert_tongbao_in(self,phone_num=testdata.phone_num,passwd=testdata.passwd,amount=testdata.tongbaoin_num,trade_num=testdata.trade_pwd,expect='铜宝转入成功'):
        self.click_myasset()
        if self.isElement("xpath",tbjpyios.myasset_cancel)==True:
            self.click_button((By.XPATH,tbjpyios.myasset_cancel))
            if self.isElement("name",tbjpyios.earn_monkey)==False:
                self.click_button((By.XPATH,tbjpyios.myasset_tongbao))
                return self.tongbaoin(amount,trade_num,expect)
            else:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.click_button((By.XPATH,tbjpyios.myasset_tongbao))
                return self.tongbaoin(amount,trade_num,expect)
        else:
            if self.isElement("name",tbjpyios.earn_monkey)==False:
                self.click_button((By.XPATH,tbjpyios.myasset_tongbao))
                return self.tongbaoin(amount,trade_num,expect)
            else:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.click_button((By.XPATH,tbjpyios.myasset_tongbao))
                return self.tongbaoin(amount,trade_num,expect)

    #5.0以上我的资产，铜宝转出
    def myassert_tongbao_out(self,phone_num=testdata.phone_num,passwd=testdata.passwd,amount=testdata.tongbaoout_num,trade_num=testdata.trade_pwd,expect='铜宝转出成功'):
        self.click_myasset()
        if self.isElement("xpath",tbjpyios.myasset_cancel)==True:
            self.click_button((By.XPATH,tbjpyios.myasset_cancel))
            if self.isElement("name",tbjpyios.earn_monkey)==False:
                self.click_button((By.XPATH,tbjpyios.myasset_tongbao))
                return self.tongbaoout(amount,trade_num,expect)
            else:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.click_button((By.XPATH,tbjpyios.myasset_tongbao))
                return self.tongbaoout(amount,trade_num,expect)
        else:
            if self.isElement("name",tbjpyios.earn_monkey)==False:
                self.click_button((By.XPATH,tbjpyios.myasset_tongbao))
                return self.tongbaoout(amount,trade_num,expect)
            else:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.click_button((By.XPATH,tbjpyios.myasset_tongbao))
                return self.tongbaoout(amount,trade_num,expect)

    #购买金额错误
    def buy_financing_products_tongbao_in_error1(self,phone_num='13735865796',passwd='654321',amount='',trade_num='65432',expect=True):
        self.financing_products_info()
        sleep(3)
        self.click_financing_products_tb()
        sleep(3)
        if self.isElement("name",tbjpyios.buy_tongbao_login_check)==False:
            self.click_tongbao_login()
            self.login(phone_num,passwd)
            if self.isElement("name",tbjpyios.tongbao_in)==True:
                return self.tongbaoin(amount,trade_num,expect)
            else:
                pass
        else:
            if self.isElement("name",tbjpyios.tongbao_in)==True:
                return self.tongbaoin(amount,trade_num,expect)
            else:
                pass

    #交易密码错误
    def buy_financing_products_tongbao_in_error2(self,phone_num='13735865796',passwd='654321',amount='100',trade_num='654322',expect=True):
        self.financing_products_info()
        sleep(3)
        self.click_financing_products_tb()
        sleep(3)
        if self.isElement("name",tbjpyios.buy_tongbao_login_check)==False:
            self.click_tongbao_login()
            self.login(phone_num,passwd)
            if self.isElement("name",tbjpyios.tongbao_in)==True:
                self.tongbaoin(amount,trade_num,expect)
            else:
                pass
        else:
            if self.isElement("name",tbjpyios.tongbao_in)==True:
                self.tongbaoin(amount,trade_num,expect)
            else:
                pass

    #交易密码位数不够
    def buy_financing_products_tongbao_in_error3(self,phone_num='13735865796',passwd='654321',amount='100',trade_num='65432',expect=True):
        self.financing_products_info()
        sleep(3)
        self.click_financing_products_tb()
        sleep(3)
        if self.isElement("name",tbjpyios.buy_tongbao_login_check)==False:
            self.click_tongbao_login()
            self.login(phone_num,passwd)
            if self.isElement("name",tbjpyios.tongbao_in)==True:
                self.tongbaoin(amount,trade_num,expect)
            else:
                pass
        else:
            if self.isElement("name",tbjpyios.tongbao_in)==True:
                self.tongbaoin(amount,trade_num,expect)
            else:
                pass

    #5.0理财产品铜宝转出
    def buy_financing_products_tongbao_out(self,phone_num=testdata.phone_num,passwd=testdata.passwd,amount=testdata.tongbaoout_num,trade_num=testdata.trade_pwd,expect='铜宝转出成功'):
        self.financing_products_info()
        sleep(3)
        self.click_financing_products_tb()
        sleep(3)
        if self.isElement("name",tbjpyios.buy_tongbao_login_check)==False:
            self.click_tongbao_login()
            self.login(phone_num,passwd)
            if self.isElement("name",tbjpyios.tongbao_out)==True:
                return self.tongbaoout(amount,trade_num,expect)
            else:
                pass
        else:
            if self.isElement("name",tbjpyios.tongbao_out)==True:
                return self.tongbaoout(amount,trade_num,expect)
            else:
                pass

    #购买金额错误
    def buy_financing_products_tongbao_out_error1(self,phone_num='13735865796',passwd='654321',amount='',trade_num='654321',expect=True):
        self.financing_products_info()
        sleep(3)
        self.click_financing_products_tb()
        sleep(3)
        if self.isElement("name",tbjpyios.buy_tongbao_login_check)==False:
            self.click_tongbao_login()
            self.login(phone_num,passwd)
            if self.isElement("name",tbjpyios.tongbao_out)==True:
                self.tongbaoout(amount,trade_num,expect)
            else:
                pass
        else:
            if self.isElement("name",tbjpyios.tongbao_out)==True:
                self.tongbaoout(amount,trade_num,expect)
            else:
                pass

    #交易密码错误
    def buy_financing_products_tongbao_out_error2(self,phone_num='13735865796',passwd='654321',amount=100,trade_num='123456',expect=True):
        self.financing_products_info()
        sleep(3)
        self.click_financing_products_tb()
        sleep(3)
        if self.isElement("name",tbjpyios.buy_tongbao_login_check)==False:
            self.click_tongbao_login()
            self.login(phone_num,passwd)
            if self.isElement("name",tbjpyios.tongbao_out)==True:
                self.tongbaoout(amount,trade_num,expect)
            else:
                pass
        else:
            if self.isElement("name",tbjpyios.tongbao_out)==True:
                self.tongbaoout(amount,trade_num,expect)
            else:
                pass

    #交易密码位数不够
    def buy_financing_products_tongbao_out_error3(self,phone_num='13735865796',passwd='654321',amount=100,trade_num='12345',expect=True):
        self.financing_products_info()
        sleep(3)
        self.click_financing_products_tb()
        sleep(3)
        if self.isElement("name",tbjpyios.buy_tongbao_login_check)==False:
            self.click_tongbao_login()
            self.login(phone_num,passwd)
            if self.isElement("name",tbjpyios.tongbao_out)==True:
                self.tongbaoout(amount,trade_num,expect)
            else:
                pass
        else:
            if self.isElement("name",tbjpyios.tongbao_out)==True:
                self.tongbaoout(amount,trade_num,expect)
            else:
                pass


    #5.0版本以上理财产品购买
    def finance_products51(self,amount2=testdata.tongbaoin_num,amount3=testdata.normal_product_num,recharge_num=testdata.recharge_num,trade_num=testdata.trade_pwd,expect=True):
        self.financing_products()
        return self.buy_financing_products5(amount2,amount3,recharge_num,trade_num,expect)

    #我的资产
    def myassert(self):
        self.click_button(())
        self.click_button((By.NAME,'开始赚钱'))

    #5.3版本更多模块-查看
    def more_check53(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        try:
            code=11
            self.click_more()
            self.click_login51()
            #查看我的账户并截图
            if self.isElement("xpath",tbjpyios.phoneId)==True:
                self.input_login_phone(phone_num)
                self.click_next()
                self.input_login_passwd(passwd)
                self.click_login_button()
                self.click_login51()
            sleep(4)
            self.screenshot()
            self.back()
            #查看邀请好友并截图
            self.click_button((By.XPATH,tbjpyios.login51))
            sleep(5)
            self.screenshot()
            self.back()
            self.click_button((By.XPATH,tbjpyios.risk))
            sleep(5)
            self.screenshot()
            self.back()
            self.click_button((By.XPATH,tbjpyios.customer_service))
            sleep(5)
            self.screenshot()
            self.back()
            self.click_button((By.XPATH,tbjpyios.settings))
            sleep(5)
            self.screenshot()
            self.back()
            self.click_button((By.XPATH,tbjpyios.about_tbj))
            sleep(5)
            self.screenshot()
            self.click_button((By.XPATH,tbjpyios.back3))
            actual=True
            e='成功'
        except Exception,e:
            actual=False
            e='失败'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #5.1我的资产页的信息中心滑动查看功能
    def myproperty_message_slide51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        self.click_myasset()
        if self.isElement("xpath",tbjpyios.myasset_cancel)==True:
            self.click_button((By.XPATH,tbjpyios.myasset_cancel))
            if self.isElement("name",tbjpyios.earn_monkey)==True:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.myproperty()
                return self.message_slide(expect)
            else:
                return self.message_slide(expect)
        else:
            if self.isElement("name",tbjpyios.earn_monkey)==True:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.myproperty()
                return self.message_slide(expect)
            else:
                return self.message_slide(expect)

    #5.1我的资产页的当前收益滑动查看功能
    def myproperty_nowincome_slide51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        self.click_myasset()
        if self.isElement("xpath",tbjpyios.myasset_cancel)==True:
            self.click_button((By.XPATH,tbjpyios.myasset_cancel))
            if self.isElement("name",tbjpyios.earn_monkey)==True:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.myproperty()
                return self.now_income43(expect)
            else:
                return self.now_income43(expect)
        else:
            if self.isElement("name",tbjpyios.earn_monkey)==True:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.myproperty()
                return self.now_income43(expect)
            else:
                return self.now_income43(expect)

    #5.1我的资产页的交易记录滑动查看功能
    def myproperty_all_trade_record_slide51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        self.click_myasset()
        if self.isElement("xpath",tbjpyios.myasset_cancel)==True:
            self.click_button((By.XPATH,tbjpyios.myasset_cancel))
            if self.isElement("name",tbjpyios.earn_monkey)==True:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.myproperty()
                return self.check_all_trade_record43(expect)
            else:
                return self.check_all_trade_record43(expect)
        else:
            if self.isElement("name",tbjpyios.earn_monkey)==True:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.myproperty()
                return self.check_all_trade_record43(expect)
            else:
                return self.check_all_trade_record43(expect)

    #5.1我的资产页的铜宝收益滑动查看功能
    def myproperty_tongbao_income_slide51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        self.click_myasset()
        if self.isElement("xpath",tbjpyios.myasset_cancel)==True:
            self.click_button((By.XPATH,tbjpyios.myasset_cancel))
            if self.isElement("name",tbjpyios.earn_monkey)==True:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.myproperty()
                return self.check_tongbao_income43(expect)
            else:
                return self.check_tongbao_income43(expect)
        else:
            if self.isElement("name",tbjpyios.earn_monkey)==True:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.myproperty()
                return self.check_tongbao_income43(expect)
            else:
                return self.check_tongbao_income43(expect)

    #5.1我的投资查看，滑动
    def check_my_investment51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        self.click_myasset()
        if self.isElement("xpath",tbjpyios.myasset_cancel)==True:
            self.click_button((By.XPATH,tbjpyios.myasset_cancel))
            if self.isElement("name",tbjpyios.earn_monkey)==True:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.myproperty()
                return self.my_investment_slide43(expect)
            else:
                return self.my_investment_slide43(expect)
        else:
            if self.isElement("name",tbjpyios.earn_monkey)==True:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.myproperty()
                return self.my_investment_slide43(expect)
            else:
                return self.my_investment_slide43(expect)

    #5.3我的资产页面。我的优惠，我的T码，我的铜板
    def my_assert_other(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        self.click_myasset()
        if self.isElement("xpath",tbjpyios.myasset_cancel)==True:
            self.click_button((By.XPATH,tbjpyios.myasset_cancel))
            if self.isElement("name",tbjpyios.earn_monkey)==True:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.myproperty()
                return self.my_assert_other_check(expect)
            else:
                return self.my_assert_other_check(expect)
        else:
            if self.isElement("name",tbjpyios.earn_monkey)==True:
                self.click_button((By.NAME,tbjpyios.earn_monkey))
                self.login(phone_num,passwd)
                self.myproperty()
                return self.my_assert_other_check(expect)
            else:
                return self.my_assert_other_check(expect)

import threading

if __name__ == '__main__':
    t = Case('iOS','7.1','','','b4769de98e88456257761f2eb0a8add30d27b89d','com.tongbanjie.pro','','')

    #重构后的组织用例
    # t.add_case('myaccout_login',t.myaccout_login)
    # t.add_case('myaccout_sign',t.myaccout_sign)

    # t.add_case('balance_out4',t.balance_out4)
    # t.add_case('balance_into4',t.balance_into4)
    # t.add_case('balance_out5',t.balance_out5)
    # t.add_case('balance_into5',t.balance_into5)

    #购买流程
    # t.add_case('buy_hot_product',t.buy_hot_product)
    t.add_case('buy_hot_product_5',t.buy_hot_product_5)
    # t.add_case('buy_financing_products',t.buy_financing_products)
    t.add_case('finance_products51',t.finance_products51)
    # t.add_case('buy_financing_products_tongbao_in',t.buy_financing_products_tongbao_in)
    # t.add_case('buy_financing_products_tongbao_out',t.buy_financing_products_tongbao_out)

    # t.add_case('myassert_tongbao_in',t.myassert_tongbao_in)
    # t.add_case('myassert_tongbao_out',t.myassert_tongbao_out)
    #
    # t.add_case('myproperty_message_slide51',t.myproperty_message_slide51)
    # t.add_case('myproperty_nowincome_slide51',t.myproperty_nowincome_slide51)
    # t.add_case('myproperty_all_trade_record_slide51',t.myproperty_all_trade_record_slide51)
    # t.add_case('myproperty_tongbao_income_slide51',t.myproperty_tongbao_income_slide51)
    # t.add_case('more_check53',t.more_check53)
    # t.add_case('my_assert_other',t.my_assert_other)


    def start():
        t.run()
    thread_1 = threading.Thread(target=start,name='thread_1')
    thread_1.setDaemon(True)
    thread_1.start()

    while not t.finsh_flag:
        data = t.stdout.readline()
        if data:
            print data
