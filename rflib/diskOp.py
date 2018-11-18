#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy
import os
from common import *
from system import *


def mkgpt(disk_name):
	return exec_shell("parted /dev/{0} -s -- mklabel".format(disk_name))


def mkpart(disk_name, part_count, *part_info):
	if isinstance(part_info, dict):
		tmp = "1"
		for i in range(0, part_count):
			if isinstance(part_info, list):
				t1 = "1" if i == 0 else tmp
				t2 = part_info[i]
				tmp = t2
				ret = exec_shell("parted /dev/{0} -s -- mkpart primary {1} {2}".format(disk_name, t1, t2))
				return ret


def zero_disk(disk_name):
	exec_shell("dd if=/dev/zero of=/dev/{0} bs=1M count=50".format(disk_name))


def mk_zfs_part():
	s = SystemInfo()
	disk_info = s.get_disk_info()
	disks = disk_info.keys()
	ret = None
	for i in range(0, len(disks)):
		if isinstance(disks, list):
			ret = exec_shell("parted /dev/{0} -s -- mkpart primary 1 -1".format(disks[i]))
	exec_shell("partprobe")
	return ret


def zero_disks(disk_list):
	if isinstance(disk_list, list):
		for i in disk_list:
			zero_disk(i)
