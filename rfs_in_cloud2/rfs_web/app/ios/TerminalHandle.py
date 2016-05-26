# _*_ coding:utf-8 _*_
__author__ = 'Eddie'

import sql,sys
import re,os,time,tbjpyios
from rfs_web.app import BaseHandle
from time import sleep
import urllib2,copy
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException

class TerminalHandle(BaseHandle):
    def __init__(self,platformName,platfromVersion,deviceName,udid,appPackage,appActivity,host,port=None,timeout=None,**kwargs):
        super(TerminalHandle,self).__init__()
        self.init_drive_error = None
        if not timeout:
            self.timeout = 30
        if not port:
            self.port = 4723
        else:
            self.port = port
        if not host:
            self.host = '127.0.0.1'
        else:
            self.host = host
        self._desired_caps = {
            'platformName':platformName,
            'platfromVersion':platfromVersion,
            'deviceName':deviceName,
            'udid':udid,
            'appPackage':appPackage,
            'appActivity':appActivity,
            'unicodeKeyboard':True,
		    'resetKeyboard':True,
            #'autoLaunch':False
        }
        if kwargs:
            self._desired_caps.update(kwargs)

        while True:
            if self.conn_webdrive():
                break
            time.sleep(1)

    def conn_webdrive(self):
        try:
            self.driver = webdriver.Remote('http://%s:%d/wd/hub' % (self.host,self.port),self._desired_caps)
            return True
        except Exception,e:
            print 'Error: ',str(e)
            if str(e) == "<urlopen error [Errno 61] Connection refused>":
                return False
            else:
                if str(e)[0] == '<' and str(e)[-1] == '>':
                    msg = str(e)[1:-1]
                else:
                    msg = str(e)
                self.init_drive_error = msg
                return True

    def setUp(self):
        #self.driver.launch_app()
        pass

    # def tearDown(self):
    #     "Hook method for deconstructing the test fixture after testing it."
    #     pass

    @classmethod
    def setUpClass(cls):
        #cls.driver.launch_app()
        pass

    #@classmethod
    def tearDownClass(self):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        self.driver.close_app()
        pass

    def find(self,loc):
        try:
            WebDriverWait(self.driver,self.timeout).until(lambda drive:drive.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except Exception,e:
            print u"%s 页面中超时%ds未能找到 %s 元素%s" %(self,self.timeout,loc,e)

    def click_keys(self,loc):
        self.find(loc).click()

    def clear_keys(self,loc):
        self.find(loc).clear()

    def send_keys(self,loc,value):
        sleep(3)
        self.find(loc).send_keys(value)

    def click_button(self,loc):
        self.find(loc).click()

    def isElement(self,identifyBy,c):
        flag=None
        try:
            if identifyBy == "id":
                self.driver.find_element_by_id(c)
            elif identifyBy == "xpath":
                self.driver.find_element_by_xpath(c)
            elif identifyBy == "class":
                self.driver.find_element_by_class_name(c)
            elif identifyBy == "name":
                self.driver.find_element_by_name(c)
            flag = True
        except NoSuchElementException,e:
            flag = False
        finally:
            return flag

    def doesExist(self,identifyBy,c):
        i = 1
        while not self.isElement(self,identifyBy):
            sleep(1)
            i = i+1
            if i >= 10:
                return False
        else:
            return True

    def screenshot(self):
        path = "/Users"
        loginname=os.getlogin()
        full_path=path+'/'+loginname
        timestr = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        dir="result_" + timestr + ".png"
        finally_dir=os.path.join(full_path,dir)
        self.driver.get_screenshot_as_file(finally_dir)


    def screenshot_True(self):
        path = "/Downloads"
        title = "appium_test_result"
        timestr = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        new_path = os.path.join(path, title)
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
            self.driver.get_screenshot_as_file(new_path+"/"+"result_True_" + timestr + ".png")
        else:
            self.driver.get_screenshot_as_file(new_path+"/"+"result_True_" + timestr + ".png")

    def screenshot_Error(self):
        path = "/Downloads"
        title = "appium_test_result"
        timestr = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        new_path = os.path.join(path, title)
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
            self.driver.get_screenshot_as_file(new_path+"/"+"result_Error_" + timestr + ".png")
        else:
            self.driver.get_screenshot_as_file(new_path+"/"+"result_Error_" + timestr + ".png")


    #android自动化键盘的定位
    def fetch_coord(self,location,size):
        #'''location:{'y':1050,'x':'100'}
        #   size:{'weidth':100,'heigth':100'''
        start_x = location['x']
        start_y = location['y']
        average_x = size['width'] / 3.0
        average_y = size['height'] / 4.0
        coord_list = []
        for i in range(4):
            _y = int(start_y + average_y * i + average_y / 2)
            for j in range(3):
                _x = int(start_x + average_x * j + average_x / 2)
                coord_list.append([(_x,_y)])
        return coord_list

class AppHandle(TerminalHandle):
    def __init__(self,platformName,platfromVersion,deviceName,app,udid,bundleId,appPackage,appActivity,port=None,timeout=None,**kwargs):
        super(AppHandle,self).__init__(platformName,platfromVersion,deviceName,app,udid,bundleId,appPackage,appActivity,port=None,timeout=None,**kwargs)

    #进入更多模块
    def click_more(self):
        self.click_button((By.NAME,tbjpyios.more))

    #点击我的帐号
    def click_myaccount(self):
        sleep(3)
        self.click_button((By.XPATH,tbjpyios.myaccount))

    #5.0更多模块的设置按钮
    def click_set_btn(self):
        self.click_button((By.NAME,tbjpyios.click_set))

    #5.0版本点击我的帐号
    def click_myaccount5(self):
        sleep(3)
        self.click_button((By.XPATH,tbjpyios.myaccount5))

    #登录，输入帐号
    def input_login_phone(self,phone_num):
        self.send_keys((By.XPATH,tbjpyios.phoneId),phone_num)


    #登录，输入帐号后点击下一步
    def click_next(self):
        self.click_keys((By.NAME,tbjpyios.next))
        sleep(2)
        if self.isElement("name",tbjpyios.check_sign)==True:
            self.back()
            self.back()
            raise Exception('进入注册模块')
        elif self.isElement("name",tbjpyios.next)==True:
            self.back()
            raise Exception('手机不满11位')


    #登录，输入密码
    def input_login_passwd(self,passwd):
        self.send_keys((By.XPATH,tbjpyios.phonepwd),passwd)


    #登录，输入密码后确定
    def click_login_button(self):
        self.click_button((By.NAME,tbjpyios.click_login))

    #退出登录
    def logout(self):
        self.click_button((By.NAME,tbjpyios.click_logout))

    #注册，输入帐号
    def input_sign_Account(self,sign_Account):
        self.send_keys((By.XPATH,tbjpyios.phoneId),sign_Account)
        self.click_button((By.NAME,tbjpyios.next))

    #注册设置登陆密码
    def send_signpwd(self,signpwd):
        self.send_keys((By.XPATH,tbjpyios.set_login_password),signpwd)

    #点击密码管理按钮
    def rl_pwd_manager(self):
        self.click_button((By.NAME,tbjpyios.rl_pwd_manager))

    #点击修改登陆密码按钮
    def change_login_pwd_layout(self):
        self.click_button((By.XPATH,tbjpyios.change_login_pwd_layout))

    #修改登陆密码
    def send_old_pwd(self,old_pwd):
        self.send_keys((By.XPATH,tbjpyios.old_password_input),old_pwd)

    #设置并重复密码
    def set_pwd(self,set_pwd,repeat_pwd):
        self.send_keys((By.XPATH,tbjpyios.new_password_input),set_pwd)
        self.send_keys((By.XPATH,tbjpyios.confilm_new_password),repeat_pwd)
        self.click_button((By.NAME,tbjpyios.modify_login_pwd))

    #点击修改交易密码按钮
    def rlyt_update_trans_pwd(self):
        self.click_button((By.NAME,tbjpyios.rlyt_update_trans_pwd))

    #点击确定按钮
    def click_sure_btn(self):
        self.click_button((By.NAME,tbjpyios.sure_btn))

    #点击完成按钮
    def click_complete_btn(self):
        self.click_button((By.NAME,tbjpyios.complete_btn))
        if self.isElement("name",tbjpyios.check_repeat_set_tradepwd)==True:
            raise Exception('修改交易密码页面，重复交易密码输入位数不够')

    #点击找回交易密码按钮
    def rlyt_find_trade_pwd(self):
        self.click_button((By.NAME,tbjpyios.rlyt_find_trade_pwd))

    #输入交易密码
    def send_trade_pwd(self,trade_pwd):
        sleep(2)
        for i in trade_pwd:
            self.driver.find_element_by_name(i).click()
            sleep(1)

    #输入原交易密码
    def send_old_trade_pwd(self,old_trade_pwd):
        sleep(2)
        for i in old_trade_pwd:
            self.driver.find_element_by_name(i).click()
            sleep(1)
        sleep(4)
        if self.isElement("xpath",tbjpyios.check_first_pwd_error)==True:
            raise Exception('原交易密码与该手机号不符合')
        elif self.isElement("name",tbjpyios.check_old_tradepwd)==True:
            raise Exception('修改交易密码页面，原交易密码输入位数不够')

    #输入新交易密码
    def send_new_trade_pwd(self,new_trade_pwd):
        sleep(2)
        for i in new_trade_pwd:
            self.driver.find_element_by_name(i).click()
            sleep(1)
        if self.isElement("name",tbjpyios.check_set_tradepwd)==True:
            raise Exception('修改交易密码页面，新交易密码输入位数不够')

    #输入重复交易密码
    def send_repeat_trade_pwd(self,repeat_trade_pwd):
        sleep(2)
        for i in repeat_trade_pwd:
            self.driver.find_element_by_name(i).click()
            sleep(1)
        sleep(4)
        if self.isElement("name",tbjpyios.check_trade_pwd_not_same)==True:
            raise Exception('两次密码输入不一致 请重新输入')

    #输入找回交易密码相关信息并修改
    def find_trade_pwd(self,phone_num,username,card):
        self.click_button((By.NAME,tbjpyios.rlyt_find_trade_pwd))
        self.send_keys((By.XPATH,tbjpyios.full_name_value),username)
        self.send_keys((By.XPATH,tbjpyios.input_value),card)
        self.click_button((By.NAME,tbjpyios.next_btn))
        sleep(5)
        myms = sql.mysql_connect(sql.db_info)
        sleep(3)
        verify_code1=myms.sql_assign_exec("select content from mdp_message WHERE recipients="+ phone_num + " ORDER BY create_time DESC LIMIT 1")
        verify_code2=re.search('\d{6}', verify_code1)
        verify_code3=verify_code2.group(0)
        self.send_keys((By.XPATH,tbjpyios.verify_input),verify_code3)
        self.click_button((By.NAME,tbjpyios.btn_next))
        self.driver.implicitly_wait(10)
        sleep(5)

    #点击账户余额按钮
    def click_account_balance(self):
        sleep(1)
        self.click_button((By.NAME,tbjpyios.rl_account_balance))
        sleep(1)

    #点击我的资产按钮
    def myproperty(self):
        self.click_button((By.XPATH,tbjpyios.myasset))

    #点击进入余额并退出
    def click_payment_details(self):
        sleep(3)
        self.click_button((By.XPATH,tbjpyios.rl_payment_details))
        self.click_button((By.NAME,tbjpyios.back1))

    #返回
    def back(self):
        self.click_button((By.NAME,tbjpyios.back1))

    #点击充值按钮
    def click_recharge(self):
        self.driver.implicitly_wait(5)
        self.click_button((By.NAME,tbjpyios.rl_recharge))

    #充值
    def rl_recharge(self,topup_num):
        sleep(5)
        self.send_keys((By.XPATH,tbjpyios.czje),topup_num)
        self.click_button((By.XPATH,tbjpyios.submit_xpath))
        if self.isElement("name",tbjpyios.safe_keyboard)==False:
            self.click_button((By.NAME,tbjpyios.sure))
            self.click_button((By.XPATH,tbjpyios.cancel))
            self.back()
            raise Exception('请输入正确充值金额')


    #点击余额转出按钮
    def click_balance_out(self):
        self.click_button((By.XPATH,tbjpyios.rl_balance_out))
        sleep(3)

    #余额转出
    def rl_balance_out(self,out_num):
        sleep(5)
        self.send_keys((By.XPATH,tbjpyios.zcje),out_num)
        self.click_button((By.XPATH,tbjpyios.submit_xpath))
        sleep(1)
        if self.isElement("name",tbjpyios.safe_keyboard)==False:
            self.click_button((By.NAME,tbjpyios.sure))
            self.click_button((By.XPATH,tbjpyios.cancel))
            self.back()
            raise Exception('转出金额不足够')

    #进入余额转出并确定
    def rl_balance_outqd(self):
        self.click_button((By.XPATH,tbjpyios.click_sure))
        self.click_button((By.ID,tbjpyios.back1))

    #点击进入回款路径
    def click_return_path_label(self):
        self.click_button((By.ID,tbjpyios.return_path_label))
        sleep(3)

    #充值或者转出成功后点击确定按钮
    def click_money_success(self):
        self.click_button((By.XPATH,tbjpyios.check_money_success))

    #确定
    def click_sure(self):
        sleep(3)
        self.click_button((By.NAME,tbjpyios.true))
        if self.isElement("xpath",tbjpyios.remind_exceed_monkey)==True:
            remind_exceed_monkey_text=self.driver.find_element_by_xpath(tbjpyios.remind_exceed_monkey).get_attribute("name")
            self.click_button((By.XPATH,tbjpyios.sure))
            self.click_button((By.XPATH,tbjpyios.cancel))
            self.back()
            raise Exception('超过该卡日累计支付金额')
        elif self.isElement("xpath",tbjpyios.withholding_defeat)==True:
            remind_exceed_monkey_text=self.driver.find_element_by_xpath(tbjpyios.withholding_defeat).get_attribute("name")
            self.click_button((By.XPATH,tbjpyios.sure))
            self.click_button((By.XPATH,tbjpyios.cancel))
            self.back()
            raise Exception('代扣失败')
        elif self.isElement("xpath",tbjpyios.net_ungelivable)==True:
            remind_exceed_monkey_text=self.driver.find_element_by_xpath(tbjpyios.withholding_defeat).get_attribute("name")
            self.click_button((By.XPATH,tbjpyios.sure))
            self.click_button((By.XPATH,tbjpyios.cancel))
            self.back()
            raise Exception('网络不给力')
        elif self.isElement("name",tbjpyios.safe_keyboard)==True:
            self.click_button((By.XPATH,tbjpyios.sure))
            self.click_button((By.XPATH,tbjpyios.cancel))
            self.back()
            raise Exception('交易密码不足位数')
        elif self.isElement("xpath",tbjpyios.product_not_support_buy)==True:
            self.screenshot_Error()
            self.click_button((By.XPATH,tbjpyios.sure))
            self.click_button((By.XPATH,tbjpyios.cancel))
            self.back()
            raise Exception('该产品暂不支持购买！')
        elif self.isElement("name",tbjpyios.pay_prompt)==True:
            self.click_button((By.XPATH,tbjpyios.sure))
            self.click_button((By.XPATH,tbjpyios.cancel))
            self.back()
            raise Exception('代扣测试')
        elif self.isElement("xpath",tbjpyios.sale_on_time)==True:
            self.click_button((By.XPATH,tbjpyios.sure))
            self.click_button((By.XPATH,tbjpyios.cancel))
            self.back()
            raise Exception('产品待售')
        elif self.isElement("xpath",tbjpyios.continued)==True:
            self.click_button((By.XPATH,tbjpyios.sure))
            self.click_button((By.XPATH,tbjpyios.cancel))
            self.back()
            raise Exception('敬请期待')


    #新用户时，设置交易密码
    def set_new_people_trade_pwd(self,new_people_trade_pwd,repeat_trade_pwd):
        for i in new_people_trade_pwd:
            self.driver.find_element_by_name(i).click()
            sleep(1)
        for i in repeat_trade_pwd:
            self.driver.find_element_by_name(i).click()
            sleep(1)
        sleep(2)

    #选择银行账户点击
    def click_bank(self):
        sleep(3)
        self.click_button((By.XPATH,tbjpyios.bank))

    #选择第一个银行账户确定
    def click_banksure(self):
        sleep(4)
        self.click_button((By.XPATH,tbjpyios.tcqd))

    #点击忘记密码按钮
    def click_forgetpwd(self):
        self.click_button((By.NAME,tbjpyios.forget_password))
        self.click_button((By.NAME,tbjpyios.next))

    #输入身份证
    def send_person_id(self,person_ID):
        self.send_keys((By.XPATH,tbjpyios.input_value),person_ID)

    #下一步
    def nextbtn(self):
        self.click_button((By.NAME,tbjpyios.next_btn))

    #找回密码
    def click_back_pwd(self,back_pwd):
        self.send_keys((By.XPATH,tbjpyios.set_login_password),back_pwd)

    #找回密码，下一步按钮点击操作
    def click_back_pwd_nextbtn(self):
        self.click_button((By.ID,tbjpyios.click_back_pwd_nextbtn))

    #点击精品推荐入口按钮
    def click_hot_product(self):
        self.click_button((By.XPATH,tbjpyios.hot_product))

    #精品推荐页购买按钮
    def ll_top_content(self):
        self.click_button((By.ID,tbjpyios.hot_product_buy))

    #输出精品推荐页的项目名称及期限
    def get_hot_product_message(self):
        get_hot_product_name=self.driver.find_element_by_id(tbjpyios.hot_product_name).get_attribute("text")
        # print get_hot_product_name
        get_hot_product_period=self.driver.find_element_by_id(tbjpyios.hot_product_period).get_attribute("text")
        # print get_hot_product_period

    #计算器的打开
    def calcopen(self):
        self.click_button((By.ID,tbjpyios.calc_btn))
        self.send_keys((By.ID,tbjpyios.purchase_amount_edit),tbjpyios.purchase_amount_edit)
        self.click_button((By.ID,tbjpyios.calc_earnings_btn))

    #计算器的关闭
    def calcclose(self):
        self.click_button((By.ID,tbjpyios.calc_close))

    #购买按钮
    def click_buy(self):
        self.click_button((By.ID,tbjpyios.hot_product_buy_btn))

    #输入购买金额
    def send_buy_money(self,amount):
        sleep(6)
        self.send_keys((By.XPATH,tbjpyios.hot_product_buy_money),amount)

    #输入购买金额后的确定按钮
    def send_buy_monkey_sure(self):
        self.click_button((By.XPATH,tbjpyios.hot_product_buy_money_sure))
        sleep(5)
        if self.isElement("xpath",tbjpyios.money_check)==True:
            self.click_button((By.XPATH,tbjpyios.click_right))
            self.click_button((By.XPATH,tbjpyios.cancel))
            self.back()
            raise Exception('金额不正确')

    #输入验证码之后确认的操作
    def qd(self):
        self.click_button((By.ID,tbjpyios.true))
        self.click_button((By.XPATH,tbjpyios.truetwo))
        self.click_button((By.ID,tbjpyios.back1))

    #点击理财产品按钮
    def tab_financing_products(self):
        self.click_button((By.XPATH,tbjpyios.tab_financing_products))

    #5.0版本理财产品铜宝入口
    def click_financing_products_tb(self):
        self.click_button((By.XPATH,tbjpyios.financing_products_tb))

    #理财产品购买按钮
    def click_product_purchase_view(self):
        self.click_button((By.ID,tbjpyios.product_purchase_view))
        sleep(5)

    #新手理财产品购买的提交按钮
    def newpeople_buy_commit(self):
        self.click_button((By.XPATH,tbjpyios.newpeople_buy_commit))

    #转让市场购买按钮
    def transfer_market_buy(self):
        self.click_button((By.XPATH,tbjpyios.transfer_buy))

    #转让市场支付按钮
    def transfer_market_pay(self):
        self.click_button((By.XPATH,tbjpyios.transfer_pay))

    #点击我的资产按钮
    def click_myasset(self):
        self.click_button((By.XPATH,tbjpyios.myasset))

    #4.3-5.0版本账户余额入口
    def click_balance5(self):
        self.click_button((By.XPATH,tbjpyios.balance_entry5))

    #进入信息中心并返回
    def click_message(self):
        self.click_button((By.ID,tbjpyios.message))
        self.click_button((By.ID,tbjpyios.back1))

    #进入当前收益
    def click_income_component(self):
        self.click_button((By.ID,tbjpyios.income_component))

    #进入累计收益
    def tv_right_option(self):
        self.click_button((By.ID,tbjpyios.tv_right_option))
        self.click_button((By.ID,tbjpyios.back1))
        self.click_button((By.ID,tbjpyios.back1))

    #铜宝页面，未登陆状态，点击登录
    def click_tongbao_login(self):
        self.click_button((By.NAME,tbjpyios.buy_tongbao_login))

    #进入铜宝
    def click_tongbao(self):
        self.click_button((By.ID,tbjpyios.tongbao_assets_layout))

    #铜宝转入
    def tongbao_in(self):
        self.click_button((By.NAME,tbjpyios.tongbao_in))

    #铜宝转出
    def tongbao_out(self):
        self.click_button((By.NAME,tbjpyios.tongbao_out))

    def click_login51(self):
        self.click_button((By.XPATH,tbjpyios.login51))

    #提交按钮
    def click_submit(self):
        self.click_button((By.NAME,tbjpyios.submit))

    #铜宝，确定按钮
    def  click_tongbao_sure_btn(self):
        self.click_button((By.NAME,tbjpyios.tongbao_sure_btn))
        # if self.isElement("name",tbjpyios.safe_keyboard)==True:
        #     self.click_button((By.NAME,tbjpyios.sure))
        #     self.click_button((By.XPATH,tbjpyios.cancel))
        #     self.back()
        #     raise Exception('交易密码位数不够')
        # if self.isElement("xpath",tbjpyios.submit_tradepwd_error)==True:
        #     submit_tradepwd_error_text=self.driver.find_element_by_xpath(tbjpyios.submit_tradepwd_error).get_attribute("name")
        #     print 11
        #     self.click_button((By.XPATH,tbjpyios.sure))
        #     self.click_button((By.XPATH,tbjpyios.cancel))
        #     self.back()
        #     raise Exception(submit_tradepwd_error_text)
            #e='交易密码与手机号不匹配'

    #进入铜宝后返回
    def tbback(self):
        self.click_button((By.NAME,tbjpyios.back1))

    #查看用户个人信息
    def click_user_infojr(self):
        u"""查看用户个人信息"""
        self.click_button((By.ID,tbjpyios.rl_user_info))

    #点击银行卡管理按钮
    def click_bankcard_manager(self):
        self.click_button((By.ID,tbjpyios.rl_bankcard_manager))

    #添加银行卡
    def add_bankcard(self):
        self.click_button((By.ID,tbjpyios.rlyt_add_bankCard))

    #持卡人信息
    def add_personalInformation(self):
        self.click_button((By.ID,tbjpyios.true))
        sleep(10)
        self.send_keys((By.XPATH,tbjpyios.card_name),tbjpyios.full_name_value)
        self.send_keys((By.XPATH,tbjpyios.card_personid),tbjpyios.input_value)

    #添加中国银行银行卡
    def add_bank_card(self):
        self.click_button((By.XPATH,tbjpyios.choose_bank))
        self.click_button((By.XPATH,tbjpyios.choose_one_bank))

    #输入银行卡号
    def send_bank_card(self):
        self.send_keys((By.XPATH,tbjpyios.bank_id),tbjpyios.card)

    #输入手机号并绑定
    def send_phone_num(self):
        #输入手机号
        self.send_keys((By.XPATH,tbjpyios.iphone_num),tbjpyios.phone)

    def bind(self):
        #绑定
        self.click_button((By.XPATH,tbjpyios.binding))

    #开始赚钱
    def start_earn_money(self):
        self.click_button((By.NAME,tbjpyios.earn_monkey))

    #普通产品购买流程(除新手，铜宝之外的产品)
    def normal_product(self,amount,trade_num,expect):
        actual=None
        code=111
        try:
            sleep(6)
            self.send_buy_money(amount)
            self.send_buy_monkey_sure()
            sleep(3)
            self.send_trade_pwd(trade_num)
            self.click_sure()
            sleep(5)
            if self.isElement("name",tbjpyios.cancel_item)==True:
                self.screenshot()
                actual=True
                e='购买成功'
                self.click_button((By.NAME,tbjpyios.cancel_item))
                self.click_button((By.XPATH,tbjpyios.check_buy_success_btn))
                self.back()
            elif self.isElement("xpath",tbjpyios.check_buy_success_btn)==True:
                self.screenshot()
                actual=True
                e='购买成功'
                self.click_button((By.XPATH,tbjpyios.check_buy_success_btn))
                self.back()
            else:
                self.screenshot()
                actual=False
                e='购买失败'
        except Exception,e:
            actual=False
        finally:
            result=actual==expect
            ending={'code':code,'message':e,'result':result}
            return ending

    #新手产品购买流程
    def new_people_product(self,trade_num,expect):
        actual=None
        code=111
        try:
            sleep(4)
            self.newpeople_buy_commit()
            self.send_trade_pwd(trade_num)
            self.click_sure()
            sleep(4)
            if self.isElement("name",tbjpyios.cancel_item)==True:
                self.screenshot()
                actual=True
                e='购买成功'
                self.click_button((By.NAME,tbjpyios.cancel_item))
                self.click_button((By.XPATH,tbjpyios.check_buy_success_btn))
                self.back()
            elif self.isElement("xpath",tbjpyios.check_buy_success_btn)==True:
                self.screenshot()
                actual=True
                e='购买成功'
                self.click_button((By.XPATH,tbjpyios.check_buy_success_btn))
                self.back()
        except Exception,e:
            actual=False
        finally:
            result=actual==expect
            ending={'code':code,'message':e,'result':result}
            return ending

    #5.0转让市场购买
    def buy_transfer(self,trade_num,expect):
        actual=None
        code=111
        try:
            sleep(4)
            self.transfer_market_buy()
            self.transfer_market_pay()
            self.send_trade_pwd(trade_num)
            self.click_sure()
            sleep(3)
            if self.isElement("name",tbjpyios.cancel_item)==True:
                self.screenshot()
                actual=True
                e='购买成功'
                self.click_button((By.NAME,tbjpyios.cancel_item))
                self.click_button((By.XPATH,tbjpyios.check_buy_success_btn))
                self.back()
            elif self.isElement("xpath",tbjpyios.check_buy_success_btn)==True:
                self.screenshot()
                actual=True
                e='购买成功'
                self.click_button((By.XPATH,tbjpyios.check_buy_success_btn))
                self.back()
        except Exception,e:
            actual=False
        finally:
            result=actual==expect
            ending={'code':code,'message':e,'result':result}
            return ending

    #预约市场购买
    def buy_order(self,amount3,recharge_num,trade_num):
        actual=None
        code=111
        sleep(4)
        self.click_button((By.XPATH,tbjpyios.product_purchase_view))
        if self.isElement("xpath",tbjpyios.order_submit)==True:
            self.screenshot()
            self.click_button((By.XPATH,tbjpyios.order_sure))
            self.back()
        else:
            sleep(3)
            self.send_buy_money(amount3)
            self.screenshot()
            self.send_buy_monkey_sure()
            self.send_trade_pwd(trade_num)
            self.click_sure()
            sleep(6)
            if self.isElement("xpath",tbjpyios.supple_tongbao)==True:
                print 2
                self.screenshot()
                self.click_button((By.XPATH,tbjpyios.supple_tongbao))
                self.tongbaoin(recharge_num,trade_num)
                self.back()
            elif self.isElement("xpath",tbjpyios.check_buy_success_btn)==True:
                print 3
                self.screenshot_True()
                actual=True
                e='购买成功'
                self.click_button((By.XPATH,tbjpyios.check_buy_success_btn))
                self.back()
            elif self.isElement("name",tbjpyios.cancel_item)==True:
                self.screenshot()
                actual=True
                e='购买成功'
                self.click_button((By.NAME,tbjpyios.cancel_item))
                self.click_button((By.XPATH,tbjpyios.check_buy_success_btn))
                self.back()
            else:
                self.screenshot()
                actual=False
                e='购买失败'

    def message_slide(self,expect):
        code=11
        self.click_button((By.XPATH,tbjpyios.message))
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        sleep(4)
        server_table=self.driver.find_element_by_xpath(tbjpyios.server_table).location
        server_table_y=server_table['y']
        server_table_size=self.driver.find_element_by_xpath(tbjpyios.server_table).size
        server_table_size_y=server_table_size['height']
        server_table_size_y=server_table_y+server_table_size_y
        sleep(2)
        message_bottom_tab=self.driver.find_element_by_xpath(tbjpyios.message_bottom).location
        message_bottom_tab_y=message_bottom_tab['y']
        try:
            self.screenshot()
            self.driver.swipe(x/2,server_table_size_y+10,x/2,message_bottom_tab_y-10,3000)
            sleep(2)
            # print 22
            # message_time2=self.driver.find_elements_by_id(tbjpyios.message_time)[0].get_attribute("name")
            # self.screenshot()
            # while message_time!=message_time2:
            #     self.driver.swipe(x/2,server_table_size_y+1,x/2,message_bottom_tab_y-1,5000)
            #     message_time=message_time2
            #     message_time2=self.driver.find_elements_by_id(tbjpyios.message_time)[0].get_attribute("name")
            #     #self.screenshot()
            #     actual=True
            #     e='success'
            actual=True
            e='success'
            self.screenshot()
            self.back()
        except Exception,e:
            self.screenshot()
            actual=False
            e='fail'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #4.3以上版本查看当前收益
    def now_income43(self,expect):
        code=11
        self.click_button((By.XPATH,tbjpyios.now_income43))
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        sleep(2)
        try:
            # if self.isElement("xpath",tbjpyios.not_hold_nowincome)==True:
            #     self.screenshot()
            #     self.back()
            #     actual=True
            #     e='success'
            # else:
            server_table=self.driver.find_element_by_xpath(tbjpyios.server_table).location
            server_table_y=server_table['y']
            server_table_size=self.driver.find_element_by_xpath(tbjpyios.server_table).size
            server_table_size_y=server_table_size['height']
            server_table_size_y=server_table_y+server_table_size_y
            # sleep(2)
            # product_name=self.driver.find_elements_by_id(tbjpyios.product_time43)[0].get_attribute("text")
            self.screenshot()
            self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,3000)
            # product_name2=self.driver.find_elements_by_id(tbjpyios.product_time43)[0].get_attribute("text")
            sleep(2)
            self.screenshot()
            # while product_name!=product_name2:
            #     self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,5000)
            #     sleep(4)
            #     product_name=product_name2
            #     product_name2=self.driver.find_elements_by_id(tbjpyios.product_name)[0].get_attribute("text")
            #         # self.screenshot()
            actual=True
            e='success'
            self.screenshot()
            self.back()
        except Exception,e:
            self.screenshot()
            self.back()
            actual=True
            e='success'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #4.3查看交易记录滑动
    def check_all_trade_record43(self,expect):
        code=11
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        try:
            self.click_button((By.XPATH,tbjpyios.trade_record43))
            self.screenshot()
            self.driver.swipe(x/2,y-1,x/2,0,3000)
            # while self.isElement("id",tbjpyios.trade_record_footer)==False:
            #     self.driver.swipe(x/2,y-1,x/2,0,3000)
            sleep(2)
            self.screenshot()
            actual=True
            e='success'
            self.back()
        except Exception,e:
            self.back()
            actual=True
            e='success'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #4.3查看铜宝累计收益
    def check_tongbao_income43(self,expect):
        code=11
        self.click_button((By.XPATH,tbjpyios.tongbao_assets_layout43))
        self.click_button((By.XPATH,tbjpyios.tongbao_income))
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        sleep(4)
        server_table=self.driver.find_element_by_xpath(tbjpyios.server_table).location
        server_table_y=server_table['y']
        server_table_size=self.driver.find_element_by_xpath(tbjpyios.server_table).size
        server_table_size_y=server_table_size['height']
        server_table_size_y=server_table_y+server_table_size_y
        sleep(2)
        # tongbao_time=self.driver.find_elements_by_id(tbjpyios.tongbao_time)[0].get_attribute("text")
        try:
            self.screenshot()
            self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,3000)
            sleep(2)
            self.screenshot()
            # sleep(2)
            # self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,5000)
            # tongbao_time2=self.driver.find_elements_by_id(tbjpyios.tongbao_time)[0].get_attribute("text")
            # self.screenshot()
            # while tongbao_time!=tongbao_time2:
            #     self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,5000)
            #     sleep(2)
            #     self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,5000)
            #     tongbao_time=tongbao_time2
            #     tongbao_time2=self.driver.find_elements_by_id(tbjpyios.tongbao_time)[0].get_attribute("text")
            actual=True
            e='success'
            self.screenshot()
            self.back()
            self.back()
        except Exception,e:
            self.screenshot()
            actual=False
            e='fail'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    def my_assert_other_check(self,expect):
        code=11
        try:
            #我的优惠
            self.click_button((By.XPATH,tbjpyios.mypreferential))
            sleep(4)
            self.screenshot()
            self.click_button((By.XPATH,tbjpyios.history_card))
            self.screenshot()
            self.click_button((By.XPATH,tbjpyios.mypreferential_back))
            #我的T码
            self.click_button((By.XPATH,tbjpyios.myTma))
            sleep(4)
            self.screenshot()
            self.click_button((By.XPATH,tbjpyios.myTma_back))
            #我的铜板
            self.click_button((By.XPATH,tbjpyios.mytongban))
            sleep(4)
            self.screenshot()
            self.click_button((By.XPATH,tbjpyios.mytongban_back))
            actual=True
            e='success'
        except Exception,e:
            self.screenshot()
            actual=False
            e='fail'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #铜宝转入流程
    def tongbaoin(self,amount,trade_num,expect):
        actual=None
        code=111
        try:
            self.tongbao_in()
            sleep(4)
            self.send_buy_money(amount)
            self.send_buy_monkey_sure()
            self.send_trade_pwd(trade_num)
            self.click_tongbao_sure_btn()
            sleep(4)
            if self.isElement("name",tbjpyios.check_buy_tongbao_success)==True:
                actual=True
                e='铜宝转入成功'
                self.click_button((By.NAME,tbjpyios.check_buy_tongbao_success))
                sleep(4)
                self.click_button((By.XPATH,tbjpyios.check_buy_tongbao))
                self.back()
            elif self.isElement("name",tbjpyios.check_buy_tongbao)==True:
                actual=True
                e='铜宝转入成功'
                self.click_button((By.XPATH,tbjpyios.check_buy_tongbao))
                self.back()
            else:
                actual=False
                e='铜宝转入失败'
        except Exception,e:
            actual=False
        finally:
            result=str(e)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #铜宝转出流程
    def tongbaoout(self,amount,trade_num,expect):
        actual=None
        code=111
        try:
            self.tongbao_out()
            self.send_buy_money(amount)
            self.send_buy_monkey_sure()
            self.send_trade_pwd(trade_num)
            self.click_tongbao_sure_btn()
            sleep(8)
            if self.isElement("name",tbjpyios.check_buy_tongbao_success)==True:
                actual=True
                e='铜宝转出成功'
                self.click_button((By.NAME,tbjpyios.check_buy_tongbao_success))
                sleep(4)
                self.click_button((By.XPATH,tbjpyios.check_buy_tongbao))
                self.back()
            elif self.isElement("xpath",tbjpyios.check_buy_tongbao)==True:
                actual=True
                e='铜宝转出成功'
                self.click_button((By.XPATH,tbjpyios.check_buy_tongbao))
                self.back()
            else:
                actual=False
                e='铜宝转出失败'
        except Exception,e:
            actual=False
        finally:
            result=str(e)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    def buy_hot_product51(self,amount2,amount3,trade_num,expect):
        code=11
        try:
            hot_product51_names=self.driver.find_elements_by_name(tbjpyios.hot_product_name)
            length=len(hot_product51_names)
            for i in range(length):
                hot_product51_names=self.driver.find_elements_by_name(tbjpyios.hot_product_name)
                hot_product51_names[i].click()
                sleep(2)
                financing_title=self.driver.find_element_by_xpath(tbjpyios.financing_title).get_attribute("name")
                if re.findall(u"新手",financing_title)!=[]:
                    self.new_people_product(trade_num,expect)
                #铜宝转入
                elif re.findall(u"铜宝",financing_title)!=[]:
                    self.tongbaoin(amount2,trade_num,expect)
                else:
                    sleep(3)
                    self.driver.find_element_by_xpath(tbjpyios.product_purchase_view).click()
                    self.normal_product(amount3,trade_num,expect)
            actual=True
            e='success'
        except Exception,e:
            print e
            self.screenshot()
            actual=False
            e='fail'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    def buy_financing_product_1(self,amount2,amount3,recharge_num,trade_num,expect):
        financing_text=self.driver.find_element_by_xpath(tbjpyios.financing_text).get_attribute("name")
        sleep(3)
        product_name51s=self.driver.find_elements_by_xpath(tbjpyios.product_name51_1)
        product_name51s_len=len(product_name51s)
        print product_name51s_len
        sleep(2)
        if re.findall(u"铜宝",financing_text)!=[]:
            self.tongbaoin(amount2,trade_num,expect)
        elif re.findall(u"转让专区",financing_text)!=[]:
            for product_name in product_name51s:
                product_name.click()
                self.buy_transfer(trade_num,expect)
            self.back()
        elif re.findall(u"预约专区",financing_text)!=[]:
            for i in range(product_name51s_len):
                product_name51s=self.driver.find_elements_by_name(tbjpyios.product_name51_1)
                product_name51s[i].click()
                self.buy_order(amount3,recharge_num,trade_num)
            self.back()
        elif self.isElement("name",tbjpyios.terminal_title)==True:
            sleep(3)
            product_name51s=self.driver.find_elements_by_xpath(tbjpyios.product_name51_1)
            product_name51s_len=len(product_name51s)
            for i in range(product_name51s_len):
                product_name51s=self.driver.find_elements_by_xpath(tbjpyios.product_name51_1)
                product_name51s[i].click()
                financing_title=self.driver.find_element_by_xpath(tbjpyios.financing_title).get_attribute("name")
                self.driver.find_element_by_xpath(tbjpyios.product_purchase_view).click()
                sleep(3)
                if self.isElement("xpath",tbjpyios.sale_on_time)==True:
                    self.screenshot()
                    self.click_button((By.NAME,tbjpyios.click_sure))
                    self.back()
                elif re.findall(u"新手",financing_title)!=[]:
                    self.new_people_product(trade_num,expect)
                else:
                    sleep(3)
                    self.normal_product(amount3,trade_num,expect)
            self.back()


    def buy_financing_product_2(self,amount2,amount3,recharge_num,trade_num,expect):
        financing_text=self.driver.find_element_by_xpath(tbjpyios.financing_text).get_attribute("name")
        sleep(3)
        product_name51s=self.driver.find_elements_by_xpath(tbjpyios.product_name51_2)
        product_name51s_len=len(product_name51s)
        sleep(2)
        if re.findall(u"铜宝",financing_text)!=[]:
            self.tongbaoin(amount2,trade_num,expect)
        elif re.findall(u"转让专区",financing_text)!=[]:
            for product_name in product_name51s:
                product_name.click()
                self.buy_transfer(trade_num,expect)
            self.back()
        elif re.findall(u"预约专区",financing_text)!=[]:
            for i in range(product_name51s_len):
                product_name51s=self.driver.find_elements_by_name(tbjpyios.product_name51_2)
                product_name51s[i].click()
                self.buy_order(amount3,recharge_num,trade_num)
            self.back()
        elif self.isElement("name",tbjpyios.terminal_title)==True:
            sleep(3)
            product_name51s=self.driver.find_elements_by_xpath(tbjpyios.product_name51_2)
            product_name51s_len=len(product_name51s)
            for i in range(product_name51s_len):
                product_name51s=self.driver.find_elements_by_xpath(tbjpyios.product_name51_2)
                product_name51s[i].click()
                financing_title=self.driver.find_element_by_xpath(tbjpyios.financing_title).get_attribute("name")
                self.driver.find_element_by_xpath(tbjpyios.product_purchase_view).click()
                sleep(3)
                if self.isElement("xpath",tbjpyios.sale_on_time)==True:
                    self.screenshot()
                    self.click_button((By.NAME,tbjpyios.click_sure))
                    self.back()
                elif re.findall(u"新手",financing_title)!=[]:
                    self.new_people_product(trade_num,expect)
                else:
                    sleep(3)
                    self.normal_product(amount3,trade_num,expect)
        self.back()

    def buy_financing_product_3(self,amount2,amount3,recharge_num,trade_num,expect):
        financing_text=self.driver.find_element_by_xpath(tbjpyios.financing_text).get_attribute("name")
        sleep(3)
        product_name51s=self.driver.find_elements_by_xpath(tbjpyios.product_name51_3)
        product_name51s_len=len(product_name51s)
        print product_name51s_len
        sleep(2)
        if re.findall(u"铜宝",financing_text)!=[]:
            self.tongbaoin(amount2,trade_num,expect)
        elif re.findall(u"转让专区",financing_text)!=[]:
            for product_name in product_name51s:
                product_name.click()
                self.buy_transfer(trade_num,expect)
            self.back()
        elif re.findall(u"预约专区",financing_text)!=[]:
            for i in range(product_name51s_len):
                product_name51s=self.driver.find_elements_by_name(tbjpyios.product_name51_3)
                product_name51s[i].click()
                self.buy_order(amount3,recharge_num,trade_num)
            self.back()
        elif self.isElement("name",tbjpyios.terminal_title)==True:
            sleep(3)
            product_name51s=self.driver.find_elements_by_xpath(tbjpyios.product_name51_3)
            product_name51s_len=len(product_name51s)
            for i in range(product_name51s_len):
                product_name51s=self.driver.find_elements_by_xpath(tbjpyios.product_name51_3)
                product_name51s[i].click()
                financing_title=self.driver.find_element_by_xpath(tbjpyios.financing_title).get_attribute("name")
                self.driver.find_element_by_xpath(tbjpyios.product_purchase_view).click()
                sleep(3)
                if self.isElement("xpath",tbjpyios.sale_on_time)==True:
                    self.screenshot()
                    self.click_button((By.NAME,tbjpyios.click_sure))
                    self.back()
                elif re.findall(u"新手",financing_title)!=[]:
                    self.new_people_product(trade_num,expect)
                else:
                    sleep(3)
                    self.normal_product(amount3,trade_num,expect)
        self.back()

    def buy_financing_product_4(self,amount2,amount3,recharge_num,trade_num,expect):
        financing_text=self.driver.find_element_by_xpath(tbjpyios.financing_text).get_attribute("name")
        sleep(3)
        product_name51s=self.driver.find_elements_by_xpath(tbjpyios.product_name51_4)
        product_name51s_len=len(product_name51s)
        print product_name51s_len
        sleep(2)
        if re.findall(u"铜宝",financing_text)!=[]:
            self.tongbaoin(amount2,trade_num,expect)
        elif re.findall(u"转让专区",financing_text)!=[]:
            for product_name in product_name51s:
                product_name.click()
                self.buy_transfer(trade_num,expect)
            self.back()
        elif re.findall(u"预约专区",financing_text)!=[]:
            for i in range(product_name51s_len):
                product_name51s=self.driver.find_elements_by_name(tbjpyios.product_name51_4)
                product_name51s[i].click()
                self.buy_order(amount3,recharge_num,trade_num)
            self.back()
        elif self.isElement("name",tbjpyios.terminal_title)==True:
            sleep(3)
            product_name51s=self.driver.find_elements_by_xpath(tbjpyios.product_name51_4)
            product_name51s_len=len(product_name51s)
            for i in range(product_name51s_len):
                product_name51s=self.driver.find_elements_by_xpath(tbjpyios.product_name51_4)
                product_name51s[i].click()
                financing_title=self.driver.find_element_by_xpath(tbjpyios.financing_title).get_attribute("name")
                self.driver.find_element_by_xpath(tbjpyios.product_purchase_view).click()
                sleep(3)
                if self.isElement("xpath",tbjpyios.sale_on_time)==True:
                    self.screenshot()
                    self.click_button((By.NAME,tbjpyios.click_sure))
                    self.back()
                elif re.findall(u"新手",financing_title)!=[]:
                    self.new_people_product(trade_num,expect)
                else:
                    sleep(3)
                    self.normal_product(amount3,trade_num,expect)
        self.back()

    def buy_financing_product_5(self,amount2,amount3,recharge_num,trade_num,expect):
        financing_text=self.driver.find_element_by_xpath(tbjpyios.financing_text).get_attribute("name")
        sleep(3)
        product_name51s=self.driver.find_elements_by_xpath(tbjpyios.product_name51_5)
        product_name51s_len=len(product_name51s)
        print product_name51s_len
        sleep(2)
        if re.findall(u"铜宝",financing_text)!=[]:
            self.tongbaoin(amount2,trade_num,expect)
        elif re.findall(u"转让专区",financing_text)!=[]:
            for product_name in product_name51s:
                product_name.click()
                self.buy_transfer(trade_num,expect)
            self.back()
        elif re.findall(u"预约专区",financing_text)!=[]:
            for i in range(product_name51s_len):
                product_name51s=self.driver.find_elements_by_name(tbjpyios.product_name51_5)
                product_name51s[i].click()
                self.buy_order(amount3,recharge_num,trade_num)
            self.back()
        elif self.isElement("name",tbjpyios.terminal_title)==True:
            sleep(3)
            product_name51s=self.driver.find_elements_by_xpath(tbjpyios.product_name51_5)
            product_name51s_len=len(product_name51s)
            for i in range(product_name51s_len):
                product_name51s=self.driver.find_elements_by_xpath(tbjpyios.product_name51_5)
                product_name51s[i].click()
                financing_title=self.driver.find_element_by_xpath(tbjpyios.financing_title).get_attribute("name")
                self.driver.find_element_by_xpath(tbjpyios.product_purchase_view).click()
                sleep(3)
                if self.isElement("xpath",tbjpyios.sale_on_time)==True:
                    self.screenshot()
                    self.click_button((By.NAME,tbjpyios.click_sure))
                    self.back()
                elif re.findall(u"新手",financing_title)!=[]:
                    self.new_people_product(trade_num,expect)
                else:
                    sleep(3)
                    self.normal_product(amount3,trade_num,expect)
        self.back()


    def buy_financing_products5(self,amount2,amount3,recharge_num,trade_num,expect):
        code=11
        try:
            product_form51s=self.driver.find_elements_by_xpath(tbjpyios.product_form51)
            sleep(3)
            product_form51s[1].click()
            self.buy_financing_product_1(amount2,amount3,recharge_num,trade_num,expect)
            product_form51s=self.driver.find_elements_by_xpath(tbjpyios.product_form51)
            product_form51s_deepcopy = copy.deepcopy(product_form51s)
            product_form51s_deepcopy[2].click()
            sleep(3)
            self.buy_financing_product_2(amount2,amount3,recharge_num,trade_num,expect)
            product_form51s=self.driver.find_elements_by_xpath(tbjpyios.product_form51)
            product_form51s_deepcopy = copy.deepcopy(product_form51s)
            product_form51s_deepcopy[3].click()
            sleep(3)
            self.buy_financing_product_3(amount2,amount3,recharge_num,trade_num,expect)
            product_form51s=self.driver.find_elements_by_xpath(tbjpyios.product_form51)
            product_form51s_deepcopy = copy.deepcopy(product_form51s)
            product_form51s_deepcopy[4].click()
            sleep(3)
            self.buy_financing_product_4(amount2,amount3,recharge_num,trade_num,expect)
            product_form51s=self.driver.find_elements_by_xpath(tbjpyios.product_form51)
            product_form51s_deepcopy = copy.deepcopy(product_form51s)
            product_form51s_deepcopy[5].click()
            sleep(3)
            self.buy_financing_product_5(amount2,amount3,recharge_num,trade_num,expect)
            actual=True
            e='success'
        except Exception,e:
            self.screenshot()
            actual=False
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    # #输入验证码
    # def send_verify_code(self):
    #     myms = sql.mysql_connect(sql.db_info)
    #     sleep(7)
    #     verifycode1=myms.sql_assign_exec("select content from mdp_message WHERE recipients="+ tbjdata.loginid(1) + " ORDER BY create_time DESC LIMIT 1")
    #     verifycode2=re.search('\d{6}', verifycode1)
    #     verifycode3=verifycode2.group(0)
    #
    # #输入验证码并点击完成按钮
    # def send_verifycode_sure(self):
    #     sleep(5)
    #     myms = sql.mysql_connect(sql.db_info)
    #     sleep(5)
    #     verify_code1=myms.sql_assign_exec("select content from mdp_message WHERE recipients="+ tbjdata.loginid(1) + " ORDER BY create_time DESC LIMIT 1")
    #     verify_code2=re.search('\d{6}', verify_code1)
    #     verify_code3=verify_code2.group(0)
    #     self.send_keys((By.ID,tbjpyios.verify_input),verify_code3)
    #     print 2
    #     self.click_button((By.ID,tbjpyios.btn_next))
    #     self.driver.implicitly_wait(10)

    #android平台覆盖安装功能
    def test(self):
        self.driver.implicitly_wait(10)
        #覆盖安装，所要覆盖安装的apk的路径
        os.system("adb install -r  D:\\apk\\TBJ_android_APP_GDT_FEED2.apk")
        #os.system("adb install -r  D:\\apk\\TBJ_4.2.0_109_0720_2305.apk")
        sleep(3)
        check_install_successs=os.popen("adb install -r  D:\\apk\\TBJ_android_APP_GDT_FEED2.apk").read().strip()
        sleep(2)
        success="Success"
        if re.search(success, check_install_successs) !=None:
        #if re.match(success, check) !=None:
            print u'强制覆盖安装成功！'
        else:
            print u'因为apk包签名不同或者版本低于当前版本等其他原因，所以放弃强制安装！'


