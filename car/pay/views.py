# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import logout

from django.template import loader

from django import forms
from django.views.decorators.csrf import csrf_exempt
# 异常
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# 数据库
from pay.models import Users, Orders, Clients, OrdersInfo, Safe, Uploaded, Vin, Adviser, CareNu

# 数据分页
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

# Libs
import json
import datetime
import urllib
import xlsxwriter
try:
	import cStringIO as StringIO
except ImportError:
	import StringIO


# Create your views here.
# 登录页面
class UserForm(forms.Form):
	username = forms.CharField(label = '用户名: ', max_length = 100, widget = forms.TextInput(attrs = {'class': 'span12'}))
	password = forms.CharField(label = '密码: ', widget = forms.PasswordInput(attrs = {'class' : 'span12'}))

#_ 登录func
def login(request):
	if request.method == 'POST':
		uf = UserForm(request.POST) 
		if uf.is_valid():
			#_ Get username password
			username = uf.cleaned_data['username']
			#_ Get username in session
			request.session['username'] = username
			password = uf.cleaned_data['password']

			#_ Match the db
			try:
				user = Users.objects.get(username__exact = username, password__exact = password)
				if user.group != 'sale':
					return HttpResponseRedirect('/order/')
				elif user.group == 'sale':
					return HttpResponseRedirect('/sale')
				else:
					return HttpResponseRedirect('/login')
			except ObjectDoesNotExist:
				return HttpResponseRedirect('/login')
		else:
			return HttpResponseRedirect('/login')
	else:
		uf = UserForm()
	return render(request, 'pay/sign.html', {'uf' : uf})


# 验证用户密码
@csrf_exempt
def valid_user(request):
	if request.method == 'POST':
		username = request.POST.get("username")
		password = request.POST.get("password")
		try:
			user = Users.objects.get(username__exact = username, password__exact = password)
			return HttpResponse(json.dumps({"msg":"ok"}))
		except ObjectDoesNotExist:
			return HttpResponse(json.dumps({"msg": "failed"}))


# 权限列表
permissions = ['admin', 'repo', 'sale']
# 判断权限
def permission_check(username):
	u = Users.objects.get(username = username)
	role = u.group
	return role

# index
def index(request):
	return HttpResponseRedirect('/login/')


