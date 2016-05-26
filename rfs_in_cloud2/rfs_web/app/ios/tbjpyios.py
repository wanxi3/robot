# -*- coding: utf-8 -*-
#第一次启动时候的欢迎界面的操作
#登录/注册
reg_login=''
#立即体验
into_main=''

#登陆模块
#更多模块按钮
more='更多'
#我的账户按钮
myaccount='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[1]'
#5.0版本我的账户，点击登录
myaccount5='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIAButton[1]'
#手机号
phoneId='//UIAApplication[1]/UIAWindow[1]/UIATextField[1]'
#下一步
next='下一步'
#密码
phonepwd='//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]'
#登陆确定按钮
click_login='确定'
#退出登录
click_logout='退出'
#5.0版本设置按钮
click_set='设置'

#注册功能
#输入验证码
verify_input='//UIAApplication[1]/UIAWindow[1]/UIATextField[1]'
#验证码重发按钮
receive_verifi_btn=''
#设置登陆密码
set_login_password='//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]'
#确定按钮
sure_btn='确 定'
#铜宝确定按钮
tongbao_sure_btn='确定'

#密码管理
#密码管理入口
rl_pwd_manager='密码管理'
#修改登录密码
change_login_pwd_layout='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[1]'
#旧密码
old_password_input='//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]'
#新密码
new_password_input='//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[2]'
#确定新密码''
confilm_new_password='//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[3]'
#修改按钮
modify_login_pwd='完成'
#修改密码确定按钮
pwdsure='确定'
#设置交易密码，完成按钮
trans_pwd_succ='完成'
#修改交易密码
rlyt_update_trans_pwd='修改交易密码'
#修改交易密码-完成
complete_btn='完成'
#修改交易密码，两次密码输入不一致的弹出框
pwd_dialog_message_text=''
#找回交易密码-按钮
rlyt_find_trade_pwd='找回交易密码'
#找回交易密码-姓名
full_name_value='//UIAApplication[1]/UIAWindow[1]/UIATextField[1]'
#找回交易密码-身份证
input_value='//UIAApplication[1]/UIAWindow[1]/UIATextField[2]'
#找回交易密码-下一步
next_btn='下一步'
#校验-下一步
btn_next='下一步'
#手势解锁
switcher_checkbox='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[4]/UIASwitch[1]'
#创建手势解锁
btn_start_set_pattern_lock='创建手势密码'
#手势解锁-标题
title='//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAStaticText[1]'

#查看用户个人信息
#用户个人信息按钮
rl_user_info='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]'
#校验用户个人信息:账户，实名认证，身份认证，投资风格
user_name='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[2]'
full_name='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[2]/UIAStaticText[2]'
id_card='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[3]/UIAStaticText[2]'
tv_risk_level_value='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[4]/UIAStaticText[2]'
#返回按钮
back2='返回'
back3='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[1]'

#账户余额一系列操作
#4.3-5.0版本账户余额入口
balance_entry5='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[3]/UIAStaticText[1]'
#账户余额模块按钮
rl_account_balance='账户余额'
#余额数值
rl_payment_details='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[1]'
#充值按钮
rl_recharge='充值'
#输入充值金额
czje="//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIATextField[1]"
#提交
recharge_submit="//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAButton[1]"
#充值处的提示，请输入正确充值金额
send_true_monkey="请输入正确充值金额"
#充值处的提示，请选择银行卡
recharge_choose_bankcard="//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[9]"
#充值处的提示，超过该卡累计支付金额
remind_exceed_monkey="//android.view.View[contains(@content-desc,'超过该卡日累计支付金额')]"
#该产品暂不支持购买的提示
product_not_support_buy="//android.view.View[contains(@content-desc,'该产品暂不支持购买')]"
#点击充值或者转出成功的“确定”按钮
click_money_success="//android.view.View/android.widget.Button[@content-desc='确 定']"
#余额转出
rl_balance_out='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[4]/UIAStaticText[1]'
#转出金额输入
zcje='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIATextField[1]'
#转出金额输入-提交
submit='提 交'
#提交的xpath
submit_xpath='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAButton[1]'
#校验金额充值/转出成功的按钮
check_money_success="//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAButton[2]"
money_success_btn='确 定'
check_money_fail=''
#请输入铜板街交易密码，的确定按钮
click_sure='确定'
#账户余额显示
balance=''
#代扣测试
pay_prompt='代扣测试'


