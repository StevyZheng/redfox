#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy
import json
from common import *
from rflib import RfBaseException
from rflib.baselogging import *
import netifaces as nf
import re


def get_sys_platform():
	pass


class SystemInfo(object):
	logger = RfBaseLogging()
	
	def __init__(self):
		if os.path.exists("/sys/class/scsi_disk"):
			self.sys_disk_path = "/sys/class/scsi_disk"
		else:
			self.logger.err("/sys/class/scsi_disk is not exists.")
			raise RfBaseException("error: /sys/class/scsi_disk is not exists.")
		self.os_ver = "rstor 0.0.1"
	
	def get_os_disk(self):
		pass
	
	def get_sys_info(self):
		cpu_mode = exec_shell(
			"cat /proc/cpuinfo |grep \"model name\"|uniq|awk -F\": \" '{print$2}'"
		).strip()
		cpu_count = exec_shell("cat /proc/cpuinfo|grep \"physical id\"|sort|uniq|wc -l").strip()
		cpu_info = "{0} x {1}".format(cpu_count, cpu_mode)
		mem_size = exec_shell("free -h|grep Mem|awk '{print$2}'").strip()
		
		json_str = {
			"cpu_mode": cpu_info,
			"mem_size": mem_size,
			"os": self.os_ver,
		}
		return json_str
	
	def get_disk_hctl(self):
		return list_file(self.sys_disk_path)
	
	def get_disk_info(self):
		all_disk_dict = {}
		hctl = self.get_disk_hctl()
		i = 0
		for f in hctl:
			i_path = pjoin(self.sys_disk_path, f, "device")
			t_model = read_file(pjoin(i_path, "model"))
			t_fw = read_file(pjoin(i_path, "rev"))
			t_dev = list_file(pjoin(i_path, "block"))[0].strip()
			t_vendor = read_file(pjoin(i_path, "vendor"))
			t_wwn = exec_shell("udevadm info --query=all --name=/dev/{0}".format(
				t_dev) + "|grep ID_WWN_WITH|awk -F'=' '{print$2}'").strip()
			if len(t_wwn) > 2:
				t_wwn = t_wwn[2:]
			t_sg = get_first_dir(pjoin(i_path, "scsi_generic"))
			t_sn = exec_shell("udevadm info --query=all --name=/dev/{0}".format(
				t_dev) + "|grep ID_SCSI_SERIAL|awk -F'=' '{print$2}'").strip()
			disk_dict = {
				"id": i,
				"hctl": f,
				"model": t_model,
				"fw": t_fw,
				"vendor": t_vendor,
				"wwn": t_wwn,
				"sg": t_sg,
				"sn": t_sn,
			}
			i += 1
			all_disk_dict[t_dev] = disk_dict
		return all_disk_dict
	
	def get_net_info(self):
		interfaces = nf.interfaces()
		interfaces_dict = {}
		try:
			gateways = nf.gateways()
			for i in interfaces:
				if re.match("eth[0-9]+|eno[0-9]+|enp[0-9]+s[0-9]+f[0-9]+|ib[0-9]+]", i):
					ifaddrs = nf.ifaddresses(i)
					interfaces_dict[i] = {}
					if nf.AF_INET in ifaddrs:
						interfaces_dict[i]["inets"] = ifaddrs[nf.AF_INET]
					if nf.AF_LINK in ifaddrs and len(ifaddrs[nf.AF_LINK]) > 0 and "addr" in dict(
							ifaddrs[nf.AF_LINK][0]):
						interfaces_dict[i]["mac"] = ifaddrs[nf.AF_LINK][0]["addr"]
				else:
					self.logger.err("Network interface is not exist!")
					raise RfBaseException("Network interface is not exist!")
		except RfBaseException as msg:
			print(msg)
		return interfaces_dict
	
	def set_net(self, interface, ipaddr, netmask, dns1=None):
		net_info = self.get_net_info()
		net_setting = {}
		if interface not in net_info:
			raise RfBaseException("Netiface is not exsits.")
		else:
			net_setting = {
				"interface": interface,
				"addr": ipaddr,
				"netmask": netmask,
			}
			if dns1 is not None:
				net_setting["dns1"] = dns1
			
			net_path = "/etc/sysconfig/network-scripts/"
			net_conf = pjoin(net_path, "ifcfg-{0}".format(interface))
			net_str = "TYPE=Ethernet\nBOOTPROTO=static-**"
			self.restart_net()
	
	def restart_net(self):
		x = exec_shell("service network restart")
		self.logger.info("Starting restart network...")
		return x
