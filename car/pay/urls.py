# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

app_name = 'pay'

urlpatterns = [

	# 首页
	url(r'^$', views.index, name='index'),
	
	# 登录页面
	url(r'^login/$', views.login, name='login'),
	# 验证登录
	url(r'^valid_user/$', views.valid_user, name='valid_user'),
	# 首页
	url(r'^repos/$', views.home, name='home'),
	# 订单
	url(r'^order/$', views.order, name='order'),
	# 管理员 订单审核
	url(r'^order_verify/$', views.order_verify, name='order_verify'),
	url(r'^orderinfo/$', views.orderinfo, name='orderinfo'),
	# 物流信息添加
	url(r'^verify_smt/$', views.verify_smt, name='verify_smt'),
	# 新增订单
	url(r'^new_order/$', views.new_order, name='new_order'),
	# 新订单保存
	url(r'^add_order/$', views.add_order, name='add_order'),
	# 订单详情
	url(r'^order_detail/$', views.order_detail, name='order_detail'),

	# 订单入库管理
	url(r'^ware_confirm/$', views.ware_confirm, name='ware_confirm'),
	# 订单确认管理
	url(r'^order_confirm/$', views.order_confirm, name='order_confirm'),
	url(r'^confirmed/$', views.confirmed, name='confirmed'),
	# 订单删除
	url(r'^order_delete/$', views.order_delete, name='order_delete'),

	# 销售
	url(r'^sale/$', views.sale, name='sale'),
	# 新增销售单
	url(r'^add_sale/$', views.add_sale, name='add_sale'),
	# 销售单保存
	url(r'^upload/$', views.upload, name='upload'),
	# 销售单审核
	url(r'^order_check/$', views.order_check, name='order_check'),
	url(r'^sale_confirm/$', views.sale_confirm, name='sale_confirm'),
	url(r'^sale_verify/$', views.sale_verify, name='sale_verify'),
	# 销售顾问管理
	url(r'^sale_assis/$', views.sale_assis, name='sale_assis'),
	url(r'^assis_process/$', views.assis_process, name='assis_process'),
	# 销售顾问修改
	url(r'^assis_change/$', views.assis_change, name='assis_change'),
	# 销售顾问修改处理
	url(r'^assis_change_process/$', views.assis_change_process, name='assis_change_process'),
	# 保险文件删除记录
	url(r'^safefile_delete/$', views.safefile_delete, name='safefile_delete'),
	# 销售顾问删除
	url(r'^assis_delete/$', views.assis_delete, name='assis_delete'),
	# 销售信息修改
	url(r'^sale_edit/$', views.sale_edit, name='sale_edit'),
	# 销售信息修改保存
	url(r'^sale_edit_save/$', views.sale_edit_save, name='sale_edit_save'),
	# 打印页面
	url(r'^print_tpl/$', views.print_tpl, name='print_tpl'),
	# Modal 查看信息
	url(r'^modal_show/$', views.modal_show, name='modal_show'),
	# 验证client返回数目
	url(r'^valid_client/$', views.valid_client, name='valid_client'),

	# 导出销售单信息
	url(r'^export/$', views.export, name='export'),

	# 退出
	url(r'^logout/$', views.logout_view, name='logout_view'),
	# 用户管理
	url(r'^users/$', views.users, name='users'),
	# 用户添加
	url(r'^add_user/$', views.add_user, name='add_user'),
	# 用户列表
	url(r'^user_manage/$', views.user_manage, name='user_manage'),
	# 用户删除
	url(r'^user_delete/$', views.user_delete, name='user_delete'),
	# 给用户修改密码
	url(r'^changepass/$', views.changepass, name='changepass'),
	# 密码修改
	url(r'^change_pw/$', views.change_pw, name='change_pw'),
	url(r'^change/$', views.change, name='change'),

	# 大保单号码管理
	url(r'^care_number/$', views.care_number, name='care_number'),
	# 大保单保存更新
	url(r'^bcare_process/$', views.bcare_process, name='bcare_process'),
	# 销售信息删除
	url(r'^saleinfo_delete/$', views.saleinfo_delete, name='saleinfo_delete'),
	# 产品新增
	url(r'^product_manage/$', views.product_manage, name='product_manage'),
	# 主辅产品新增
	url(r'^add_first/$', views.add_first, name='add_first'),
	url(r'^add_second/$', views.add_second, name='add_second'),
	# 主辅产品删除
	url(r'^first_del/$', views.first_del, name='first_del'),
	url(r'^second_del/$', views.second_del, name='second_del'),

]