#5.0理财产品，铜宝按钮
financing_products_tb='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]'

#回款路径
#回款路径未设置文本
label="//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]/UIAScrollView[1]/UIAStaticText[2]"
#回款路径模块按钮
return_path_label='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[4]'
#第一个银行账户
first_bank='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[2]/UIAStaticText[1]'
#弹出框的确定以及取消按钮
return_path_label_sure='确定'
return_path_label_cancel='取消'

#银行卡管理
#提示的添加银行卡弹出框
add_bank_popup='//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]/UIACollectionView[1]/UIACollectionCell[2]/UIAButton[1]'
#银行卡按钮
rl_bankcard_manager='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[2]'
#添加银行卡
rlyt_add_bankCard='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]'
#添加银行卡-姓名
card_name='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIATextField[1]'
#添加银行卡-身份证
card_personid='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIATextField[2]'
#选择银行
choose_bank='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[9]'
#选择银行 中国银行
choose_one_bank="//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[18]"
#选择银行 建设银行
xzyhjs='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[17]'
#银行卡号
bank_id='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIATextField[3]'
#手机号
iphone_num="//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIATextField[4]"
#绑定
binding="//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAButton[1]"
#输入验证码
send_verify='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIATextField[5]'
#完成按钮
success_btn='完成'
#提示，交易密码错误
submit_tradepwd_error="//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[11]"

#精品推荐购买产品
#精品页的产品
ll_top_content='//UIAApplication[1]/UIAWindow[1]/UIATabBar[1]/UIAButton[1]'
#精品推荐购买产品模块按钮
jpmkbtn='转入'
#精品推荐标题
hot_product_title='精品推荐'
#点击精品推荐页面的购买按钮
hot_product_buy='//UIAApplication[1]/UIAWindow[1]/UIAButton[1]'
#购买按钮
hot_product_buy_btn='购买'
#输入金额
hot_product_buy_money='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIATextField[1]'
#输入金额-提交
hot_product_buy_money_sure='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAButton[1]'
#选择付款方式
payment_method='使用账户余额付款'
#银行列表，选择第一个银行
bank_list='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[14]'
#银行列表的返回按钮
bankback_btn='返回'
#选择付款方式上的关闭按钮
close='//android.widget.RelativeLayout[@index=0]/android.widget.ImageView'
#返回
back='//android.view.View[@index=0]/android.view.View[@index=0]'
#购买成功后的确定
true='确定'
#确定
truetwo='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAButton[2]'
#失败处理1
#fail1='//android.view.View[@index=0]/android.view.View[@index=18]'
fail1='//android.view.View[@index=0]/android.view.View[@index=12]'
#失败处理2
fail2='//android.view.View[@index=0]/android.view.View[@index=0]/android.view.View[@index=0]'
#计算器按钮
calc_btn='calcImg'
#输入计算数值
purchase_amount_edit='//UIAApplication[1]/UIAWindow[1]/UIATextField[1]'
#计算
calc_earnings_btn='//UIAApplication[1]/UIAWindow[1]/UIAButton[4]'
#关闭计算器name
gb='//UIAApplication[1]/UIAWindow[1]/UIAButton[3]'
#金额不够时，弹出框的确定按钮
bgqd='//android.view.View[@index=0]/android.view.View[@index=12]'
#购买成功后的确定按钮
cgqd="//android.widget.Button[contain(@content-desc,'确定')]"

#我的资产
#我的资产模块按钮
myasset='//UIAApplication[1]/UIAWindow[1]/UIATabBar[1]/UIAButton[3]'
#信息中心按钮
message='//UIAApplication[1]/UIAWindow[1]/UIAImage[1]/UIAButton[1]'
#返回
back1='返回'
#资产页面校验
check_myassert='总资产'
#取消
cancel='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[1]'
#提示框的确定
sure='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[12]'

#产品预告
cpyg='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[3]'

#关于铜板街
#关于铜板街-进入
rlyt_about_tbj='关于铜板街'
#各个id
ljwm='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]'
server='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[2]'
pj='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[3]'
attention='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[4]'

