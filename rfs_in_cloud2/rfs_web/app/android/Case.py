# _*_ coding:utf-8 _*_
__author__ = 'Eddie'

import re
from selenium.webdriver.common.by import By
from time import sleep

import TerminalHandle
import sql
import tbjpy


class Case(TerminalHandle.AppHandle, TerminalHandle.Data):
    def __init__(self,platformName,platfromVersion,deviceName,udid,appPackage,appActivity,host=None,port=None,timeout=None,**kwargs):
        super(Case,self).__init__(platformName,platfromVersion,deviceName,udid,appPackage,appActivity,host,port,timeout=None,**kwargs)

    testdata= TerminalHandle.Data()
    #date=Date()
    #进入我的账户
    def myAccount(self):
        u"""进入我的账户"""
        #print 1
        self.click_more()
        #print 2
        #点击“我的账户”,然后进行账号的登录操作
        self.click_myaccount()

    #登录功能
    def login(self,phone_num,passwd,expect=None,ending=None,*args):
        actual=True
        code=111
        try:
            if self.isElement("id", tbjpy.input_phone)==False:
                # print 222
                e='用户已登录'
                self.back()
            else:
                sleep(2)
                self.input_login_phone(phone_num)
                self.click_next()
                self.input_login_passwd(passwd)
                self.click_login_button()
                sleep(3)
                if self.isElement("id", tbjpy.check_login_fail)==True:
                    #self.screenshot_Error()
                    #actual=False
                    e='手机号和密码不匹配'
                    self.back()
                    self.back()
                    pass
                else:
                    #self.screenshot_True()
                    actual=True
                    e='登录成功'
                    #self.click_myaccount()
                    #self.logout()
        except Exception,e:
                #e = str(e)
            actual=False
        finally:
                #print expect,e
            result=str(e)==str(expect)
            #print str(e),str(expect),str(result)
            ending={'code':code,'message':e,'result':result}
            return ending

    #注册
    def sign(self,phone_num,sign_pwd,expect=True,ending=None,*args):
        actual=None
        code=111
        try:
            if self.isElement("id", tbjpy.input_phone)==False:
                e='用户已登录'
                actual=False
                self.back()
            else:
                self.input_sign_Account(phone_num)
                if self.isElement("id", tbjpy.input_login_passwd)==True:
                    e='已注册的帐号'
                    actual=False
                    pass
                else:
                    sleep(5)
                    myms = sql.mysql_connect(sql.db_info)
                    yzm=myms.sql_assign_exec("select content from mdp_message WHERE recipients="+ phone_num+ " ORDER BY create_time DESC LIMIT 1")
                    yzm1=re.search('\d{4}', yzm)
                    yzm2=yzm1.group(0)
                    self.send_keys((By.ID, tbjpy.verify_input), yzm2)
                    self.send_signpwd(sign_pwd)
                    self.click_complete_btn()
                    sleep(3)
                    if self.isElement("id", tbjpy.sign_fail_check)==True:
                        #self.screenshot_Error()
                        actual=False
                        e='注册失败'
                    else:
                        #self.screenshot_True()
                        actual=True
                        e='注册成功'
        except Exception,e:
            actual=False
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #@util.decorate
    #点击查看用户个人信息
    def user_info(self):
        sleep(5)
        #print 1
        self.click_myaccount()
        #u"""查看用户个人信息"""
        self.click_user_infojr()
        #print 3
        if self.isElement("id", tbjpy.true)==True:
            #print 1
            self.click_bankcard_manager()
            #选择中国银行
            self.add_bankcard()
            #输入持卡人信息
            self.add_personalInformation()
            self.add_bank_card()
            self.send_bank_card()
            #输入手机号并绑定
            self.send_phone_num()
            #输入验证码并点击完成按钮
            self.send_verifycode_sure()
        else:
            #print 2
            self.verify_person_info()

    #进入密码管理模块
    def pwd_manager(self):
        self.click_myaccount()
        #u"""密码管理"""
        self.rl_pwd_manager()

    #修改登录密码
    def modify_login_pwd(self,old_pwd,set_pwd,repeat_pwd,expect=True,ending=None):
        actual=None
        code=111
        try:
        #修改登录密码
            self.change_login_pwd_layout()
            self.send_old_pwd(old_pwd)
            self.set_pwd(set_pwd,repeat_pwd)
            #sleep(5)
            self.driver.implicitly_wait(10)
            if self.isElement("id", tbjpy.check_pwd_success)==True:
                #self.screenshot_True()
                e='修改登录密码成功'
                self.back()
                self.back()
                #self.logout()
                actual=True
            else:
                #print 2
                e='修改登录密码失败'
                self.back()
                self.back()
                self.back()
                #self.logout()
                #self.screenshot_Error()
                actual=False
        except Exception,e:
            actual=False
        finally:
            result=str(e)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #修改交易密码
    def modify_trade_pwd(self,old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect=True):
        actual=None
        code=111
        try:
            self.rlyt_update_trans_pwd()
            self.send_old_trade_pwd(old_trade_pwd)
            self.send_new_trade_pwd(new_trade_pwd)
            self.send_repeat_trade_pwd(repeat_trade_pwd)
            self.click_complete_btn()
            self.driver.implicitly_wait(10)
            if self.isElement("id", tbjpy.check_pwd_success)==True:
                self.screenshot()
                e='修改交易密码成功'
                self.back()
                self.back()
                #self.logout()
                actual=True
            elif self.isElement("id", tbjpy.pwd_dialog_message_text)==True:
                actual=False
                #self.screenshot()
                pwd_dialog_message_text=self.driver.find_element_by_id(tbjpy.pwd_dialog_message_text).get_attribute("name")
                #print pwd_dialog_message_text
                self.click_button((By.ID, tbjpy.click_sure))
                self.back1()
                self.back()
                self.back()
                #self.back()
                #self.logout()
                e='两次密码输入不一致'
            else:
                self.screenshot()
                actual=False
                e='修改交易密码失败'
        except Exception,e:
            actual=False
        finally:
            #print e,expect
            result=str(e)==str(expect)
            #print result
            ending={'code':code,'message':e,'result':result}
            return ending

    #找回交易密码
    def back_trade_pwd(self,username,card,new_trade_pwd,repeat_trade_pwd,expect=True,ending=None):
        actual=None
        code=111
        try:
            self.find_trade_pwd(username,card)
            self.send_new_trade_pwd(new_trade_pwd)
            self.send_repeat_trade_pwd(repeat_trade_pwd)
            self.click_complete_btn()
            if self.isElement("id", tbjpy.check_pwd_success)==True:
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
            # print actual,expect,ending
            # print actual==expect
            return ending

    #进入余额模块
    def enter_balance(self):
        #点击我的账户
        #self.click_myaccount()
        #点击账户余额
        self.click_account_balance()
        self.driver.implicitly_wait(10)

    #账户余额一充值
    def top_up(self,topup_num,trade_pwd,expect=True,ending=None):
        actual=None
        code=111
        try:
            #充值
            self.rl_recharge(topup_num)
            #输入铜板街交易密码
            self.send_trade_pwd(trade_pwd)
            self.click_sure()
            sleep(7)
            if self.isElement("xpath", tbjpy.check_money_success)==True:
                self.screenshot()
                actual=True
                self.click_button((By.XPATH, tbjpy.check_money_success))
                if self.isElement("xpath", tbjpy.check_money_success)==False:
                    e='余额成功充值'
                    self.back()
                    self.back()
            else:
                self.screenshot()
                actual=False
                self.back()
                e='账户余额充值失败'
        except Exception,e:
            actual=False
        finally:
            result=str(e)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #余额提现
    def cash(self,out_num,trade_pwd,expect=True,ending=None):
        actual=None
        code=111
        try:
            self.rl_balance_out(out_num)
            sleep(1)
            self.send_trade_pwd(trade_pwd)
            self.click_sure()
            sleep(5)
            if self.isElement("xpath", tbjpy.check_money_success)==True:
                print 223
                self.screenshot()
                actual=True
                #e='余额成功提现'
                self.click_button((By.XPATH, tbjpy.check_money_success))
                if self.isElement("xpath", tbjpy.check_money_success)==False:
                    e='余额成功提现'
                    self.back()
                    self.back()
                else:
                    pass
            else:
                self.screenshot()
                actual=False
                self.back()
                e='余额提现失败'
        except Exception,e:
            actual=False
        finally:
            result=str(e)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #4.3账户余额一充值
    def top_up43(self,topup_num,trade_pwd,expect=True,ending=None):
        actual=None
        code=111
        try:
            #充值
            self.rl_recharge43(topup_num)
            #输入铜板街交易密码
            self.send_trade_pwd(trade_pwd)
            self.click_sure43()
            sleep(7)
            if self.isElement("xpath", tbjpy.check_money_success)==True:
                self.screenshot()
                actual=True
                self.click_button((By.XPATH, tbjpy.check_money_success))
                if self.isElement("xpath", tbjpy.check_money_success)==False:
                    e='余额成功充值'
                    self.back()
                    #self.back()
            else:
                self.screenshot()
                actual=False
                e='账户余额充值失败'
        except Exception,e:
            actual=False
        finally:
            result=str(e)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #4.3余额提现
    def cash43(self,out_num,trade_pwd,expect=True,ending=None):
        actual=None
        code=111
        try:
            self.rl_balance_out43(out_num)
            sleep(1)
            self.send_trade_pwd(trade_pwd)
            self.click_sure43()
            sleep(5)
            if self.isElement("xpath", tbjpy.check_money_success)==True:
                # print 66
                self.screenshot()
                actual=True
                #e='余额成功提现'
                self.click_button((By.XPATH, tbjpy.check_money_success))
                if self.isElement("xpath", tbjpy.check_money_success)==False:
                    e='余额成功提现'
                    self.back()
                    #self.back()
                else:
                    pass
            else:
                self.screenshot()
                actual=False
                e='余额提现失败'
        except Exception,e:
            actual=False
        finally:
            result=str(e)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #回款路径
    def path(self,new_people_trade_pwd,trade_pwd,repeat_trade_pwd,expect=True,ending=None):
        u"""回款路径"""
        #点击我的账户
        sleep(4)
        self.click_myaccount()
        actual=None
        try:
            self.click_return_path_label()
            #设置用户交易密码
            if self.isElement("xpath", tbjpy.label)==True:
                self.set_new_people_trade_pwd(new_people_trade_pwd,repeat_trade_pwd)
                #以安装键盘做参照物，若还存在，则设置交易密码失败；反之
                if self.isElement("id", tbjpy.key)==True:
                    actual=False
                else:
                    actual=True
            #输入用户交易密码
            else:
                self.send_trade_pwd(trade_pwd)
                self.click_sure()
            #选择回款路径
            #账户余额
                self.click_bank()
                if self.isElement("xpath", tbjpy.tcqd)==True:
                    self.click_banksure()
                    #print u"选择回款路径成功"
                else:
                    self.back()
                    #print u"返回成功"
        except Exception,e:
            actual=False
        finally:
            print actual,expect
            print actual==expect
            return actual==expect


    #忘记密码后，找回密码
    def back_pwd(self,phone_num='13735865796',person_ID='330522199009256911',new_pwd='654321',expect=True,ending=None):
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
            sleep(4)
            yzm=myms.sql_assign_exec("select content from mdp_message WHERE recipients="+ phone_num + " ORDER BY create_time DESC LIMIT 1")
            yzm1=re.search('\d{4}', yzm)
            yzm2=yzm1.group(0)
            self.send_keys((By.ID, tbjpy.verify_input), yzm2)
            self.click_back_pwd(new_pwd)
            self.click_complete_btn()
            sleep(5)
            if self.isElement("id", tbjpy.check_find_pwd)==True:
                self.screenshot()
                actual=False
                e='找回密码设置失败'
            else:
                self.screenshot()
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
        #self.ll_top_content()
        pass

    #进入理财产品模块
    def financing_products(self):
        self.tab_financing_products()

    #选择第一个理财产品
    def click_first_financing_products(self):
        self.click_frist_financing_product()
        self.click_product_purchase_view()



    #铜宝转出流程
    def tongbaoout(self,amount,trade_num,expect=True,ending=None):
        actual=None
        code=111
        try:
            self.tongbao_out()
            self.send_buy_money(amount)
            self.send_buy_monkey_sure()
            self.send_trade_pwd(trade_num)
            self.click_sure()
            sleep(6)
            if self.isElement("xpath", tbjpy.check_buy_success_btn)==True:
                self.screenshot_True()
                actual=True
                e='铜宝转出成功'
                self.click_button((By.XPATH, tbjpy.check_buy_success_btn))
                print 22
                self.back()
                print 221
            else:
                self.screenshot_Error()
                actual=False
                e='铜宝转出失败'
        except Exception,e:
            actual=False
        finally:
            result=str(e)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #设置新用户交易密码是否成功功能
    def set_new_people_trade_pwd_check(self,new_people_trade_pwd,repeat_trade_pwd,expect):
        actual=None
        code=111
        try:
            self.set_new_people_trade_pwd(new_people_trade_pwd,repeat_trade_pwd)
            sleep(6)
            if self.isElement("xpath", tbjpy.check_set_newpeople_tradepwd_fail)==True:
                actual=False
                e='购买失败'
            else:
                actual=True
                e='购买成功'
                self.click_button((By.ID, tbjpy.complete_btn))
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

    def buy_hot_product(self):
        self.hot_product()

    #4.3-5.0版本账户余额入口
    def enter_balance5(self):
        #self.click_myasset()
        #print 1
        self.click_balance5()
        #print 2

     #5.0版本理财产品铜宝入口
    def click_financing_products_tb(self):
        self.click_button((By.XPATH, tbjpy.financing_products_tb))

    #理财产品页信息
    def financing_products_info(self):
        self.tab_financing_products()
        second_financing_name=self.driver.find_element_by_xpath(tbjpy.second_financing_name).get_attribute("text")
        #print second_financing_name
        third_financing_name=self.driver.find_element_by_xpath(tbjpy.third_financing_name).get_attribute("text")
        #print third_financing_name
        fourth_financing_name=self.driver.find_element_by_xpath(tbjpy.fourth_financing_name).get_attribute("text")
        #print fourth_financing_name

    '''重构后的组织用例'''
    #通过更多-我的帐号模块进入，登录成功
    def myaccout_login(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect='登录成功',*args):
        '''
        用户进行登录
        '''
        #self.phone_num
        self.myAccount()
        return self.login(phone_num,passwd,expect)

    #登陆失败的模块,手机号长度不满11位
    def myaccout_login_error1(self,phone_num=testdata.phone_num_e1,passwd=testdata.passwd,expect='手机号不满11位',*args):
        '''
        登陆失败的模块,手机号长度不满11位
        '''
        self.myAccount()
        return self.login(phone_num,passwd,expect)

    #手机号未注册
    def myaccout_login_error2(self,phone_num=testdata.phone_num_e2,passwd=testdata.passwd,expect='进入注册模块',*args):
        '''
        登陆失败的模块,手机号未注册
        '''
        self.myAccount()
        return self.login(phone_num,passwd,expect)

    #手机号和密码不匹配
    def myaccout_login_error3(self,phone_num=testdata.phone_num,passwd=testdata.passwd_e1,expect='手机号和密码不匹配',*args):
        '''
        登陆失败的模块,手机号和密码不匹配
        '''
        self.myAccount()
        return self.login(phone_num,passwd,expect)

    #手机号为已注册号码，密码不满6位
    def myaccout_login_error4(self,phone_num=testdata.phone_num,passwd=testdata.passwd_e2,expect='密码不满6位或为空',*args):
        '''
        登陆失败的模块,手机号为已注册号码，密码不满6位
        '''
        self.myAccount()
        return self.login(phone_num,passwd,expect)

    #通过更多-我的帐号模块进入，注册
    def myaccout_sign(self,phone_num=testdata.sign_num,sign_pwd=testdata.sign_pwd,expect=True):
        '''
        通过更多-我的帐号模块进入，注册
        '''
        self.myAccount()
        return self.sign(phone_num,sign_pwd,expect)

    #5.1以上版本通过更多-我的帐号模块进入，注册
    def myaccout_sign51(self,phone_num=testdata.sign_num,sign_pwd=testdata.sign_pwd,expect=True):
        '''
        通过更多-我的帐号模块进入，注册
        '''
        self.click_more()
        self.click_login51()
        return self.sign(phone_num,sign_pwd,expect)

    #5.1通过更多-我的帐号模块进入，登录成功
    def myaccout_login51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect='登录成功',*args):
        '''
        用户进行登录
        '''
        #self.phone_num
        self.click_more()
        self.click_login51()
        return self.login(phone_num,passwd,expect)

    #5.1登陆失败的模块,手机号长度不满11位
    def myaccout_login51_error1(self,phone_num=testdata.phone_num_e1,passwd=testdata.passwd,expect='手机号不满11位',*args):
        '''
        登陆失败的模块,手机号长度不满11位
        '''
        self.click_more()
        self.click_login51()
        return self.login(phone_num,passwd,expect)

    #5.1手机号未注册
    def myaccout_login51_error2(self,phone_num=testdata.phone_num_e2,passwd=testdata.passwd,expect='进入注册模块',*args):
        '''
        登陆失败的模块,手机号未注册
        '''
        self.click_more()
        self.click_login51()
        return self.login(phone_num,passwd,expect)

    #5.1手机号和密码不匹配
    def myaccout_login51_error3(self,phone_num=testdata.phone_num,passwd=testdata.passwd_e1,expect='手机号和密码不匹配',*args):
        '''
        登陆失败的模块,手机号和密码不匹配
        '''
        self.click_more()
        self.click_login51()
        return self.login(phone_num,passwd,expect)

    #5.1手机号为已注册号码，密码不满6位
    def myaccout_login51_error4(self,phone_num=testdata.phone_num,passwd=testdata.passwd_e2,expect='密码不满6位或为空',*args):
        '''
        登陆失败的模块,手机号为已注册号码，密码不满6位
        '''
        self.click_more()
        self.click_login51()
        return self.login(phone_num,passwd,expect)

    #5.1通过更多-我的帐号模块进入，注册
    def myaccout_sign51(self,phone_num=testdata.sign_num,sign_pwd=testdata.sign_pwd,expect=True):
        '''
        通过更多-我的帐号模块进入，注册
        '''
        self.click_more()
        self.click_login51()
        return self.sign(phone_num,sign_pwd,expect)

    #修改登陆密码成功
    def modify_loginpwd_after_login(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_pwd=testdata.old_pwd,set_pwd=testdata.set_pwd,repeat_pwd=testdata.repeat_pwd,expect='修改登录密码成功'):
        '''
        修改登陆密码成功
        '''
        self.myAccount()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_login_pwd(old_pwd,set_pwd,repeat_pwd,expect)
        else:
            self.login(phone_num,passwd)
            self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_login_pwd(old_pwd,set_pwd,repeat_pwd,expect)

    #修改登陆密码失败，原密码错误
    def modify_loginpwd_after_login_error1(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_pwd=testdata.old_pwd_e1,set_pwd=testdata.set_pwd,repeat_pwd=testdata.repeat_pwd,expect='修改登录密码失败'):
        '''
        修改登陆密码失败，原密码错误
        '''
        self.myAccount()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_login_pwd(old_pwd,set_pwd,repeat_pwd,expect)
        else:
            self.login(phone_num,passwd)
            self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_login_pwd(old_pwd,set_pwd,repeat_pwd,expect)

    #原密码正确，新置密码与重复新置密码不一致
    def modify_loginpwd_after_login_error2(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_pwd=testdata.old_pwd,set_pwd=testdata.set_pwd,repeat_pwd=testdata.repeat_pwd_e1,expect='修改登录密码失败'):
        '''
        修改以密码原密码正确，新置密码与重复新置密码不一致
        '''
        self.myAccount()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_login_pwd(old_pwd,set_pwd,repeat_pwd,expect)
        else:
            self.login(phone_num,passwd)
            self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_login_pwd(old_pwd,set_pwd,repeat_pwd,expect)

    #登陆后修改交易密码成功
    def modify_trade_pwd_after_login(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_trade_pwd=testdata.old_trade_pwd,new_trade_pwd=testdata.new_trade_pwd,repeat_trade_pwd=testdata.repeat_trade_pwd,expect='修改交易密码成功'):
        '''
        登陆后修改交易密码成功
        '''
        self.myAccount()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)
        else:
            self.login(phone_num,passwd)
            self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)


    #原交易密码与手机号不匹配
    def modify_trade_pwd_after_login_error1(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_trade_pwd=testdata.old_trade_pwd_e1,new_trade_pwd=testdata.new_trade_pwd,repeat_trade_pwd=testdata.repeat_trade_pwd,expect='原交易密码错误'):
        '''
        原交易密码与手机号不匹配
        '''
        self.myAccount()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)
        else:
            self.login(phone_num,passwd)
            self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

    #原交易密码位数不够
    def modify_trade_pwd_after_login_error2(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_trade_pwd=testdata.old_trade_pwd_e2,new_trade_pwd=testdata.new_trade_pwd,repeat_trade_pwd=testdata.repeat_trade_pwd,expect='原交易密码输入位数不够'):
        '''
        原交易密码位数不够
        '''
        self.myAccount()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)
        else:
            self.login(phone_num,passwd)
            self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

    #原交易密码正确，新交易密码位数不够
    def modify_trade_pwd_after_login_error3(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_trade_pwd=testdata.old_trade_pwd,new_trade_pwd=testdata.new_trade_pwd_e1,repeat_trade_pwd=testdata.repeat_trade_pwd,expect='新交易密码输入位数不够'):
        '''
        原交易密码正确，新交易密码位数不够
        '''
        self.myAccount()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)
        else:
            self.login(phone_num,passwd)
            self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

    #原交易密码正确，新交易密码位数正确。重复新交易密码位数不够
    def modify_trade_pwd_after_login_error4(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_trade_pwd=testdata.old_trade_pwd,new_trade_pwd=testdata.new_trade_pwd,repeat_trade_pwd=testdata.repeat_trade_pwd_e1,expect='重复交易密码不够位数'):
        '''
        原交易密码正确，新交易密码位数正确。重复新交易密码位数不够
        '''
        self.myAccount()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)
        else:
            self.login(phone_num,passwd)
            self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

    #原交易密码正确，新交易密码位数正确。重复新交易密码与新交易密码不匹配
    def modify_trade_pwd_after_login_error5(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_trade_pwd=testdata.old_trade_pwd,new_trade_pwd=testdata.new_trade_pwd,repeat_trade_pwd=testdata.repeat_trade_pwd_e2,expect='两次密码输入不一致'):
        '''
        原交易密码正确，新交易密码位数正确。重复新交易密码与新交易密码不匹配
        '''
        self.myAccount()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)
        else:
            self.login(phone_num,passwd)
            self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

     #5.1修改登陆密码成功
    def modify_loginpwd_after_login51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_pwd=testdata.old_pwd,set_pwd=testdata.set_pwd,repeat_pwd=testdata.repeat_pwd,expect='修改登录密码成功'):
        '''
        修改登陆密码成功
        '''
        self.click_more()
        self.setting51()
        self.rl_pwd_manager()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            # print 1
            # self.rl_pwd_manager()
            return self.modify_login_pwd(old_pwd,set_pwd,repeat_pwd,expect)
        else:
            self.login(phone_num,passwd)
            #self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_login_pwd(old_pwd,set_pwd,repeat_pwd,expect)

    #5.1修改登陆密码失败，原密码错误
    def modify_loginpwd_after_login51_error1(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_pwd=testdata.old_pwd_e1,set_pwd=testdata.set_pwd,repeat_pwd=testdata.repeat_pwd,expect='修改登录密码失败'):
        '''
        修改登陆密码失败，原密码错误
        '''
        self.click_more()
        self.setting51()
        self.rl_pwd_manager()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            #self.rl_pwd_manager()
            return self.modify_login_pwd(old_pwd,set_pwd,repeat_pwd,expect)
        else:
            self.login(phone_num,passwd)
            #self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_login_pwd(old_pwd,set_pwd,repeat_pwd,expect)

    #5.1原密码正确，新置密码与重复新置密码不一致
    def modify_loginpwd_after_login51_error2(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_pwd=testdata.old_pwd,set_pwd=testdata.set_pwd,repeat_pwd=testdata.repeat_pwd_e1,expect='修改登录密码失败'):
        '''
        修改以密码原密码正确，新置密码与重复新置密码不一致
        '''
        self.click_more()
        self.setting51()
        self.rl_pwd_manager()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            #self.rl_pwd_manager()
            return self.modify_login_pwd(old_pwd,set_pwd,repeat_pwd,expect)
        else:
            self.login(phone_num,passwd)
            #self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_login_pwd(old_pwd,set_pwd,repeat_pwd,expect)

    #5.1登陆后修改交易密码成功
    def modify_trade_pwd_after_login51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_trade_pwd=testdata.old_trade_pwd,new_trade_pwd=testdata.new_trade_pwd,repeat_trade_pwd=testdata.repeat_trade_pwd,expect='修改交易密码成功'):
        '''
        登陆后修改交易密码成功
        '''
        self.click_more()
        self.setting51()
        self.rl_pwd_manager()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            # self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)
        else:
            self.login(phone_num,passwd)
            #self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

    #5.1原交易密码与手机号不匹配
    def modify_trade_pwd_after_login51_error1(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_trade_pwd=testdata.old_trade_pwd_e1,new_trade_pwd=testdata.new_trade_pwd,repeat_trade_pwd=testdata.repeat_trade_pwd,expect='原交易密码错误'):
        '''
        原交易密码与手机号不匹配
        '''
        self.click_more()
        self.setting51()
        self.rl_pwd_manager()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            # self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)
        else:
            self.login(phone_num,passwd)
            # self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

    #5.1原交易密码位数不够
    def modify_trade_pwd_after_login51_error2(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_trade_pwd=testdata.old_trade_pwd_e2,new_trade_pwd=testdata.new_trade_pwd,repeat_trade_pwd=testdata.repeat_trade_pwd,expect='原交易密码输入位数不够'):
        '''
        原交易密码位数不够
        '''
        self.click_more()
        self.setting51()
        self.rl_pwd_manager()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            # self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)
        else:
            self.login(phone_num,passwd)
            # self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

    #5.1原交易密码正确，新交易密码位数不够
    def modify_trade_pwd_after_login51_error3(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_trade_pwd=testdata.old_trade_pwd,new_trade_pwd=testdata.new_trade_pwd_e1,repeat_trade_pwd=testdata.repeat_trade_pwd,expect='新交易密码输入位数不够'):
        '''
        原交易密码正确，新交易密码位数不够
        '''
        self.click_more()
        self.setting51()
        self.rl_pwd_manager()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            # self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)
        else:
            self.login(phone_num,passwd)
            # self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

    #5.1原交易密码正确，新交易密码位数正确。重复新交易密码位数不够
    def modify_trade_pwd_after_login51_error4(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_trade_pwd=testdata.old_trade_pwd,new_trade_pwd=testdata.new_trade_pwd,repeat_trade_pwd=testdata.repeat_trade_pwd_e1,expect='重复交易密码不够位数'):
        '''
        原交易密码正确，新交易密码位数正确。重复新交易密码位数不够
        '''
        self.click_more()
        self.setting51()
        self.rl_pwd_manager()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            #self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)
        else:
            self.login(phone_num,passwd)
            # self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

    #5.1原交易密码正确，新交易密码位数正确。重复新交易密码与新交易密码不匹配
    def modify_trade_pwd_after_login51_error5(self,phone_num=testdata.phone_num,passwd=testdata.passwd,old_trade_pwd=testdata.old_trade_pwd,new_trade_pwd=testdata.new_trade_pwd,repeat_trade_pwd=testdata.repeat_trade_pwd_e2,expect='两次密码输入不一致'):
        '''
        原交易密码正确，新交易密码位数正确。重复新交易密码与新交易密码不匹配
        '''
        self.click_more()
        self.setting51()
        self.rl_pwd_manager()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            # self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)
        else:
            self.login(phone_num,passwd)
            # self.click_myaccount()
            self.rl_pwd_manager()
            return self.modify_trade_pwd(old_trade_pwd,new_trade_pwd,repeat_trade_pwd,expect)

    #登陆后找回交易密码
    def back_trade_pwd_after_login(self,phone_num='13735865796',passwd='654321',username=u'吴越欣',card='330522199009256911',new_trade_pwd='654321',repeat_trade_pwd='654321',expect=True):
        self.myaccout_login(phone_num,passwd)
        self.click_myaccount()
        self.rl_pwd_manager()
        return self.back_trade_pwd(username,card,new_trade_pwd,repeat_trade_pwd,expect)

    #4.2版本余额充值成功
    def balance_into4(self,phone_num=testdata.phone_num,passwd=testdata.passwd,topup_num=testdata.topup_num,trade_pwd=testdata.trade_pwd,expect='余额成功充值'):
        '''
        4.2版本余额充值成功
        '''
        self.myAccount()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            self.enter_balance()
            self.click_recharge()
            return self.top_up(topup_num,trade_pwd,expect)
        else:
            self.login(phone_num,passwd,expect)
            self.click_myaccount()
            self.enter_balance()
            self.click_recharge()
            return self.top_up(topup_num,trade_pwd,expect)

    #充值金额为空
    def balance_into4_error1(self,phone_num=testdata.phone_num,passwd=testdata.passwd,topup_num=testdata.topup_num_e1,trade_pwd=testdata.trade_pwd,expect='充值金额错误'):
        '''
        4.2版本余额，充值金额为空
        '''
        self.myAccount()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            self.enter_balance()
            self.click_recharge()
            return self.top_up(topup_num,trade_pwd,expect)
        else:
            self.login(phone_num,passwd)
            self.click_myaccount()
            self.enter_balance()
            self.click_recharge()
            return self.top_up(topup_num,trade_pwd,expect)

    #交易密码错误
    def balance_into4_error2(self,phone_num=testdata.phone_num,passwd=testdata.passwd,topup_num=testdata.topup_num,trade_pwd=testdata.trade_pwd_e,expect='交易密码错误'):
        '''
        4.2版本余额，交易密码错误
        '''
        self.myAccount()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            self.enter_balance()
            self.click_recharge()
            return self.top_up(topup_num,trade_pwd,expect)
        else:
            self.login(phone_num,passwd)
            self.click_myaccount()
            self.enter_balance()
            self.click_recharge()
            return self.top_up(topup_num,trade_pwd,expect)

    #4.2版本余额提现
    def balance_out4(self,phone_num=testdata.phone_num,passwd=testdata.passwd,out_num=testdata.out_num,trade_pwd=testdata.trade_pwd,expect='余额成功提现'):
        '''
        4.2版本余额提现，成功
        '''
        self.myAccount()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            self.enter_balance()
            self.click_balance_out()
            return self.cash(out_num,trade_pwd,expect)
        else:
            self.login(phone_num,passwd,expect)
            self.click_myaccount()
            self.enter_balance()
            self.click_balance_out()
            return self.cash(out_num,trade_pwd,expect)

    #4.2版本余额提现，转出金额为空
    def balance_out4_error1(self,phone_num=testdata.phone_num,passwd=testdata.passwd,out_num=testdata.out_num_e1,trade_pwd=testdata.trade_pwd,expect='提现金额错误'):
        '''
        4.2版本余额提现，转出金额为空
        '''
        self.myAccount()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            self.enter_balance()
            self.click_balance_out()
            return self.cash(out_num,trade_pwd,expect)
        else:
            self.login(phone_num,passwd,expect)
            self.click_myaccount()
            self.enter_balance()
            self.click_balance_out()
            return self.cash(out_num,trade_pwd,expect)

    #4.2版本余额提现，交易密码与手机号不匹配
    def balance_out4_error2(self,phone_num=testdata.phone_num,passwd=testdata.passwd,out_num=testdata.out_num,trade_pwd=testdata.trade_pwd_e,expect='交易密码错误'):
        '''
        4.2版本余额提现，交易密码与手机号不匹配
        '''
        self.myAccount()
        sleep(3)
        if self.isElement("id", tbjpy.input_phone)==False:
            #self.click_myaccount()
            self.enter_balance()
            self.click_balance_out()
            return self.cash(out_num,trade_pwd,expect)
        else:
            self.login(phone_num,passwd,expect)
            self.click_myaccount()
            self.enter_balance()
            self.click_balance_out()
            return self.cash(out_num,trade_pwd,expect)

    # #4.2版本余额提现，交易密码位数不够
    # def balance_out4_error3(self,phone_num='13735865796',passwd='654321',out_num='100',trade_pwd='12345',expect=False):
    #     '''
    #     4.2版本余额提现，交易密码位数不够
    #     '''
    #     self.myaccout_login(phone_num,passwd)
    #     self.enter_balance()
    #     self.click_balance_out()
    #     return self.cash(out_num,trade_pwd,expect)

    #4.2以上版本余额提现
    def balance_out5(self,phone_num=testdata.phone_num,passwd=testdata.passwd,out_num=testdata.out_num,trade_pwd=testdata.trade_pwd,expect='余额成功提现'):
        '''
        4.2以上版本余额提现，成功
        '''
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            self.enter_balance5()
            self.click_balance_out()
            return self.cash43(out_num,trade_pwd,expect)
        else:
            self.enter_balance5()
            self.click_balance_out()
            return self.cash43(out_num,trade_pwd,expect)

    #转入金额错误
    def balance_out5_error1(self,phone_num=testdata.phone_num,passwd=testdata.passwd,out_num=testdata.out_num_e1,trade_pwd=testdata.trade_pwd,expect='提现金额错误'):
        '''
        4.2版本余额提现，转入金额为空
        '''
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            self.enter_balance5()
            self.click_balance_out()
            return self.cash43(out_num,trade_pwd,expect)
        else:
            self.enter_balance5()
            self.click_balance_out()
            return self.cash43(out_num,trade_pwd,expect)

    #交易密码错误
    def balance_out5_error2(self,phone_num=testdata.phone_num,passwd=testdata.passwd,out_num=testdata.out_num,trade_pwd=testdata.trade_pwd_e,expect='余额提现失败'):
        '''
        4.2版本余额提现，交易密码错误
        '''
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            self.enter_balance5()
            self.click_balance_out()
            return self.cash43(out_num,trade_pwd,expect)
        else:
            self.enter_balance5()
            self.click_balance_out()
            return self.cash43(out_num,trade_pwd,expect)

    #4.2以上版本余额充值
    def balance_in5(self,phone_num=testdata.phone_num,passwd=testdata.passwd,topup_num=testdata.topup_num,trade_pwd=testdata.trade_pwd,expect='余额成功充值'):
        '''
        4.2以上版本余额充值，成功
        '''
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            self.enter_balance5()
            self.click_recharge()
            return self.top_up43(topup_num,trade_pwd,expect)
        else:
            self.enter_balance5()
            self.click_recharge()
            return self.top_up43(topup_num,trade_pwd,expect)

    #转入金额错误
    def balance_in5_error1(self,phone_num=testdata.phone_num,passwd=testdata.passwd,topup_num=testdata.topup_num_e1,trade_pwd=testdata.trade_pwd,expect='充值金额错误'):
        '''
        4.2版本余额提现，转入金额为空
        '''
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            self.enter_balance5()
            self.click_recharge()
            return self.top_up43(topup_num,trade_pwd,expect)
        else:
            self.enter_balance5()
            self.click_recharge()
            return self.top_up43(topup_num,trade_pwd,expect)

    #交易密码错误
    def balance_in5_error2(self,phone_num=testdata.phone_num,passwd=testdata.passwd,topup_num=testdata.topup_num,trade_pwd=testdata.trade_pwd_e,expect='交易密码错误'):
        '''
        4.2版本余额提现，交易密码错误
        '''
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            self.enter_balance5()
            self.click_recharge()
            return self.top_up43(topup_num,trade_pwd,expect)
        else:
            self.enter_balance5()
            self.click_recharge()
            return self.top_up43(topup_num,trade_pwd,expect)

    # #交易密码位数不够
    # def balance_out5_error3(self,phone_num='13735865796',passwd='654321',out_num='100',trade_pwd='12345',expect=False):
    #     self.myaccout_login(phone_num,passwd)
    #     self.enter_balance5()
    #     self.click_balance_out()
    #     return self.cash(out_num,trade_pwd,expect)

    #5.1以上版本余额提现
    def balance_out51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,out_num=testdata.out_num,trade_pwd=testdata.trade_pwd,expect='余额成功提现'):
        '''
        5.1以上版本余额提现，成功
        '''
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.click_more()
            self.click_login51()
            self.login(phone_num,passwd)
            # self.back()
            self.myproperty()
            self.enter_balance5()
            self.click_balance_out()
            return self.cash43(out_num,trade_pwd,expect)
        else:
            self.enter_balance5()
            self.click_balance_out()
            return self.cash43(out_num,trade_pwd,expect)

    #转入金额错误
    def balance_out51_error1(self,phone_num=testdata.phone_num,passwd=testdata.passwd,out_num=testdata.out_num_e1,trade_pwd=testdata.trade_pwd,expect='提现金额错误'):
        '''
        5.1版本余额提现，转入金额为空
        '''
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.click_more()
            self.click_login51()
            self.login(phone_num,passwd)
            self.myproperty()
            self.enter_balance5()
            self.click_balance_out()
            return self.cash43(out_num,trade_pwd,expect)
        else:
            self.enter_balance5()
            self.click_balance_out()
            return self.cash43(out_num,trade_pwd,expect)

    #交易密码错误
    def balance_out51_error2(self,phone_num=testdata.phone_num,passwd=testdata.passwd,out_num=testdata.out_num,trade_pwd=testdata.trade_pwd_e,expect='交易密码错误'):
        '''
        5.1版本余额提现，交易密码错误
        '''
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.click_more()
            self.click_login51()
            self.login(phone_num,passwd)
            self.myproperty()
            self.enter_balance5()
            self.click_balance_out()
            return self.cash43(out_num,trade_pwd,expect)
        else:
            self.enter_balance5()
            self.click_balance_out()
            return self.cash43(out_num,trade_pwd,expect)

    #4.2以上版本余额充值
    def balance_in51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,topup_num=testdata.topup_num,trade_pwd=testdata.trade_pwd,expect='余额成功充值'):
        '''
        5.1以上版本余额充值，成功
        '''
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.click_more()
            self.click_login51()
            self.login(phone_num,passwd)
            # self.back()
            self.myproperty()
            self.enter_balance5()
            self.click_recharge()
            return self.top_up43(topup_num,trade_pwd,expect)
        else:
            self.enter_balance5()
            self.click_recharge()
            return self.top_up43(topup_num,trade_pwd,expect)

    #转入金额错误
    def balance_in51_error1(self,phone_num=testdata.phone_num,passwd=testdata.passwd,topup_num=testdata.topup_num_e1,trade_pwd=testdata.trade_pwd,expect='充值金额错误'):
        '''
        5.1版本余额提现，转入金额为空
        '''
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.click_more()
            self.click_login51()
            self.login(phone_num,passwd)
            # self.back()
            self.myproperty()
            self.enter_balance5()
            self.click_recharge()
            return self.top_up43(topup_num,trade_pwd,expect)
        else:
            self.enter_balance5()
            self.click_recharge()
            return self.top_up43(topup_num,trade_pwd,expect)

    #交易密码错误
    def balance_in51_error2(self,phone_num=testdata.phone_num,passwd=testdata.passwd,topup_num=testdata.topup_num,trade_pwd=testdata.trade_pwd_e,expect='交易密码错误'):
        '''
        5.1版本余额提现，交易密码错误
        '''
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.click_more()
            self.click_login51()
            self.login(phone_num,passwd)
            # self.back()
            self.myproperty()
            self.enter_balance5()
            self.click_recharge()
            return self.top_up43(topup_num,trade_pwd,expect)
        else:
            self.enter_balance5()
            self.click_recharge()
            return self.top_up43(topup_num,trade_pwd,expect)

    #4.2更多模块-查看
    def more_check42(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        try:
            code=11
            self.click_more()
            #查看我的账户并截图
            self.click_button((By.ID, tbjpy.loginbtn))
            if self.isElement("id", tbjpy.input_phone)==True:
                self.input_login_phone(phone_num)
                self.click_next()
                self.input_login_passwd(passwd)
                self.click_login_button()
                self.click_button((By.ID, tbjpy.loginbtn))
            self.driver.implicitly_wait(5)
            self.screenshot()
            self.back()
            #查看邀请好友并截图
            self.click_button((By.ID, tbjpy.invite))
            sleep(5)
            self.screenshot()
            self.back()
           # 查看产品预告并截图
            self.click_button((By.ID, tbjpy.pre_sell))
            sleep(4)
            self.screenshot()
            self.click_button((By.XPATH, tbjpy.back2))
            #查看关于铜板街并截图
            print 1
            self.click_button((By.ID, tbjpy.about_tbj42))
            self.driver.implicitly_wait(5)
            self.screenshot()
            self.back()
            actual=True
            e='成功'
        except Exception,e:
            actual=False
            e='失败'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #4.3更多模块-查看
    def more_check43(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        try:
            code=11
            self.click_more()
            #查看我的账户并截图
            self.click_button((By.ID, tbjpy.loginbtn))
            if self.isElement("id", tbjpy.input_phone)==True:
                self.input_login_phone(phone_num)
                self.click_next()
                self.input_login_passwd(passwd)
                self.click_login_button()
                self.click_button((By.ID, tbjpy.loginbtn))
            sleep(4)
            self.screenshot()
            self.back()
            #查看邀请好友并截图
            self.click_button((By.ID, tbjpy.invite))
            sleep(5)
            self.screenshot()
            self.back()
           # 查看产品预告并截图
            self.click_button((By.ID, tbjpy.pre_sell))
            sleep(4)
            self.screenshot()
            self.click_button((By.XPATH, tbjpy.back2))
            #查看关于铜板街并截图
            self.click_button((By.ID, tbjpy.about_tbj42))
            self.driver.implicitly_wait(5)
            self.screenshot()
            self.back()
            actual=True
            e='成功'
        except Exception,e:
            actual=False
            e='失败'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #5.0更多模块-查看
    def more_check5(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        try:
            code=11
            self.click_more()
            #查看我的账户并截图
            self.click_button((By.ID, tbjpy.loginbtn))
            if self.isElement("id", tbjpy.input_phone)==True:
                self.input_login_phone(phone_num)
                self.click_next()
                self.input_login_passwd(passwd)
                self.click_login_button()
                self.click_button((By.ID, tbjpy.loginbtn))
            sleep(4)
            self.screenshot()
            self.back()
            #查看邀请好友并截图
            # print 111
            self.click_button((By.ID, tbjpy.invite))
            sleep(5)
            self.screenshot()
            self.back()
            actual=True
            e='成功'
        except Exception,e:
            actual=False
            e='失败'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #5.1更多模块-查看
    def more_check51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        try:
            code=11
            self.click_more()
            self.click_login51()
            #查看我的账户并截图
            # self.click_button((By.ID,tbjpy.loginbtn))
            if self.isElement("id", tbjpy.input_phone)==True:
                self.input_login_phone(phone_num)
                self.click_next()
                self.input_login_passwd(passwd)
                self.click_login_button()
                self.click_login51()
            sleep(4)
            self.screenshot()
            self.back()
            #查看邀请好友并截图
            print 111
            self.click_button((By.ID, tbjpy.invite))
            sleep(5)
            self.screenshot()
            self.back()
            self.click_button((By.ID, tbjpy.risk))
            sleep(5)
            self.screenshot()
            self.back()
            self.click_button((By.ID, tbjpy.customer_service))
            sleep(5)
            self.screenshot()
            self.back()
            self.click_button((By.ID, tbjpy.settings))
            sleep(5)
            self.screenshot()
            self.back()
            self.click_button((By.ID, tbjpy.about_tbj))
            sleep(5)
            self.screenshot()
            self.click_button((By.XPATH, tbjpy.back2))
            print 444
            actual=True
            e='成功'
        except Exception,e:
            actual=False
            e='失败'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #5.2更多模块-查看
    def more_check52(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        try:
            code=11
            self.click_more()
            self.click_login51()
            #查看我的账户并截图
            # self.click_button((By.ID,tbjpy.loginbtn))
            if self.isElement("id", tbjpy.input_phone)==True:
                self.input_login_phone(phone_num)
                self.click_next()
                self.input_login_passwd(passwd)
                self.click_login_button()
                self.click_login51()
            sleep(4)
            self.screenshot()
            self.back()
            #查看邀请好友并截图
            print 111
            self.click_button((By.ID, tbjpy.invite))
            sleep(5)
            self.screenshot()
            self.back()
            self.click_button((By.ID, tbjpy.risk))
            sleep(5)
            self.screenshot()
            self.back()
            self.click_button((By.ID, tbjpy.customer_service))
            sleep(5)
            self.screenshot()
            self.back()
            self.click_button((By.ID, tbjpy.settings))
            sleep(5)
            self.screenshot()
            self.back()
            self.click_button((By.ID, tbjpy.about_tbj))
            sleep(5)
            self.screenshot()
            self.click_button((By.XPATH, tbjpy.back2))
            print 444
            actual=True
            e='成功'
        except Exception,e:
            actual=False
            e='失败'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #精品推荐购买
    def buy_hot_product(self,phone_num=testdata.phone_num,passwd=testdata.passwd,trade_num=testdata.trade_pwd,expect1=True,amount2=testdata.tongbaoin_num,expect2=True,amount3=testdata.normal_product_num,expect3=True):
        # self.myaccout_login()
        # print 111
        self.hot_product()
        # print 222
        get_hot_product_name=self.driver.find_element_by_id(tbjpy.hot_product_name42).get_attribute("text")
        # print get_hot_product_name
        #get_hot_product_period=self.driver.find_element_by_id(tbjpy.hot_product_period).get_attribute("text")
        #print get_hot_product_period
        self.ll_top_content()
        self.screenshot()
        sleep(3)
        if self.isElement("id", tbjpy.login_page_check)==True:
            #print 1
            self.login(phone_num,passwd)
            #print 2121
            get_hot_product_name=self.driver.find_element_by_id(tbjpy.hot_product_name42).get_attribute("text")
            #print get_hot_product_name
            self.ll_top_content()
            if re.findall(u"新手",get_hot_product_name)!=[]:
                # print 1
                self.screenshot()
                return self.new_people_product(trade_num,expect1)
            #铜宝转入
            elif re.findall(u"铜宝",get_hot_product_name)!=[]:
                # print 2
                self.screenshot()
                return self.tongbaoin(amount2,trade_num,expect2)
            else:
                # print 3
                self.screenshot()
                return self.normal_product(amount3,trade_num,expect3)
        else:
            if re.findall(u"新手",get_hot_product_name)!=[]:
                # print 4
                self.screenshot()
                return self.new_people_product(trade_num,expect1)
            #铜宝转入
            elif re.findall(u"铜宝",get_hot_product_name)!=[]:
                # print 5
                self.screenshot()
                return self.tongbaoin(amount2,trade_num,expect2)
            else:
                # print 6
                self.screenshot()
                return self.normal_product(amount3,trade_num,expect3)

    #理财产品购买4.2版本
    def buy_financing_products(self,phone_num='13735865796',passwd='654321',amount='600',normal_trade_num='654321',expect=True):
        self.tab_financing_products()
        self.click_frist_financing_product()
        self.click_product_purchase_view()
        if self.isElement("xpath", tbjpy.buy_check_login_page_no)==True:
            return self.normal_product(amount,normal_trade_num,expect)
        else:
            self.login(phone_num,passwd)
            self.click_product_purchase_view()
            self.screenshot()
            return self.normal_product(amount,normal_trade_num,expect)

    def buy_financing_products_error1(self,phone_num='13735865796',passwd='654321',amount='',normal_trade_num='654321',expect=True):
        self.tab_financing_products()
        self.click_frist_financing_product()
        self.click_product_purchase_view()
        if self.isElement("xpath", tbjpy.buy_check_login_page_no)==True:
            return self.normal_product(amount,normal_trade_num,expect)
        else:
            self.login(phone_num,passwd)
            self.click_product_purchase_view()
            return self.normal_product(amount,normal_trade_num,expect)

    def buy_financing_products_error2(self,phone_num='13735865796',passwd='654321',amount='600',normal_trade_num='123456',expect=True):
        self.tab_financing_products()
        self.click_frist_financing_product()
        self.click_product_purchase_view()
        if self.isElement("xpath", tbjpy.buy_check_login_page_no)==True:
            return self.normal_product(amount,normal_trade_num,expect)
        else:
            self.login(phone_num,passwd)
            self.click_product_purchase_view()
            return self.normal_product(amount,normal_trade_num,expect)

    #4.2我的资产铜宝转入
    def myproperty_tongbao_in42(self,phone_num=testdata.phone_num,passwd=testdata.passwd,amount=testdata.tongbaoin_num,trade_num=testdata.trade_pwd,expect='铜宝转入成功'):
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            self.myassert_tongbao42()
            if self.isElement("id", tbjpy.tongbao_in)==True:
                #print "成功进入铜宝页面"
                return self.tongbaoin(amount,trade_num,expect)
            else:
                pass
        else:
            self.myassert_tongbao42()
            if self.isElement("id", tbjpy.tongbao_in)==True:
                #print "成功进入铜宝页面"
                return self.tongbaoin(amount,trade_num,expect)
            else:
                pass

    #4.2我的资产铜宝转出
    def myproperty_tongbao_out42(self,phone_num=testdata.phone_num,passwd=testdata.passwd,amount=testdata.tongbaoout_num,trade_num=testdata.trade_pwd,expect='铜宝转出成功'):
        #self.myaccout_login()
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            self.myassert_tongbao42()
            if self.isElement("id", tbjpy.tongbao_in)==True:
                print 333
                #print "成功进入铜宝页面"
                return self.tongbaoout(amount,trade_num,expect)
            else:
                pass
        else:
            self.myassert_tongbao42()
            if self.isElement("id", tbjpy.tongbao_in)==True:
                #print "成功进入铜宝页面"
                return self.tongbaoout(amount,trade_num,expect)
            else:
                pass

    #4.3我的资产铜宝转入
    def myproperty_tongbao_in43(self,phone_num=testdata.phone_num,passwd=testdata.passwd,amount=testdata.tongbaoin_num,trade_num=testdata.trade_pwd,expect='铜宝转入成功'):
        #self.myaccout_login()
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            self.myassert_tongbao43()
            if self.isElement("id", tbjpy.tongbao_in)==True:
                #print "成功进入铜宝页面"
                return self.tongbaoin(amount,trade_num,expect)
            else:
                pass
        else:
            self.myassert_tongbao43()
            if self.isElement("id", tbjpy.tongbao_in)==True:
                #print "成功进入铜宝页面"
                return self.tongbaoin(amount,trade_num,expect)
            else:
                pass

    #4。3我的资产铜宝转出
    def myproperty_tongbao_out43(self,phone_num=testdata.phone_num,passwd=testdata.passwd,amount=testdata.tongbaoin_num,trade_num=testdata.trade_pwd,expect='铜宝转出成功'):
        #self.myaccout_login()
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            self.myassert_tongbao43()
            if self.isElement("id", tbjpy.tongbao_in)==True:
                #print "成功进入铜宝页面"
                return self.tongbaoout(amount,trade_num,expect)
            else:
                pass
        else:
            self.myassert_tongbao43()
            if self.isElement("id", tbjpy.tongbao_in)==True:
                #print "成功进入铜宝页面"
                return self.tongbaoout(amount,trade_num,expect)
            else:
                pass

    #5.1我的资产铜宝转入
    def myproperty_tongbao_in51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,amount=testdata.tongbaoin_num,trade_num=testdata.trade_pwd,expect='铜宝转入成功'):
        #self.myaccout_login()
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.click_more()
            self.click_login51()
            self.login(phone_num,passwd)
            self.myproperty()
            self.myassert_tongbao43()
            if self.isElement("id", tbjpy.tongbao_in)==True:
                #print "成功进入铜宝页面"
                return self.tongbaoin(amount,trade_num,expect)
            else:
                pass
        else:
            self.myassert_tongbao43()
            if self.isElement("id", tbjpy.tongbao_in)==True:
                #print "成功进入铜宝页面"
                return self.tongbaoin(amount,trade_num,expect)
            else:
                pass

    #5。1我的资产铜宝转出
    def myproperty_tongbao_out51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,amount=testdata.tongbaoin_num,trade_num=testdata.trade_pwd,expect='铜宝转出成功'):
        #self.myaccout_login()
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.click_more()
            self.click_login51()
            self.login(phone_num,passwd)
            self.myproperty()
            self.myassert_tongbao43()
            if self.isElement("id", tbjpy.tongbao_in)==True:
                #print "成功进入铜宝页面"
                return self.tongbaoout(amount,trade_num,expect)
            else:
                pass
        else:
            self.myassert_tongbao43()
            if self.isElement("id", tbjpy.tongbao_in)==True:
                #print "成功进入铜宝页面"
                return self.tongbaoout(amount,trade_num,expect)
            else:
                pass

    #5.0理财产品铜宝转入
    def buy_financing_products_tongbao_in(self,phone_num=testdata.phone_num,passwd=testdata.passwd,amount=testdata.tongbaoin_num,trade_num=testdata.trade_pwd,expect='铜宝转入成功'):
        #self.myaccout_login()
        self.financing_products_info()
        sleep(3)
        self.click_financing_products_tb()
        sleep(3)
        if self.isElement("id", tbjpy.buy_tongbao_check)==True:
            self.click_tongbao_login()
            self.login(phone_num,passwd)
            if self.isElement("id", tbjpy.tongbao_in)==True:
                #print "成功进入铜宝页面"
                return self.tongbaoin(amount,trade_num,expect)
            else:
                pass
        else:
            if self.isElement("id", tbjpy.tongbao_in)==True:
                #print "成功进入铜宝页面"
                return self.tongbaoin(amount,trade_num,expect)
            else:
                pass


    # 5.0理财产品铜宝转出
    def buy_financing_products_tongbao_out(self,phone_num=testdata.phone_num,passwd=testdata.passwd,amount=testdata.tongbaoout_num,trade_num=testdata.trade_pwd,expect='铜宝转出成功'):
        #self.myaccout_login()
        self.financing_products_info()
        sleep(3)
        self.click_financing_products_tb()
        sleep(3)
        if self.isElement("id", tbjpy.buy_tongbao_check)==True:
            self.click_tongbao_login()
            self.login(phone_num,passwd)
            if self.isElement("id", tbjpy.tongbao_out)==True:
                #print "成功进入铜宝页面"
                return self.tongbaoout(amount,trade_num,expect)
            else:
                pass
        else:
            if self.isElement("id", tbjpy.tongbao_out)==True:
                #print "成功进入铜宝页面"
                return self.tongbaoout(amount,trade_num,expect)
            else:
                pass


    #理财产品购买5.0版本
    def buy_financing_products5(self,phone_num='13735865796',passwd='654321',amount=300,trade_num='654321',expect=True,expect1=True,expect2=True):
        #self.myaccout_login()
        self.financing_products_info()
        sleep(4)
        second_financing_name=self.driver.find_element_by_xpath(tbjpy.second_financing_name).get_attribute("name")
        if  re.findall(u"转让专区",second_financing_name)!=[]:
            self.click_second_financing_name()
            self.click_second_financing_name_first()
            self.transfer_market_buy()
            #print 1
            if self.isElement("id", tbjpy.login_page_check)==True:
                #print 2
                self.login(phone_num,passwd)
                self.transfer_market_buy()
                #self.click_product_purchase_view()
                return self.buy_transfer(trade_num,expect)
            else:
                #print 3
                self.transfer_market_buy()
                #self.click_product_purchase_view()
                return self.buy_transfer(trade_num,expect)
        else:
            #print 4
            self.click_second_financing_name()
            self.click_second_financing_name_first()
            self.click_product_purchase_view()
            if self.isElement("id", tbjpy.login_page_check)==True:
                self.login(phone_num,passwd)
                self.click_product_purchase_view()
                sleep(5)
                if self.isElement("xpath", tbjpy.newpeople_buy_check)==True:
                    #print 5
                    amount_text=self.driver.find_element_by_xpath(tbjpy.newpeople_buy_check).get_attribute("name")
                    print amount_text
                    return self.new_people_product(trade_num,expect1)
                else:
                    #print 6
                    return self.normal_product(amount,trade_num,expect2)
            else:
                if self.isElement("xpath", tbjpy.newpeople_buy_check)==True:
                    return self.new_people_product(trade_num,expect1)
                else:
                    return self.normal_product(amount,trade_num,expect2)

    #交易密码与手机号不匹配
    def buy_financing_products5_error1(self,phone_num='13735865796',passwd='654321',amount='100',trade_num='654321',expect=True,expect1=True,expect2=True):
        self.financing_products_info()
        sleep(4)
        second_financing_name=self.driver.find_element_by_xpath(tbjpy.second_financing_name).get_attribute("name")
        if  re.findall(u"转让专区",second_financing_name)!=[]:
            self.click_second_financing_name()
            self.click_second_financing_name_first()
            self.transfer_market_buy()
            #print 1
            if self.isElement("id", tbjpy.login_page_check)==True:
                #print 2
                self.login(phone_num,passwd)
                self.transfer_market_buy()
                self.buy_transfer(trade_num,expect)
            else:
                #print 3
                self.transfer_market_buy()
                self.buy_transfer(trade_num,expect)
        else:
            #print 4
            self.click_second_financing_name()
            self.click_second_financing_name_first()
            self.click_product_purchase_view()
            if self.isElement("id", tbjpy.login_page_check)==True:
                self.login(phone_num,passwd)
                self.click_product_purchase_view()
                sleep(5)
                if self.isElement("xpath", tbjpy.newpeople_buy_check)==True:
                    # print 5,self.driver.find_element_by_xpath(tbjpy.second_financing_name).get_attribute("text")
                    #print 5
                    amount_text=self.driver.find_element_by_xpath(tbjpy.newpeople_buy_check).get_attribute("name")
                    print amount_text
                    self.new_people_product(trade_num,expect1)
                else:
                    #print 6
                    self.normal_product(amount,trade_num,expect2)
            else:
                if self.isElement("xpath", tbjpy.newpeople_buy_check)==True:
                    self.new_people_product(trade_num,expect1)
                else:
                    self.normal_product(amount,trade_num,expect2)

    def buy_financing_products5_error2(self,phone_num='13735865796',passwd='654321',amount='100',trade_num='65432',expect=True,expect1=True,expect2=True):
        self.financing_products_info()
        sleep(4)
        second_financing_name=self.driver.find_element_by_xpath(tbjpy.second_financing_name).get_attribute("name")
        if  re.findall(u"转让专区",second_financing_name)!=[]:
            self.click_second_financing_name()
            self.click_second_financing_name_first()
            self.transfer_market_buy()
            print 1
            if self.isElement("id", tbjpy.login_page_check)==True:
                print 2
                self.login(phone_num,passwd)
                self.transfer_market_buy()
                self.buy_transfer(trade_num,expect)
            else:
                print 3
                self.transfer_market_buy()
                self.buy_transfer(trade_num,expect)
        else:
            print 4
            self.click_second_financing_name()
            self.click_second_financing_name_first()
            self.click_product_purchase_view()
            if self.isElement("id", tbjpy.login_page_check)==True:
                self.login(phone_num,passwd)
                self.click_product_purchase_view()
                sleep(5)
                if self.isElement("xpath", tbjpy.newpeople_buy_check)==True:
                    print 5
                    amount_text=self.driver.find_element_by_xpath(tbjpy.newpeople_buy_check).get_attribute("name")
                    print amount_text
                    self.new_people_product(trade_num,expect1)
                else:
                    print 6
                    self.normal_product(amount,trade_num,expect2)
            else:
                if self.isElement("xpath", tbjpy.newpeople_buy_check)==True:
                    self.new_people_product(trade_num,expect1)
                else:
                    self.normal_product(amount,trade_num,expect2)

    def financing_verify(self):
        self.tab_financing_products()
        sleep(3)
        x=self.driver.get_window_size()['width']
        finance_up=self.driver.find_element_by_id(tbjpy.financing_up).location
        finance_up_location_y=finance_up['y']
        finance_up_y=finance_up_location_y
        finance_down=self.driver.find_element_by_xpath(tbjpy.financing_down).location
        finance_down_location_y=finance_down['y']
        finance_down_size=self.driver.find_element_by_xpath(tbjpy.financing_down).size
        finance_down_size_y=finance_down_size['height']
        finance_down_y=finance_down_location_y+finance_down_size_y

        page_source1=self.driver.page_source
        names=self.driver.find_elements_by_id(tbjpy.financing_name)
        length=len(names)
        print length
        for i in range(length):
            financename_text=self.driver.find_element_by_xpath('//android.widget.LinearLayout[@index=%d]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[@index=1]/android.widget.TextView'%(i+1)).get_attribute("name")
            self.click_button((By.XPATH,'//android.widget.LinearLayout[@index=%d]/android.widget.LinearLayout'%(i+1)))
            self.driver.implicitly_wait(10)
            financename_title=self.driver.find_element_by_id(tbjpy.title).get_attribute("name")
            if financename_title==u'铜宝':
                pass
                #print '进入铜宝购买页'
            elif financename_text==u'产品预告':
                pass
                #raise Exception('ee')
                #raise Exception('ee')
            elif financename_text==u'升级测试':
                pass
                #raise Exception('ee')
            elif financename_text==financename_title:
                pass
                #print '产品正确'
            else:
                pass
                #print '产品错误'
            if self.isElement("xpath", tbjpy.first_financing)!=True:
                pass
                #print '没有产品'
            else:
                pass
                #print '有产品'
            self.click_button((By.ID, tbjpy.tv_left_option))
        print 1
        self.driver.swipe(x/2,finance_down_y,x/2,finance_up_y,3000)
        print 2
        sleep(4)
        page_source2=self.driver.page_source
        while page_source1!=page_source2:
            names=self.driver.find_elements_by_id(tbjpy.financing_name)
            length=len(names)
            for i in range(length):
                financename_text=self.driver.find_element_by_xpath('//android.widget.LinearLayout[@index=%d]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[@index=1]/android.widget.TextView'%(i+1)).get_attribute("name")
                print 22
                self.click_button((By.XPATH,'//android.widget.LinearLayout[@index=%d]/android.widget.LinearLayout'%(i+1)))
                print 33
                self.driver.implicitly_wait(10)
                financename_title=self.driver.find_element_by_id(tbjpy.title).get_attribute("name")
                if financename_title==u'铜宝':
                    print '进入铜宝购买页'
                elif financename_text==u'产品预告':
                    raise Exception('ee')
                elif financename_text==u'升级测试':
                    raise Exception('ee')
                elif financename_text==financename_title:
                    print '产品正确'
                else:
                    print '产品错误'
                if self.isElement("xpath", tbjpy.first_financing)!=True:
                    print '没有产品'
                else:
                    print '有产品'
                self.click_button((By.ID, tbjpy.tv_left_option))
            sleep(6)
            page_source1=page_source2
            page_source2=self.driver.page_source
            print '继续滑动'
        else:
            print '已经滑到底'

        # self.click_second_financing_name()
        # location=self.driver.find_element_by_xpath('//android.widget.FrameLayout/android.widget.LinearLayout[@index=0]').size
        # location_y=location['height']-1
        # menu_default_y=self.driver.find_element_by_id(tbjpy.menu_default).location['y']
        # menu_default_height=self.driver.find_element_by_id(tbjpy.menu_default).size['height']
        # menu_default_y2=menu_default_y+menu_default_height+1
        # print menu_default_y2,location_y
        # #print location_y
        # page_source1=self.driver.page_source
        # self.driver.swipe(x/2,menu_default_y2,x/2,location_y,3000)
        # print 2
        # page_source2=self.driver.page_source
        # while page_source1!=page_source2:
        #     self.driver.swipe(x/2,1667,x/2,317,3000)
        #     sleep(6)
        #     page_source1=page_source2
        #     page_source2=self.driver.page_source
        #     print '继续滑动'
        # else:
        #     print '已经滑到底'

    def test_invite_friends(self):
        self.click_more()
        self.click_button((By.ID, tbjpy.more_invite))
        pass

    #4.2我的资产页的信息中心滑动查看功能
    def myproperty_message_slide42(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        # print 1
        self.myproperty()
        # print 2
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            return self.message_slide(expect)
        else:
            return self.message_slide(expect)

    #5.1我的资产页的信息中心滑动查看功能
    def myproperty_message_slide51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        # print 1
        self.myproperty()
        # print 2
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.click_more()
            self.click_login51()
            self.login(phone_num,passwd)
            self.myproperty()
            return self.message_slide(expect)
        else:
            return self.message_slide(expect)

    #4.2我的资产页的当前收益滑动查看功能
    def myproperty_nowincome_slide42(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        # print 1
        self.myproperty()
        # print 2
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            return self.now_income(expect)
        else:
            return self.now_income(expect)

    #4.2我的资产页的当前收益滑动查看功能
    def myproperty_nowincome_slide42(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        # print 1
        self.myproperty()
        # print 2
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            return self.now_income(expect)
        else:
            return self.now_income(expect)

    #4.3我的资产页的当前收益滑动查看功能
    def myproperty_nowincome_slide43(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        # print 1
        self.myproperty()
        # print 2
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            return self.now_income43(expect)
        else:
            return self.now_income43(expect)

    #5.1我的资产页的当前收益滑动查看功能
    def myproperty_nowincome_slide51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        # print 1
        self.myproperty()
        # print 2
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.click_more()
            self.click_login51()
            self.login(phone_num,passwd)
            self.myproperty()
            return self.now_income43(expect)
        else:
            return self.now_income43(expect)

    #4.3我的资产页的交易记录滑动查看功能
    def myproperty_all_trade_record_slide42(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            return self.check_all_trade_record(expect)
        else:
            return self.check_all_trade_record(expect)

    #4.3我的资产页的交易记录滑动查看功能
    def myproperty_all_trade_record_slide43(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            return self.check_all_trade_record43(expect)
        else:
            return self.check_all_trade_record43(expect)

    #5.1我的资产页的交易记录滑动查看功能
    def myproperty_all_trade_record_slide51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.click_more()
            self.click_login51()
            self.login(phone_num,passwd)
            self.myproperty()
            return self.check_all_trade_record43(expect)
        else:
            return self.check_all_trade_record43(expect)

    #4.2我的资产页的铜宝收益滑动查看功能
    def myproperty_tongbao_income_slide42(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            return self.check_tongbao_income(expect)
        else:
            return self.check_tongbao_income(expect)

    #4.3我的资产页的铜宝收益滑动查看功能
    def myproperty_tongbao_income_slide43(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            return self.check_tongbao_income43(expect)
        else:
            return self.check_tongbao_income43(expect)

    #5.1我的资产页的铜宝收益滑动查看功能
    def myproperty_tongbao_income_slide51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.click_more()
            self.click_login51()
            print 111
            self.login(phone_num,passwd)
            #self.back()
            print 222
            sleep(3)
            self.myproperty()
            print 11
            return self.check_tongbao_income43(expect)
        else:
            return self.check_tongbao_income43(expect)

    #4.2我的资产页的资产详情滑动查看功能
    def myproperty_myproperty_product_slide42(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        #print 1
        self.myproperty()
        #print 2
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            return self.check_myproperty_product(expect)
        else:
            return self.check_myproperty_product(expect)

    #4.3我的投资查看，滑动
    def check_my_investment(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.myAccount()
            self.login(phone_num,passwd)
            self.myproperty()
            return self.my_investment_slide43(expect)
        else:
            return self.my_investment_slide43(expect)

    #5.1我的投资查看，滑动
    def check_my_investment51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,expect=True):
        self.myproperty()
        total_assets_num=self.driver.find_element_by_id(tbjpy.total_assets).get_attribute("text")
        if total_assets_num=='0.00':
            self.click_more()
            self.click_login51()
            self.login(phone_num,passwd)
            self.myproperty()
            sleep(3)
            return self.my_investment_slide43(expect)
        else:
            sleep(3)
            return self.my_investment_slide43(expect)

    #4.2理财产品购买
    def finance_products42(self,phone_num=testdata.phone_num,passwd=testdata.passwd,amount2=testdata.tongbaoin_num,amount3=testdata.normal_product_num,trade_num=testdata.trade_pwd,expect=True):
        sleep(3)
        self.tab_financing_products()
        self.driver.find_elements_by_id(tbjpy.finance_product)[0].click()
        self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
        if self.isElement("id", tbjpy.input_phone)==True:
            # print 3
            self.login(phone_num,passwd)
            self.back()
            #遍历购买
            return self.buy_financing_products42(amount2,amount3,trade_num,expect)
        else:
            #print 1
            sleep(4)
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            # print 2
            self.back()
            return self.buy_financing_products42(amount2,amount3,trade_num,expect)

    #5.1精品推荐
    def buy_hot_product_51(self,phone_num=testdata.phone_num,passwd=testdata.passwd,amount2=testdata.tongbaoin_num,amount3=testdata.normal_product_num,trade_num=testdata.trade_pwd,expect=True):
        sleep(3)
        self.hot_product()
        if self.isElement("id", tbjpy.hot_product_login)==True:
            print 1
            self.click_button((By.ID, tbjpy.hot_product_login))
            self.login(phone_num,passwd)
            return self.buy_hot_product51(amount2,amount3,trade_num,expect)
        else:
            # print 2
            return self.buy_hot_product51(amount2,amount3,trade_num,expect)
            pass

    #5.1理财产品购买
    def finance_products51(self,amount2=testdata.tongbaoin_num,amount3=testdata.normal_product_num,trade_num=testdata.trade_pwd,expect=True):
        self.financing_products()
        return  self.buy_financing_products51(amount2,amount3,trade_num,expect)
        # pass

    #5.2理财产品购买
    def finance_products52(self,amount2=testdata.tongbaoin_num,amount3=testdata.normal_product_num,recharge_num=testdata.recharge_num,trade_num=testdata.trade_pwd,expect=True):
        self.financing_products()
        # print trade_num
        return self.buy_financing_products52(amount2,amount3,recharge_num,trade_num,expect)

    def test(self,trade_num=testdata.trade_pwd):
        self.financing_products()
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        product_form51s=self.driver.find_elements_by_id(tbjpy.product_form51)
        finance_lable_default=self.driver.find_element_by_xpath(tbjpy.finance_lable).location
        finance_lable_default_y=finance_lable_default['y']
        finance_lable_default_size=self.driver.find_element_by_xpath(tbjpy.finance_lable).size
        finance_lable_default_size_y=finance_lable_default_size['height']
        finance_lable_size_y=finance_lable_default_y+finance_lable_default_size_y
        tongbao_52_default=self.driver.find_element_by_id(tbjpy.tongbao_52).location
        tongbao_52_default_y=tongbao_52_default['y']
        tongbao_52_default_size=self.driver.find_element_by_id(tbjpy.tongbao_52).size
        tongbao_52_default_size_y=tongbao_52_default_size['height']
        tongbao_52_size_y=tongbao_52_default_y+tongbao_52_default_size_y
        self.driver.swipe(x/2,tongbao_52_size_y+1,x/2,finance_lable_size_y+1,1000)
        financing_name=self.driver.find_element_by_xpath("//android.widget.TextView[@text='产品预告']").get_attribute("text")
        print financing_name
        self.click_button((By.XPATH,"//android.widget.TextView[@text='产品预告']"))
        if re.findall(u"产品",financing_name)!=[]:
            pass
            print 222
            sleep(4)
            self.driver.tap([(200, 100)])
            # self.click_button((By.XPATH,tbjpy.product_advance_notice_back))
        # self.click_button((By.XPATH,"//android.widget.TextView[@text='转让专区']"))
        # product_name51s=self.driver.find_elements_by_id(tbjpy.product_name51)
        # for product_name in product_name51s:
        #     product_name.click()
        #     self.click_button((By.ID,tbjpy.transfer_buy))
        #     if self.isElement("xpath",tbjpy.Bond_dialog_message)==True:
        #         self.click_button((By.ID,tbjpy.click_sure))
        #         self.back()
        #         # self.back()
        #     else:
        #         self.click_button((By.XPATH,tbjpy.transfer_pay))
        #         print 22
        #     # sleep(5)
        #     # self.transfer_market_pay()
        # # print 555
        #         self.send_trade_pwd(trade_num)
        #         self.click_sure()
        #         sleep(6)
        #         self.click_button((By.XPATH,tbjpy.check_buy_success_btn))
        #     # self.back()

# print a

import threading

if __name__ == '__main__':
    t = Case('Android','4.3','',u'6O5721A11031','com.tongbanjie.android','TBJWelcomeActivity','localhost',4720)

    # t.add_case('myaccout_sign',t.myaccout_sign)
    # t.add_case('myaccout_sign51',t.myaccout_sign51)
    # t.add_case('手机号长度不满11位',t.myaccout_login_error1)
    # t.add_case('myaccout_login_error2',t.myaccout_login_error2)
    # t.add_case('myaccout_login_error3',t.myaccout_login_error3)
    # t.add_case('myaccout_login_error4',t.myaccout_login_error4)
    # t.add_case('登陆成功',t.myaccout_login)

    # t.add_case('myaccout_login51',t.myaccout_login51)
    # t.add_case('myaccout_sign51',t.myaccout_sign51)
    # t.add_case('myaccout_login51_error1',t.myaccout_login51_error1)
    # t.add_case('myaccout_login51_error2',t.myaccout_login51_error2)
    # t.add_case('myaccout_login51_error3',t.myaccout_login51_error3)
    # t.add_case('myaccout_login51_error4',t.myaccout_login51_error4)
    #
    # t.add_case('modify_loginpwd_after_login',t.modify_loginpwd_after_login)
    # t.add_case('modify_loginpwd_after_login_error1',t.modify_loginpwd_after_login_error1)
    # t.add_case('modify_loginpwd_after_login_error2',t.modify_loginpwd_after_login_error2)
    # t.add_case('modify_trade_pwd_after_login',t.modify_trade_pwd_after_login)
    # t.add_case('modify_trade_pwd_after_login_error1',t.modify_trade_pwd_after_login_error1)
    # t.add_case('modify_trade_pwd_after_login_error2',t.modify_trade_pwd_after_login_error2)
    # t.add_case('modify_trade_pwd_after_login_error3',t.modify_trade_pwd_after_login_error3)
    # t.add_case('modify_trade_pwd_after_login_error4',t.modify_trade_pwd_after_login_error4)
    # t.add_case('modify_trade_pwd_after_login_error5',t.modify_trade_pwd_after_login_error5)
    # #
    # t.add_case('modify_loginpwd_after_login51',t.modify_loginpwd_after_login51)
    # t.add_case('modify_loginpwd_after_login51_error1',t.modify_loginpwd_after_login51_error1)
    # t.add_case('modify_loginpwd_after_login51_error2',t.modify_loginpwd_after_login51_error2)
    # t.add_case('modify_trade_pwd_after_login51',t.modify_trade_pwd_after_login51)
    # t.add_case('modify_trade_pwd_after_login51_error1',t.modify_trade_pwd_after_login51_error1)
    # t.add_case('modify_trade_pwd_after_login51_error2',t.modify_trade_pwd_after_login51_error2)
    # t.add_case('modify_trade_pwd_after_login51_error3',t.modify_trade_pwd_after_login51_error3)
    # t.add_case('modify_trade_pwd_after_login51_error4',t.modify_trade_pwd_after_login51_error4)
    # t.add_case('modify_trade_pwd_after_login51_error5',t.modify_trade_pwd_after_login51_error5)

    # t.add_case('balance_out4',t.balance_out4)
    # t.add_case('balance_out4_error1',t.balance_out4_error1)
    # t.add_case('balance_out4_error2',t.balance_out4_error2)
    # t.add_case('balance_into4',t.balance_into4)
    # t.add_case('balance_into4_error1',t.balance_into4_error1)
    #
    # t.add_case('balance_out5',t.balance_out5)
    # t.add_case('balance_out5_error1',t.balance_out5_error1)
    # t.add_case('balance_out5_error2',t.balance_out5_error2)
    # t.add_case('balance_in5',t.balance_in5)
    # t.add_case('balance_in5_error1',t.balance_in5_error1)
    # t.add_case('balance_in5_error2',t.balance_in5_error2)
    #
    # t.add_case('balance_out51',t.balance_out51)
    # t.add_case('balance_out51_error1',t.balance_out51_error1)
    # t.add_case('balance_out51_error2',t.balance_out51_error2)
    # t.add_case('balance_in51',t.balance_in51)
    # t.add_case('balance_in51_error1',t.balance_in51_error1)
    # t.add_case('balance_in51_error2',t.balance_in51_error2)
    # #购买流程
    #
    # t.add_case('myproperty_tongbao_in42',t.myproperty_tongbao_in42)
    # t.add_case('myproperty_tongbao_out42',t.myproperty_tongbao_out42)
    # t.add_case('myproperty_tongbao_in43',t.myproperty_tongbao_in43)
    # t.add_case('myproperty_tongbao_out43',t.myproperty_tongbao_out43)
    # t.add_case('myproperty_tongbao_in51',t.myproperty_tongbao_in51)
    # t.add_case('myproperty_tongbao_out51',t.myproperty_tongbao_out51)

    # t.add_case('myproperty_message_slide42',t.myproperty_message_slide42)
    # t.add_case('myproperty_message_slide51',t.myproperty_message_slide51)
    # t.add_case('myproperty_nowincome_slide42',t.myproperty_nowincome_slide42)
    # t.add_case('myproperty_all_trade_record_slide42',t.myproperty_all_trade_record_slide42)
    # t.add_case('myproperty_myproperty_product_slide42',t.myproperty_myproperty_product_slide42)
    # t.add_case('myproperty_tongbao_income_slide42',t.myproperty_tongbao_income_slide42)
    # t.add_case('myproperty_nowincome_slide43',t.myproperty_nowincome_slide43)
    # t.add_case('myproperty_all_trade_record_slide43',t.myproperty_all_trade_record_slide43)
    # t.add_case('myproperty_tongbao_income_slide43',t.myproperty_tongbao_income_slide43)
    # t.add_case('myproperty_nowincome_slide51',t.myproperty_nowincome_slide51)
    # t.add_case('myproperty_all_trade_record_slide51',t.myproperty_all_trade_record_slide51)
    # t.add_case('myproperty_tongbao_income_slide51',t.myproperty_tongbao_income_slide51)
    # t.add_case('check_my_investment',t.check_my_investment)
    # t.add_case('check_my_investment51',t.check_my_investment51)
    # t.add_case('buy_hot_product',t.buy_hot_product)
    # t.add_case('finance_products42',t.finance_products42)
    t.add_case('buy_hot_product_51',t.buy_hot_product_51)
    # t.add_case('finance_products51',t.finance_products51)
    # t.add_case('finance_products52',t.finance_products52)

    # t.add_case('test',t.test)
    # t.add_case('more_check42',t.more_check42)
    # t.add_case('more_check43',t.more_check43)
    # t.add_case('more_check5',t.more_check5)
    # t.add_case('more_check51',t.more_check51)
    # t.add_case('more_check52',t.more_check52)

    # t.run()

    def start():
        t.run()
    thread_1 = threading.Thread(target=start,name='thread_1')
    thread_1.setDaemon(True)
    thread_1.start()

    while not t.finsh_flag:
        data = t.stdout.readline()
        if data:
            print data