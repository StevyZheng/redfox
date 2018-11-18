#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy
import fire
from rflib.baselogging import RfBaseLogging
from storage.disk import Disk
from net.interface import Net
from storage.zfs import *


class RfLogging(RfBaseLogging):
	pass


class Main(object):
	_ver = "0.0.1"
	
	def version(self):
		print(self._ver)
	
	disk = Disk()
	net = Net()
	zpool = Zpool()


if __name__ == "__main__":
	fire.Fire(Main)

