#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy
import json
import prettytable as pt
from rflib.common import *
from rflib.system import *


class Net(object):
	def __init__(self):
		pass
	
	def show(self, type="table"):
		s = SystemInfo()
		ni = s.get_net_info()
		if type == "table":
			p = pt.PrettyTable(["interface", "ipaddr", "netmask", "mac"])
			for i in ni:
				addr = netmask = "None"
				if "inets" in ni[i] and len(ni[i]["inets"]) > 0:
					addr = ni[i]["inets"][0]["addr"]
					netmask = ni[i]["inets"][0]["netmask"]
				p.add_row([i, addr, netmask, ni[i]["mac"]])
			print(p)
		elif type == "json":
			print(json.dumps(ni, indent=1))