#忘记密码后，找回密码
#点击忘记密码
forget_password='忘记密码'
#找回密码，下一步
click_back_pwd_nextbtn='下一步'

#个人信息
#投资风格
tzfg='com.tongbanjie.android:id/rlyt_risk_survey'
#分享按钮
fx='com.tongbanjie.android:id/iv_right_option'
#分享到微信平台按钮
share_logo_weixin='//UIAApplication[1]/UIAWindow[1]/UIAButton[1]'
#分享到微信朋友圈按钮
share_logo_wxfriends='//UIAApplication[1]/UIAWindow[1]/UIAButton[2]'
#朋友圈分享发送
fs='com.tencent.mm:id/ee'

#输入交易密码，确定
jixu='确定'

#回款路径错误输入交易密码，返回按钮
rl_return_path='com.tongbanjie.android:id/rl_return_path'

#理财产品
tab_financing_products='//UIAApplication[1]/UIAWindow[1]/UIATabBar[1]/UIAButton[2]'
#随便选择的一个理财产品
frist='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[3]'
#理财产品购买
lccpbuy='//UIAApplication[1]/UIAWindow[1]/UIAButton[2]'


#校验登录失败
check_login_fail='登录密码'
#校验注册失败
sign_fail_check='返回'
#校验修改登录密码，原始密码错误
first_pwd_error='原始密码错误'
#校验修改登录密码不能为空
check_modify_pwd_not_null='密码不能空'
#校验修改密码，两次不一样
check_modify_pwd_not_same='两次输入的新密码不一样'
#校验修改登录密码成功
check_pwd_success='修改密码成功'
#提示：用户名与密码不匹配
pwd_notsuite_acount='用户名与密码不匹配'
#弹出框，确定按钮
click_right="//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[contains(@name,'确定')]"
#确定按钮
pwd_confirm_btn='//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[1]'
#校验进入注册模块
check_sign='验证码'
#铜板街安全键盘
safe_keyboard='铜板街安全键盘'
#代扣失败
withholding_defeat="//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[contains(@name,'代扣失败')]"
#网络不给力，请稍后重试
net_ungelivable="//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]/UIAScrollView[1]/UIAStaticText[contains(@name,'网络不给力')]"
#校验输入交易密码错误
check_first_pwd_error="//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]/UIAScrollView[1]/UIAStaticText[2]"
#校验两次密码输入不一致，请重新输入的弹出框
check_trade_pwd_not_same="两次密码输入不一致 请重新输入"
#校验修改交易密码成功
check_modify_trade_pwd='修改登录密码'
#校验找回交易密码成功
check_back_trade_pwd='修改登录密码'
#校验账户余额一充值成功
check_recharge_success='确 定'
#校验找回密码成功
check_find_pwd='我的账户'
#校验购买成功
check_buy_success_btn='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAButton[2]'
#校验铜宝转入成功
check_buy_tongbao_success='44'
#校验铜宝转出成功
check_buy_tongbao='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAButton[2]'
#我的资产-铜宝入口
myasset_tongbao='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[2]/UIAButton[2]'
#校验新手产品购买成功
check_newbuy_success_btn='确定'
#设置新用户交易密码是否成功功能
check_set_newpeople_tradepwd_fail='铜板街安全键盘'
#购买产品没有跳转到登陆页面
buy_check_login_page_no=""
#购买铜宝，未登录，点击登录
buy_tongbao_login_check='账户余额自动转入铜宝，随时产生收益'
#购买铜宝，点击登录
buy_tongbao_login='点击登录'
#跳转到登陆页面按钮
login_page_check=''
#新手购买 定死的金额
newpeople_buy_check=""
#理财产品的label
financing_label=''
#校验修改交易密码页面，请输入原交易密码。还停留在该页面
check_old_tradepwd='请输入原交易密码验证身份'
#校验修改交易密码页面，请重新设置交易密码。还停留在该页面
check_set_tradepwd='请重新设置交易密码'
#校验修改交易密码页面，请重新设置交易密码。还停留在该页面
check_repeat_set_tradepwd='请重复输入交易密码'
#校验输入原交易密码错误的弹出框
check_old_tradepwd_error=""
#校验重复输入交易密码错误的弹出框
check_repeat_set_tradepwd_error='两次密码输入不一致 请重新输入'
#校验超过该卡累计支付金额提示框
check_exceed_total_money=""
#校验交易密码错误，请重新输入的提示框
check_trade_pwd_error=""
#校验充值失败，请联系客服的提示
check_recharge_fail=""
#校验精品推荐页，购买的提示
check_recommendation_reminder=''
#交易密码错误
tradepwd_error="//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[13]"
#提示的确定按钮
reminder_sure_button=''
#理财产品-产品预告的title定位
product_advance_title=''
#理财产品-升级测试的title定位
product_upgrade_title=""
#转让购买
transfer_buy="//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[6]/UIAButton[contains(@name,'立即购买')]"
#转让实付
transfer_pay="//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAButton[contains(@name,'实付')]"

