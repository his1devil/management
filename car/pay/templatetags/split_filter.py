# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter
def spl(str, char):
	"""
	模板中实现split字符方法
	"""
	return str.split(char)[-1]
