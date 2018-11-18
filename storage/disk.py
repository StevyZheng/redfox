#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy
from rflib.system import *
import prettytable as pt


class Disk(object):
	def __init__(self):
		pass
	
	def show(self, type="table"):
		system = SystemInfo()
		disk_info = system.get_disk_info()
		if type == DATA_TYPE_TABLE:
			tb = pt.PrettyTable()
			tb.hrules = pt.ALL
			tb.vrules = pt.ALL
			tb.field_names = ["disk", "model", "h:c:t:l", "sn", "wwn", "sg"]
			for key in disk_info:
				data = disk_info[key]
				tb.add_row([key, data["model"], data["hctl"], data["sn"], data["wwn"], data["sg"]])
			print(tb)
		elif type == DATA_TYPE_JSON:
			print(json.dumps(disk_info, indent=1))