#开始赚钱
earn_monkey='开始赚钱'

#铜宝转入
tongbao_in='转入'
#铜宝转出
tongbao_out='转出'

#5.3更多-个人资料
login51='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIAButton[1]'

#精品推荐
hot_product='//UIAApplication[1]/UIAWindow[1]/UIATabBar[1]/UIAButton[1]'
#投资风格
risk='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[1]'
#邀请好友
customer_service='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[2]/UIAStaticText[1]'
#设置
settings='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[5]/UIAStaticText[1]'
#了解我们
about_tbj='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[6]/UIAStaticText[1]'
#5.3版本，精品推荐的注册/登录按钮
hot_product_login='注册/登录'

banner='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIAScrollView[1]/UIAImage[1]'
hot_product_name='理财期限'
financing_title='//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAStaticText[1]'
product_purchase_view='//UIAApplication[1]/UIAWindow[1]/UIAButton[2]'
cancel_item='cancel'

finance_lable='//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAImage[1]'

tongbao_52='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]'

product_form51='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell'

terminal_title='默认'

financing_text='//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAStaticText[1]'

sort_menu_default='//UIAApplication[1]/UIAWindow[1]/UIAStaticText[1]'

product_name51_1='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell'
product_name51_2='//UIAApplication[1]/UIAWindow[1]/UIATableView[2]/UIATableCell'
product_name51_3='//UIAApplication[1]/UIAWindow[1]/UIATableView[3]/UIATableCell'
product_name51_4='//UIAApplication[1]/UIAWindow[1]/UIATableView[4]/UIATableCell'
product_name51_5='//UIAApplication[1]/UIAWindow[1]/UIATableView[5]/UIATableCell'


#信息中心-服务中心
server_table='//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAImage[1]'
#信息中心-活动攻略
message_bottom='//UIAApplication[1]/UIAWindow[1]/UIAButton[1]'
message_time='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell/UIAStaticText[2]'
#当日收益
now_income43='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[4]'

trade_record43='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[8]'

tongbao_assets_layout43='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[2]/UIAButton[2]'
tongbao_income='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[3]'

#我的资产页面，我的优惠
mypreferential='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[5]'
#我的资产页面，我的T码
myTma='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[6]'
#我的资产页面，我的铜板
mytongban='//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[7]'
#历史卡劵
history_card='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIALink[2]/UIAStaticText[1]'

#我的优惠的返回按钮
mypreferential_back='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[1]'
#我的T码的返回按钮
myTma_back='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[3]'
#我的铜板的返回按钮
mytongban_back='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[1]'

#新手购买提交按钮
newpeople_buy_commit='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAButton[1]'
#预计开售
sale_on_time="//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]/UIAScrollView[1]/UIAStaticText[contains(@name,'准时开售')]"
#敬请期待
continued="//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]/UIAScrollView[1]/UIAStaticText[contains(@name,'敬请期待')]"
#购买金额需多少元起
money_check='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[15]'

#预约的提示
order_submit='//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]/UIAScrollView[1]/UIAStaticText[2]'
#预约的提示-确定按钮
order_sure='//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]/UIACollectionView[1]/UIACollectionCell[1]'

#我的资产-取消
myasset_cancel='//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]/UIACollectionView[1]/UIACollectionCell[1]'