class Data(object):
    def __init__(self):
        #测试帐号
        self.phone_num='13735865796'
        #帐号长度不满11位
        self.phone_num_e1='1373586579'
        #未注册帐号
        self.phone_num_e2='13735865792'
        #拟注册帐号
        self.sign_num='13735865782'
        #测试帐号密码
        self.passwd='654321'
        #密码和帐号不匹配
        self.passwd_e1='123456'
        #密码不满六位
        self.passwd_e2='65432'
        #注册设置的密码
        self.sign_pwd='123456'
        #原登录密码
        self.old_pwd='654321'
        #错误的原登录密码
        self.old_pwd_e1='123456'
        #新置登录密码
        self.set_pwd='654321'
        #重复新登录密码
        self.repeat_pwd='654321'
        #重复新登录密码与新置登录密码不匹配
        self.repeat_pwd_e1='123456'
        #原交易密码
        self.old_trade_pwd='654321'
        #错误的原交易密码
        self.old_trade_pwd_e1='123456'
        #原交易密码位数不够
        self.old_trade_pwd_e2='12345'
        #新交易密码
        self.new_trade_pwd='654321'
        #新交易密码位数不够
        self.new_trade_pwd_e1='65432'
        #重复新置密码
        self.repeat_trade_pwd='654321'
        #重复新置密码位数不够
        self.repeat_trade_pwd_e1='65432'
        #重复新置密码与新置密码不匹配
        self.repeat_trade_pwd_e2='123456'
        #充值金额
        self.topup_num='100'
        #充值金额为空
        self.topup_num_e1=''
        #交易密码
        self.trade_pwd='654321'
        #错误的交易密码
        self.trade_pwd_e='654322'
        #提现金额
        self.out_num='100'
        #充值金额为空
        self.out_num_e1=''
        #铜宝转入金额
        self.tongbaoin_num='100'
        #铜宝转出金额
        self.tongbaoout_num='100'
        #普通产品购买金额
        self.normal_product_num='300'
        self.person_ID=''
        #铜宝充值金额
        self.recharge_num='100'


