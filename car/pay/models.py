# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.contrib import admin

# Create your models here.
'''
# 管理组用户表
class User(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)

	def __str__(self):
		return self.username
'''

# 用户表
# Group分类，库管和销售
class Users(models.Model):
	username = models.CharField(max_length=128)
	password = models.CharField(max_length=128)
	group = models.CharField(max_length=50)
	area = models.CharField(max_length=50)
	note = models.CharField(max_length=128)

	def __str__(self):
		return self.username

# 销售顾问管理表
class Adviser(models.Model):
	username = models.CharField(max_length=50)
	idnumber = models.CharField(max_length=50)
	mobile = models.CharField(max_length=50)
	area = models.ForeignKey(Users)

	def __str__(self):
		return self.username


# 订单表
class Orders(models.Model):
	onumber = models.CharField(max_length=50)
	company = models.CharField(max_length=50)
	client =  models.CharField(max_length=50)
	phone = models.CharField(max_length=50, default='0')
	mobile = models.CharField(max_length=50, default='0')
	repos = models.CharField(max_length=50)
	transport = models.CharField(max_length=50)
	source = models.CharField(max_length=50)
	note = models.CharField(max_length=128, null=True)
	orderinfo = models.CharField(max_length=128, default='')
	# 订单用户外键用户
	applicant = models.ForeignKey(Users)
	pubtime = models.DateTimeField(auto_now_add=True)
	# 成功为0 失败为1
	verify_status = models.IntegerField(default=1)
	send_status = models.IntegerField(default=1)
	# 确认状态 成功为0 失败为1
	confirm = models.IntegerField(default=1)

	def __str__(self):
		return self.onumber


# 订单发货信息表
class OrdersInfo(models.Model):
	order = models.ForeignKey(Orders)
	sentnumber = models.CharField(max_length=50)
	send_date = models.CharField(max_length=50)
	deliverman = models.CharField(max_length=50)
	deliverltd = models.CharField(max_length=50)
	delivernumber = models.CharField(max_length=50)
	# 审核状态 确认为0 未确认为1
	verify = models.IntegerField(default=1)


# 投保用户表
class Clients(models.Model):
	fours = models.CharField(max_length=50, blank=True, null=True)
	client_type = models.CharField(max_length=50)
	client_name = models.CharField(max_length=50)
	identity_type = models.CharField(max_length=50)
	identity_nu = models.CharField(max_length=128)
	# 联系地址分段
	prov = models.CharField(max_length=50, null=True, blank=True)
	city = models.CharField(max_length=50, null=True, blank=True)
	address = models.CharField(max_length=128)
	mobile = models.CharField(max_length=50, null=True, blank=True)

# 大保单号码
class CareNu(models.Model):
	b_care_number = models.CharField(max_length=50, blank=True, null=True)

# 投保信息
class Safe(models.Model):
	# 管理者
	writer = models.CharField(max_length=50, blank=True, null=True)
	# 大保单号码
	b_care_number = models.ForeignKey(CareNu, blank=True, null=True)
	# 小保单号
	care_number = models.CharField(max_length=50, blank=True, null=True)
	# POS机交易码
	pos_number = models.CharField(max_length=50, blank=True, null=True)
	client = models.ForeignKey(Clients)
	# 销售日期
	sale_date = models.DateTimeField(auto_now=True)
	# 贷款金融机构
	financial = models.CharField(max_length=50, blank=True, null=True)
	# 产品名称
	product_name = models.CharField(max_length=50)
	# 主设备名称
	equip_name = models.CharField(max_length=50)
	# 辅设备名称
	second_equip_name = models.CharField(max_length=50, blank=True, null=True)
	# 车品牌
	car_name = models.CharField(max_length=50)
	# 车型号
	car_type = models.CharField(max_length=50, blank=True, null=True)
	# 初始购车日期
	buycar_date = models.CharField(max_length=50)
	# 购车发票价格
	car_price = models.CharField(max_length=50, blank=True, null=True)
	# 车管家价格
	price = models.CharField(max_length=50)
	# 车架号
	vin = models.CharField(max_length=128)
	# 发动机号码
	car_number = models.CharField(max_length=50, blank=True, null=True)
	# 销售顾问
	sale_man = models.CharField(max_length=50, blank=True, null=True)
	# 购车类型
	buy_type = models.CharField(max_length=50)
	# 第一受益人
	first_benefit = models.CharField(max_length=50)
	# 审核状态
	check_status = models.IntegerField(default=1)
	# 销售状态
	sale_status = models.IntegerField(default=1)
	# 安装状态
	install_status = models.IntegerField(default=1)

# 测试车架号
class Vin(models.Model):
	vin = models.CharField(max_length=128, null=True)


# 保存文件目录生成
def user_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	return 'vin_{0}/{1}'.format(instance.vin.vin, filename)

# 测试上传文件
class Uploaded(models.Model):
	#files = models.FileField(upload_to='documents/%Y/%m/%d', blank=True, null=True)
	vin = models.ForeignKey(Safe)
	files = models.FileField(upload_to=user_directory_path, blank=True, null=True)

admin.site.register(Users)

