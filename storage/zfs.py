#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy
from rflib.diskOp import *
from rflib.common import *


class Zpool(object):
	def __init__(self):
		pass
	
	def list(self):
		print(exec_shell("zpool list"))
	
	def status(self):
		pass