# 仓库管理页面
def home(request):
	#_ 获取user的session
	username = request.session.get('username')
	if username:
		return render(request, 'pay/home.html', {'username': username},
								context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect('/login')


# 查询条件
def getCondition(data={}):
	kwargs = {}
	for (k, v) in data.items():
		if v is not None and v != u'' and v != 'None' and v!= '':
			kwargs[k] = v
	return kwargs

# 订单查询
def order(request):
	username = request.session.get('username')
	if username:
		if request.method == 'GET':
			role = permission_check(username)
			if role == 'admin':
				# 搜索条件
				onumber = request.GET.get('onumber')
				status = request.GET.get('status')
				# 时间范围
				datefrom = request.GET.get('from')
				start_date = request.GET.get('from')
				dateto = request.GET.get('to')
				end_date = request.GET.get('to')
				if datefrom is not None and datefrom != '' and datefrom != 'None':
					datefrom = datetime.datetime.strptime(datefrom, '%Y-%m-%d')
				if dateto is not None and dateto != '' and dateto != 'None':
					dateto = datetime.datetime.strptime(dateto, '%Y-%m-%d')

				searchCondition = {'onumber__icontains': onumber, 'send_status__icontains': status, 'pubtime__gt': datefrom, 'pubtime__lt': dateto}
				kwargs = getCondition(searchCondition)
				query = {'status': status, 'onumber': onumber, 'from': start_date, 'to': end_date}
				# 分页设置
				limit = 10
				order_list = Orders.objects.filter(**kwargs).order_by('-id')
				paginator = Paginator(order_list, limit)
				# 获取页数
				page = request.GET.get('page')
				try:
					orderlist = paginator.page(page)
				except PageNotAnInteger:
					orderlist = paginator.page(1)
				except EmptyPage:
					orderlist = paginator.page(paginator.num_pages)
				query = urllib.urlencode(query)

				return render(request, 'pay/order.html',
						{'orders': orderlist,
						'username': username,
						'query': query,
						'role': role},
						context_instance=RequestContext(request))
			elif role == 'repo':
				u = Users.objects.get(username=username)
				onumber = request.GET.get('onumber')
				status = request.GET.get('status')
				# 时间范围
				datefrom = request.GET.get('from')
				dateto = request.GET.get('to')
				start_date = request.GET.get('from')
				end_date = request.GET.get('to')
				if datefrom is not None and datefrom != '' and datefrom != 'None':
					datefrom = datetime.datetime.strptime(datefrom, '%Y-%m-%d')
				if dateto is not None and dateto != '' and dateto != 'None':
					dateto = datetime.datetime.strptime(dateto, '%Y-%m-%d')
				searchCondition = {'onumber__icontains': onumber, 'send_status__icontains': status, 'pubtime__gt': datefrom, 'pubtime__lt': dateto}
				kwargs = getCondition(searchCondition)
				query = {'status': status, 'onumber': onumber, 'from': start_date, 'to': end_date}
				query = urllib.urlencode(query)
				# 分页
				limit = 10
				order_list = Orders.objects.filter(**kwargs).filter(applicant__area__contains=u.area).order_by('-id')
				paginator = Paginator(order_list, limit)
				# 获取页数
				page = request.GET.get('page')
				try:
					orderlist = paginator.page(page)
				except PageNotAnInteger:
					orderlist = paginator.page(1)
				except EmptyPage:
					orderlist = paginator.page(paginator.num_pages)

				return render(request, 'pay/order.html',
							{'orders': orderlist,
							'username': username,
							'query': query},
							context_instance=RequestContext(request))
			else:
				return render(request, 'pay/403.html', {'username': username},
									context_instance=RequestContext(request))

	else:
		return HttpResponseRedirect('/login')

# 超级管理员审核订单
def order_verify(request):
	username = request.session.get('username')
	if username:
		role = permission_check(username)
		if role == 'admin':
			order_list = Orders.objects.filter(verify_status=1).order_by('-id')
			# 分页设置
			limit = 10
			paginator = Paginator(order_list, limit)
			page = request.GET.get('page')
			try:
				orderlist = paginator.page(page)
			except PageNotAnInteger:
				orderlist = paginator.page(1)
			except EmptyPage:
				orderlist = paginator.page(paginator.num_pages)
			return render(request, 'pay/orderverify.html',
							{'username': username,
							'orders': orderlist,
							'role': role},
							context_instance=RequestContext(request))
		else:
			return render(request, 'pay/403.html', {'username': username},
						context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login')


# 订单审核详情
def orderinfo(request):
	username = request.session.get('username')
	if username:
		role = permission_check(username)
		if role == 'admin':
			if request.method == 'GET':
				info = request.GET.get('info')
				order = Orders.objects.get(onumber=info)
				area = Orders.objects.get(onumber=info).applicant.area
				return render(request, 'pay/orderinfo.html',
							{'username': username,
							'role': role,
							'order': order,
							'area': area},
							context_instance=RequestContext(request))
		else:
			return render(request, 'pay/403.html',
						{'username': username},
						context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login')

# 订单详情
def order_detail(request):
	username = request.session.get('username')
	if username:
		role = permission_check(username)
		if role != 'sale':
			if request.method == 'GET':
				onumber = request.GET.get('onu')
				order = Orders.objects.get(onumber=onumber)
				area = Orders.objects.get(onumber=onumber).applicant.area
				return render(request, 'pay/orderdetail.html',
							{'username': username,
							'role': role,
							'order': order,
							'area': area})
		else:
			return HttpResponseRedirect('/login')

# 订单删除
@csrf_exempt
def order_delete(request):
	username = request.session.get('username')
	role = permission_check(username)
	if role != 'sale':
		if request.method == 'POST':
			onumber = request.POST.get('onumber')
			try:
				Orders.objects.get(onumber=onumber).delete()
				return HttpResponse(json.dumps({"msg": "ok"}))
			except:
				return HttpResponse(json.dumps({"msg": "failed!"}))
	else:
		return HttpResponse(json.dumps({"msg":"failed"}))

# 订单发货
@csrf_exempt
def verify_smt(request):
	if request.method == "POST":
		sentnumber = request.POST.get('sentnumber')
		sentdate = request.POST.get('sentdate')
		expresscompany = request.POST.get('expresscompany')
		express = request.POST.get('express')
		onumber = request.POST.get('onumber')
		deliverman = request.POST.get('deliverman')
		# 保存到发货信息表中
		order = Orders.objects.get(onumber=onumber)
		orderinfo = OrdersInfo(order=order, sentnumber=sentnumber, send_date=sentdate, deliverman=deliverman, deliverltd=expresscompany, delivernumber=express, verify=0)
		orderinfo.save()
		order.send_status = 0
		order.verify_status = 0
		order.save()

		return HttpResponse(json.dumps({"msg": "ok"}))
	else:
		return HttpResponse(json.dumps({"msg": "failed"}))


# 新增订单
def new_order(request):
	username = request.session.get('username')
	if username:
		return render(request, 'pay/neworder.html', {'username': username})
	else:
		return HttpResponseRedirect('/login')

# 新增订单处理
@csrf_exempt
def add_order(request):
	if request.method == "POST":
		username = request.session.get('username')
		company = request.POST.get("company")
		user = request.POST.get("username")
		phone = request.POST.get("phone")
		mobile = request.POST.get("mobile")
		repos = request.POST.get("repos")
		transport = request.POST.get("transport")
		source = request.POST.get("source")
		note = request.POST.get("note")
		orderinfo = request.POST.get("orderinfo")
		# 插入数据库
		applicant = Users.objects.get(username=username)
		onumber = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
		order = Orders(onumber = onumber, company = company, client = user, phone = phone, mobile=mobile, repos=repos, transport=transport, source=source, note=note, orderinfo=orderinfo, applicant=applicant)
		order.save()

		return HttpResponse(json.dumps({"msg": "ok"}))
	else:
		return HttpResponse(json.dumps({"msg": "failed"}))

# 入库管理
def ware_confirm(request):
	username = request.session.get('username')
	if username:
		if request.method == 'GET':
			role = permission_check(username)
			if role == 'admin':
				# 搜索条件
				sentnumber = request.GET.get('sentn')
				status = request.GET.get('status')
				express = request.GET.get('expressnumber')
				searchCondition = {'sentnumber__icontains': sentnumber,
					'order__confirm__icontains': status, 'delivernumber__icontains': express}
				kwargs = getCondition(searchCondition)
				query = {'sentn':sentnumber, 'status': status, 'expressnumber': express}
				query = getCondition(query)
				query = urllib.urlencode(query)
				# 分页设置
				limit = 10
				order_list = OrdersInfo.objects.filter(**kwargs).order_by('-id')
				paginator = Paginator(order_list, limit)
				# 获取页数
				page = request.GET.get('page')
				try:
					orderlist = paginator.page(page)
				except PageNotAnInteger:
					orderlist = paginator.page(1)
				except EmptyPage:
					orderlist = paginator.page(paginator.num_pages)
				return render(request, 'pay/wareconfirm.html',
						{'username': username,
						'orderinfos': orderlist,
						'query': query,
						'role': role})

			elif role == 'repo':
				# 搜索条件
				u = Users.objects.get(username=username)
				sentnumber = request.GET.get('sentnumber')
				status = request.GET.get('status')
				express = request.GET.get('express')
				searchCondition = {'sentnumber__icontains': sentnumber, 'order__confirm__icontains': status, 'delivernumber__icontains': express}
				kwargs = getCondition(searchCondition)
				query = {'sentn': sentnumber, 'status': status, 'expressnumber': express}
				query = getCondition(query)
				query = urllib.urlencode(query)
				# 分页设置
				limit = 10
				order_list = OrdersInfo.objects.filter(**kwargs).filter(order__applicant__area__icontains=u.area).order_by('-id')
				paginator = Paginator(order_list, limit)
				# 获取页数
				page = request.GET.get('page')
				try:
					orderlist = paginator.page(page)
				except PageNotAnInteger:
					orderlist = paginator.page(1)
				except EmptyPage:
					orderlist = paginator.page(paginator.num_pages)
				return render(request, 'pay/wareconfirm.html',
							{'username': username,
							'orderinfos': orderlist,
							'query': query,
							'role': role})


			else:
				return render(request, 'pay/403.html',
							{'username': username,
							'role': role})
	else:
		return HttpResponseRedirect('/login')


# 订单入库确认管理
def order_confirm(request):
	username = request.session.get('username')
	if username:
		if request.method == 'GET':
			role = permission_check(username)
			if role != 'sale':
				# 获取订单号
				onumber = request.GET.get('nu')
				order = OrdersInfo.objects.filter(order__onumber=onumber)
				return render(request, 'pay/orderconfirm.html',
							{'username': username,
							'role': role,
							'onumber': onumber,
							'order': order})

			else:
				return render(request, 'pay/403.html', 
								{'username': username,	
								'role': role})
	else:
		return HttpResponseRedirect('/login')

@csrf_exempt
def confirmed(request):
	if request.method == 'POST':
		onumber = request.POST.get('onumber')
		order = Orders.objects.get(onumber=onumber)
		order.confirm = 0
		order.save()
		return HttpResponse(json.dumps({"msg": "ok"}))
	else:
		return HttpResponse(json.dumps({"msg": "failed"}))

# 销售信息
def sale(request):
	username = request.session.get('username')
	if username:
		if request.method == 'GET':
			role = permission_check(username)
			# 搜索条件
			carenumber = request.GET.get('carenumber')
			clientname = request.GET.get('clientname')
			if clientname:
				clientname = request.GET.get('clientname')
			carname = request.GET.get('carname')
			if carname:
				carname = request.GET.get('carname').encode('utf8') 
			saleman = request.GET.get('saleman')
			if saleman:
				saleman = request.GET.get('saleman').encode('utf8')
			beneman = request.GET.get('beneman')
			if beneman:
				beneman = request.GET.get('beneman').encode('utf8')
			# 时间范围
			datefrom = request.GET.get('from')
			start_date = request.GET.get('from')
			dateto = request.GET.get('to')
			end_date = request.GET.get('to')
			if datefrom is not None and datefrom != '' and datefrom != 'None':
				datefrom = datetime.datetime.strptime(datefrom, '%Y-%m-%d')
			if dateto is not None and dateto != '' and dateto != 'None':
				dateto = datetime.datetime.strptime(dateto, '%Y-%m-%d')
			searchCondition = {'care_number__icontains': carenumber, 'client__client_name__icontains': clientname, 'car_name': carname, 'sale_man__icontains': saleman, 'first_benefit__icontains': beneman, 'sale_date__gt': datefrom, 'sale_date__lt': dateto}
			kwargs = getCondition(searchCondition)
			query = {'cnumber': carenumber, 'cname': clientname, 'carname': carname, 'sman': saleman, 'bman': beneman, 'from': start_date, 'to': end_date}
			query = getCondition(query)
			# 分页设置 
			limit = 10
			if role == 'admin':
				carelist = Safe.objects.filter(**kwargs).order_by('-id')
				paginator = Paginator(carelist, limit)
				# 获取页数
				page = request.GET.get('page')
				try:
					carelist = paginator.page(page)
				except PageNotAnInteger:
					carelist = paginator.page(1)
				except EmptyPage:
					carelist = paginator.page(paginator.num_pages)
				query = urllib.urlencode(query)
				return render(request, 'pay/sale.html',
							{'username': username,
							'role': role,
							'query': query,
							'carelist': carelist})
			elif role == 'sale':
				u = Users.objects.get(username=username)
				carelist = Safe.objects.filter(**kwargs).filter(client__fours__contains=u.area).order_by('-id')
				paginator = Paginator(carelist, limit)
				# 获取页数
				page = request.GET.get('page')
				try:
					carelist = paginator.page(page)
				except PageNotAnInteger:
					carelist = paginator.page(1)
				except EmptyPage:
					carelist = paginator.page(paginator.num_pages)
				query = urllib.urlencode(query)
				return render(request, 'pay/sale.html',
							{'username': username,
							'role': role,
							'query': query,
							'carelist': carelist})

			else:
				return render(request, 'pay/403.html',
							{'username': username,
							'role': role})

		else:
			return HttpResponseRedirect('/login')

	else:
		return HttpResponseRedirect('/login')


# 新增销售单
def add_sale(request):
	username = request.session.get('username')
	if username:
		role = permission_check(username)
		if role == 'sale':
			u = Users.objects.get(username=username)
			adviserlist = Adviser.objects.filter(area=u)
			return render(request, 'pay/newsale.html',
						{'username': username,
						'role': role,
						'adviserlist': adviserlist})
		elif role == 'admin':
			return render(request, 'pay/newsale.html',
						{'username': username,
						'role': role})
		else:
			return render(request, 'pay/403.html',
						{'username': username,
						'role': role})
	else:
		return HttpResponseRedirect('/login')


# 新增销售单保存
@csrf_exempt
def upload(request):
	username = request.session.get('username')
	if username:
		if request.method == "POST":
			# 客户信息
			clienttype = request.POST.get('clienttype')
			clientname = request.POST.get('clientname')
			idtype = request.POST.get('idtype')
			idnumber = request.POST.get('idnumber')
			# 地址
			prov = request.POST.get("prov")
			city = request.POST.get("city")
			address = request.POST.get('address')
			mobile = request.POST.get('mobilephone')
			# 保单信息
			# 车辆类型
			buytype = request.POST.get('buytype')
			# 贷款金融机构
			fcompany = request.POST.get('fcompany')
			# 产品名称
			productname = request.POST.get('productname')
			# 主设备名称
			equipname = request.POST.get('equipname')
			# 辅助设备名称
			secondequipname = request.POST.get('secondequip')
			# 初始购车日期
			startdate = request.POST.get('startdate')
			# 车辆品牌
			carname = request.POST.get('carname')
			# 车辆型号
			cartype = request.POST.get('cartype')
			# 购车发票价格
			carprice = request.POST.get('carprice')
			# 车管家价格
			price = request.POST.get('price')
			# 唯一车辆编号
			vin = request.POST.get('vin')
			# 发动机号码
			carnumber = request.POST.get('carnumber')
			# 销售顾问
			saleman = request.POST.get('saleman')			
			beneman = request.POST.get('beneman')
			fileslist = request.FILES.getlist('files')
			# 获取用户地区
			try:
				area = Users.objects.get(username=username).area
			except ObjectDoesNotExist:
				area = 'None'
			# 保存客户信息到Clients
			Clients(fours=area, client_type=clienttype, client_name=clientname, identity_type=idtype, identity_nu=idnumber, prov=prov, city=city, address=address, mobile=mobile).save()
			# 获取client ID号码作为外键
			client = Clients.objects.get(identity_nu=idnumber)
			# 保存到投保单中
			Safe(writer=username, client=client, financial=fcompany, product_name=productname, equip_name=equipname, second_equip_name=secondequipname, car_name=carname, car_type=cartype,  buycar_date=startdate, car_price=carprice, price=price, vin=vin, car_number=carnumber, sale_man=saleman, buy_type=buytype, first_benefit=beneman).save()
			# 获取 vin 作为外键保存
			objvin = Safe.objects.get(vin=vin)
			for file in fileslist:
				Uploaded(vin=objvin, files=file).save()
			# bulk_create优化
			#for file in fileslist:
				#Uploaded.objects.filter(vin=vin).update(files=file)
			#	newfileslist.append(Uploaded(vin=vin, files=file))
			#Uploaded.objects.filter(vin=vin).bulk_create(newfileslist)

			#newfile = Uploaded(files = files)
			#newfile.save()
			return HttpResponseRedirect('/sale')
	else:
		return HttpResponseRedirect('/login')


# 销售单管理审核
def order_check(request):
	username = request.session.get('username')
	if username:
		role = permission_check(username)
		if role == 'admin':
			# 分页设置
			limit = 10
			carelist = Safe.objects.all().order_by('-id')
			paginator = Paginator(carelist, limit)
			# 获取页数
			page = request.GET.get('page')
			try:
				carelist = paginator.page(page)
			except PageNotAnInteger:
				carelist = paginator.page(1)
			except EmptyPage:
				carelist = paginator.page(paginator.num_pages)

			return render(request, 'pay/ordercheck.html',
						{'username': username,
						'role': role,
						'carelist': carelist})
		else:
			return render(request, 'pay/403.html',
						{'username': username,
						'role': role})

# 销售订单审核详情
def sale_confirm(request):
	username = request.session.get('username')
	if username:
		if request.method == 'GET':
			role = permission_check(username)
			if role == 'admin':
				vin = request.GET.get('vin')
				try:
					care = Safe.objects.get(vin=vin)
					files = Uploaded.objects.filter(vin=care)
					cnu = CareNu.objects.all()
				except ObjectDoesNotExist:
					care = []
				return render(request, 'pay/saleinfo.html', {'username': username,
					'role': role,
					'care': care,
					'cnu': cnu,
					'files': files})
			else:
				return render(request, 'pay/403.html',
						{'username': username,
						'role': role})
	else:
		return HttpResponseRedirect('/login')

# 审核确定
@csrf_exempt
def sale_verify(request):
	username = request.session.get('username')
	if username:
		if request.method == "POST":
			vin = request.POST.get('vin')
			bcarenu = request.POST.get('bcarenu')
			carenumber = request.POST.get('carenumber')
			posnumber = request.POST.get('posnumber')
			sale_status = request.POST.get('sale_status')
			install_status = request.POST.get('install_status')
			check_status = request.POST.get('check_status')
			bcarenuobj = CareNu.objects.get(b_care_number=bcarenu)
			# 存入数据库
			Safe.objects.filter(vin=vin).update(b_care_number=bcarenuobj, care_number=carenumber, pos_number=posnumber, sale_status=sale_status, install_status=install_status, check_status=check_status)
			try:
				s = Safe.objects.get(care_number=carenumber)
				return HttpResponse(json.dumps({"msg": "ok"}))
			except MultipleObjectsReturned:
				return HttpResponse(json.dumps({"msg": "failed"}))
		else:
			return HttpResponse(json.dumps({"msg": "failed"}))
	else:
		return HttpResponse(json.dumps({"msg": "failed"})) 

# 销售信息修改
def sale_edit(request):
	username = request.session.get('username')
	if username:
		role = permission_check(username)
		if role != 'repo':
			if request.method == 'GET':
				vin = request.GET.get('id')
				care = Safe.objects.get(vin=vin)
				u = Users.objects.get(username=username)
				adviserlist = Adviser.objects.filter(area=u)
				safefiles = Uploaded.objects.filter(vin=care)
				return render(request, 'pay/saleedit.html',
						{'username': username,
						'care': care,
						'adviserlist': adviserlist,
						'safefiles': safefiles,
						'role': role})

		else:
			return render(request, 'pay/403.html',
						{'username': username,
						'role': role})

	else:
		return HttpResponseRedirect('/login')


# 销售单修改保存
@csrf_exempt
def sale_edit_save(request):
	username = request.session.get('username')
	if username:
		if request.method == "POST":
			# 客户信息
			clienttype = request.POST.get('clienttype')
			clientname = request.POST.get('clientname')
			idtype = request.POST.get('idtype')
			idnumber = request.POST.get('idnumber')
			# 地址
			prov = request.POST.get("prov")
			city = request.POST.get("city")
			address = request.POST.get('address')
			mobile = request.POST.get('mobilephone')
			# 保单信息
			buytype = request.POST.get('buytype')
			fcompany = request.POST.get('fcompany')
			productname = request.POST.get('productname')
			cartype = request.POST.get('cartype')
			equipname = request.POST.get('equipname')
			# 辅助设备名称
			secondequipname = request.POST.get('secondequip')
			# 初始购车日期
			startdate = request.POST.get('startdate')
			# 车辆品牌
			carname = request.POST.get('carname')
			# 车辆型号
			cartype = request.POST.get('cartype')
			# 购车发票价格
			carprice = request.POST.get('carprice')
			# 车管家价格
			price = request.POST.get('price')
			vin = request.POST.get('vin')
			carnumber = request.POST.get('carnumber')
			saleman = request.POST.get('saleman')
			beneman = request.POST.get('beneman')
			fileslist = request.FILES.getlist('files')
			# client id
			cid = request.POST.get('cid')
			# safe id
			sid = request.POST.get('sid')
			# 获取用户地区
			try:
				area = Users.objects.get(username=username).area
			except ObjectDoesNotExist:
				area = 'None'
			# 保存客户信息到Clients
			Clients.objects.filter(id=cid).update(fours=area, client_type=clienttype, client_name=clientname, identity_type=idtype, identity_nu=idnumber, prov=prov, city=city, address=address, mobile=mobile)
			# 获取client ID号码作为外键
			client = Clients.objects.get(identity_nu=idnumber)
			# 保存到投保单中
			Safe.objects.filter(id=sid).update(client=client, financial=fcompany, product_name=productname, car_type=cartype, equip_name=equipname, second_equip_name=secondequipname, car_name=carname, buycar_date=startdate,car_price=carprice, price=price, vin=vin, car_number=carnumber, sale_man=saleman, buy_type=buytype, first_benefit=beneman)
			# 获取 vin 作为外键保存
			objvin = Safe.objects.get(vin=vin)
			for file in fileslist:
				Uploaded(vin=objvin, files=file).save()
			# bulk_create优化
			#for file in fileslist:
				#Uploaded.objects.filter(vin=vin).update(files=file)
			#	newfileslist.append(Uploaded(vin=vin, files=file))
			#Uploaded.objects.filter(vin=vin).bulk_create(newfileslist)

			#newfile = Uploaded(files = files)
			#newfile.save()
			return HttpResponseRedirect('/sale')
	else:
		return HttpResponseRedirect('/login')

# 验证client返回数目
@csrf_exempt
def valid_client(request):
	if request.method == "POST":
		idnumber = request.POST.get("idnumber")
		try:
			client = Clients.objects.get(identity_nu=idnumber)
			return HttpResponse(json.dumps({"msg": "failed"}))
		except ObjectDoesNotExist:
			return HttpResponse(json.dumps({"msg": "ok"}))
		except MultipleObjectsReturned:
			return HttpResponse(json.dumps({"msg": "failed"}))


# 打印页面
def print_tpl(request):
	username = request.session.get('username')
	if username:
		role = permission_check(username)
		if role != 'repo':
			if request.method == 'GET':
				carenumber = request.GET.get('nu')
				try:
					care = Safe.objects.get(care_number=carenumber)
					client = care.client
				except ObjectDoesNotExist, MultipleObjectsReturned:
					care = []
					client = []
				return render(request, 'pay/tpl.html',
							{'username': username,
							'care': care,
							'client': client,
							'role': role})

		else:
			return render(request, 'pay/403.html',
						{'username': username,
						'role': role})
	else:
		return HttpResponseRedirect('/login')

# modal 展示
def modal_show(request):
	username = request.session.get('username')
	if username:
		role = permission_check(username)
		if role != 'repo':
			vin = request.GET.get('vin')
			try:
				care = Safe.objects.get(vin=vin)
				files = Uploaded.objects.filter(vin=care)
			except ObjectDoesNotExist:
				care = []
			return render(request, 'pay/modalshow.html',
						{'care': care,
						'files': files})
		else:
			return render(request, 'pay/403.html',
						{'username': username,
						'role': role})
	else:
		return HttpResponseRedirect('/login')

# 导出excel
def export(request):
	username = request.session.get('username')
	if username:
		role = permission_check(username)
		if role == 'admin':
			# 新建一个IO数据流
			output = StringIO.StringIO()
			# 将xlsx数据写入数据流
			xlsxdata = xlsxwriter.Workbook(output)
			# 新增一个格式
			date_format = xlsxdata.add_format({'num_format': u'yyyy"年"m"月"d"日"'})
			worksheet = xlsxdata.add_worksheet('safe')
			objs = Safe.objects.all()
			col = 1
			row = 0
			header = [
			 	u"代理商",
			 	u"保单号",
			 	u"POS机交易码",
			 	u"客户姓名",
			 	u"客户证件类型",
			 	u"客户证件号码",
			 	u"客户所在省份",
			 	u"客户所在地区",
			 	u"客户联系地址",
			 	u"客户电话",
			 	u"销售日期",
			 	u"贷款金融机构",
			 	u"产品名称",
			 	u"主设备名称",
			 	u"辅设备名称",
			 	u"车辆品牌",
			 	u"车辆型号",
			 	u"初始购车日期",
			 	u"购车发票价格",
			 	u"车管家价格",
			 	u"车架号",
			 	u"发动机号码",
			 	u"销售顾问",
			 	u"购车类型",
			 	u"第一受益人",
			 	u"审核状态",
			 	u"销售状态",
			 	u"安装状态",
			 ]
			for i in range(28):
				worksheet.write(0, i, header[i])
			for obj in objs:
				if obj.client.identity_type=="identity":
					iden = u"身份证"
				elif obj.client.identity_type=="passport":
					iden = u"护照"
				elif obj.client.identity_type=="driven":
					iden = u"驾照"
				else:
					iden = "None"
				fields = [
			 		#(obj.writer,),
			 		(obj.client.fours,),
			 		(obj.care_number,),
			 		(obj.pos_number,),
			 		(obj.client.client_name,),
			 		(iden,),
			 		(obj.client.identity_nu,),
			 		(obj.client.prov,),
			 		(obj.client.city,),
			 		(obj.client.address,),
			 		(obj.client.mobile,),
			 		(str(obj.sale_date),),
			 		(obj.financial,),
			 		(obj.product_name,),
			 		(obj.equip_name,),
			 		(obj.second_equip_name,),
			 		(obj.car_name,),
			 		(obj.car_type,),
			 		(obj.buycar_date, date_format),
			 		(obj.car_price,),
			 		(obj.price,),
			 		(obj.vin,),
			 		(obj.car_number,),
			 		(obj.sale_man,),
			 		(u"全款" if obj.buy_type=="fullpay" else u"贷款",),
			 		(obj.first_benefit,),
			 		(u"未审核" if obj.check_status==1 else u"已审核",),
			 		(u"未销售" if obj.sale_status==1 else u"已销售",),
			 		(u"未安装" if obj.install_status==1 else u"已安装",)
			 	]
			 	print fields
			 	for n in range(28):
			 		worksheet.write(col, row+n, *(fields[n]))
				col += 1
			xlsxdata.close()
			output.seek(0)
			dat = datetime.datetime.now()
			response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
			response['Content-Disposition'] = 'attachment; filename="'+ str(dat) +'export-data.xlsx"'
			return response
		else:
			return render(request, 'pay/403.html',
						{'username': username,
						'role': role})
	else:
		return HttpResponseRedirect('/login')


# 退出
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/login')

# 用户管理
def users(request):
	username = request.session.get('username')
	if username:
		role = permission_check(username)
		if role == 'admin':
			return render(request, 'pay/users.html', 
						{'username': username,
						'role': role}) 
		else:
			return render(request, 'pay/403.html', 
						{'username': username,
						'role': role})
	else:
		return HttpResponseRedirect('/login')

def user_manage(request):
	username = request.session.get('username')
	if username:
		role = permission_check(username)
		if role == 'admin':
			users = Users.objects.all()
			return render(request, 'pay/usermanage.html',
						{'username': username,
						'role': role,
						'users': users})

		else:
			return render(request, 'pay/403.html',
						{'username': username,
						'role': role})
	else:
		return HttpResponseRedirect('/login')

# 用户删除
@csrf_exempt
def user_delete(request):
	username = request.session.get('username')
	role = permission_check(username)
	if role == 'admin':
		if request.method == 'POST':
			uid = request.POST.get('id')
			print uid
			try:
				Users.objects.get(id=uid).delete()
				return HttpResponse(json.dumps({"msg":"ok"}))
			except:
				return HttpResponse(json.dumps({"msg":"failed"}))
	else:
		return HttpResponse(json.dumps({"msg":"failed"}))

# 添加用户
@csrf_exempt
def add_user(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		group = request.POST.get('group')
		area = request.POST.get('area')
		note = request.POST.get('note')

		try:
			user = Users.objects.get(username = username)
			if user is not None:
				return HttpResponse(json.dumps({"msg": "already"}))
		except:
			user = Users(username = username, password = password, group = group, area = area, note =note)
			user.save()
			return HttpResponse(json.dumps({"msg": "ok"}))
	else:
		return HttpResponse(json.dumps({"msg": "failed"}))


# 销售顾问管理
def sale_assis(request):
	username = request.session.get('username')
	if username:
		role = permission_check(username)
		if role == 'sale':
			advisers = Adviser.objects.filter(area__username__contains=username)
			return render(request, 'pay/assis.html',
						{'username': username,
						'role': role,
						'advisers': advisers})

		elif role == 'admin':
			return render(request, 'pay/assis.html',
						{'username': username,
						'role': role})

		else:
			return render(request, 'pay/403.html',
						{'username': username,
						'role': role})
	else:
		return HttpResponseRedirect('/login')

# 销售顾问添加
@csrf_exempt
def assis_process(request):
	username = request.session.get('username')
	if request.method == 'POST':
		sname = request.POST.get('sname')
		idnumber = request.POST.get('idnumber')
		mobile = request.POST.get('mobile')
		user = Users.objects.get(username=username)
		try:
			u = Adviser.objects.get(idnumber=idnumber)
			return HttpResponse(json.dumps({"msg":"failed"}))
		except ObjectDoesNotExist:
			u = Adviser(username=sname, idnumber=idnumber, mobile=mobile, area=user)
			u.save()
		return HttpResponse(json.dumps({"msg":"ok"}))
	else:
		return HttpResponse(json.dumps({"msg":"ok"}))

# 销售顾问修改
def assis_change(request):
	username = request.session.get('username')
	if username:
		role = permission_check(username)
		if request.method == 'GET':
			if role == 'sale':
				idnumber = request.GET.get('id')
				assisinfo = Adviser.objects.get(idnumber=idnumber)
				return render(request, 'pay/assischange.html',
							{'username': username,
							'assisinfo': assisinfo,
							'role': role})
			else:
				return render(request, 'pay/403.html',
							{'username': username,
							'role': role})
		else:
			return HttpResponseRedirect('/login')

	else:
		return HttpResponseRedirect('/login')

# 销售顾问修改处理
@csrf_exempt
def assis_change_process(request):
	username = request.session.get('username')
	if username:
		if request.method == 'POST':
			orinumber = request.POST.get("orinumber")
			username = request.POST.get("username")
			idnumber = request.POST.get("idnumber")
			mobile = request.POST.get("mobile")
			Adviser.objects.filter(idnumber=orinumber).update(username=username, idnumber=idnumber, mobile=mobile)
			return HttpResponse(json.dumps({"msg":"ok"}))
		else:
			return HttpResponse(json.dumps({"msg":"failed"}))

	else:
		return HttpResponse(json.dumps({"msg":"failed"}))


# 销售顾问删除
@csrf_exempt
def assis_delete(request):
	username = request.session.get('username')
	role = permission_check(username)
	if role == 'sale':
		if request.method == 'POST':
			idnumber = request.POST.get('idnumber')
			try:
				Adviser.objects.get(idnumber=idnumber).delete()
				return HttpResponse(json.dumps({"msg":"ok"}))
			except:
				return HttpResponse(json.dumps({"msg":"failed"}))
	else:
		return HttpResponse(json.dumps({"msg":"failed"}))

# 保险文件删除
@csrf_exempt
def safefile_delete(request):
	username = request.session.get('username')
	role = permission_check(username)
	if role == 'sale':
		if request.method == 'POST':
			file = request.POST.get('file')
			vin = request.POST.get('vin')
			try:
				Uploaded.objects.filter(vin__vin__icontains=vin).get(files=file).delete()
				return HttpResponse(json.dumps({"msg":"ok"}))
			except:
				return HttpResponse(json.dumps({"msg":"failed"}))
	else:
		return HttpResponse(json.dumps({"msg":"failed"}))

# 修改密码
def change_pw(request):
	username = request.session.get('username')
	if username:
		role = permission_check(username)
		return render(request, 'pay/changepw.html',
					{'username': username,
					'role': role})
	else:
		return HttpResponseRedirect('/login')

@csrf_exempt
def change(request):
	username = request.session.get('username')
	if username:
		if request.method == 'POST':
			newpasswd = request.POST.get('newpasswd')
			try:
				u = Users.objects.get(username=username)
				u.password = newpasswd
				u.save()
				return HttpResponse(json.dumps({"msg": "ok"}))
			except ObjectDoesNotExist:
				return HttpResponse(json.dumps({'msg': 'failed'}))
	else:
		return HttpResponse(json.dumps({'msg': "failed"}))


# 大保单管理
def care_number(request):
	username = request.session.get('username')
	if username:
		role = permission_check(username)
		if role == 'admin':
			bcarenumber = CareNu.objects.all()
			return render(request, 'pay/bcarenumber.html',
						{'username': username,
						'role': role,
						'bcarenumber': bcarenumber})
		else:
			return render(request, 'pay/403.html',
						{'username': username,
						'role': role})
	else:
		return HttpResponseRedirect('/login')

# 大保单更新
@csrf_exempt
def bcare_process(request):
	username = request.session.get('username')
	if username:
		if request.method == 'POST':
			bcarenu = request.POST.get('bcarenu')
			CareNu.objects.all().update(b_care_number=bcarenu)
			return HttpResponse(json.dumps({"msg": "ok"}))

	else:
		return HttpResponse(json.dumps({'msg': "failed"}))

# 销售信息删除
@csrf_exempt
def saleinfo_delete(request):
	username = request.session.get('username')
	role = permission_check(username)
	if role == 'admin':
		if request.method == 'POST':
			vin = request.POST.get('vin')
			try:
				Safe.objects.get(vin=vin).delete()
				return HttpResponse(json.dumps({"msg":"ok"}))
			except:
				return HttpResponse(json.dumps({"msg":"failed"}))
	else:
		return HttpResponse(json.dumps({"msg":"failed"}))

