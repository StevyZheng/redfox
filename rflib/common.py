#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy
import os
import logging
from enum import Enum, unique
from . import *
from os.path import join as pjoin

RF_LOG_DIR = "/var/log/redfox"
RF_CONF_DIR = "/etc/redfox"

if not os.path.exists(RF_LOG_DIR):
	os.mkdir(RF_LOG_DIR)
if not os.path.exists(RF_CONF_DIR):
	os.mkdir(RF_CONF_DIR)

RF_DISKINFO_FILE = pjoin(RF_CONF_DIR, "disk_info.json")

RF_LOG_FILEL = os.path.join(RF_LOG_DIR, "redfox.log")
RF_LOG_FORMAT = '%(asctime)s [%(name)s][%(process)d] %(levelname)s: %(message)s'
RF_LOG_LEVEL = logging.WARNING
RF_DEBUG_LEVEL = logging.INFO

DATA_TYPE_TABLE = "table"
DATA_TYPE_JSON = "json"

RF_HDD = "HDD"
RF_SSD = "SSD"

RF_SHELL_TIMEOUT_DEF = 30

YES_STRINGS = ["yes", "YES", "ON", "on", "true", "True", "TRUE"]
NO_STRINGS = ["no", "NO", "OFF", "off", "false", "False", "FALSE"]


def read_file(file_path):
	with open(file_path, 'r') as fp:
		string = fp.read()
	return string[:-1].strip()


def write_file(file_path, string):
	with open(file_path, 'w') as fp:
		fp.truncate()
		fp.write(string)


def append_file(file_path, string):
	with open(file_path, 'a') as fp:
		fp.write(string)


@unique
class FileType(Enum):
	DIR = 1
	FILE = 2
	ALL = 3
	LINK = 4


def list_file(path, file_type=FileType.ALL):
	tmp = os.listdir(path)
	if file_type == FileType.ALL:
		return tmp
	elif file_type == FileType.FILE:
		return [f for f in tmp if os.path.isfile(os.path.join(path, f))]
	elif file_type == FileType.DIR:
		return [f for f in tmp if os.path.isdir(os.path.join(path, f))]
	elif file_type == FileType.LINK:
		return [f for f in tmp if os.path.islink(os.path.join(path, f))]
	else:
		raise RfBaseException("File type is error.")


def get_first_dir(path):
	tmp = list_file(path, FileType.DIR)
	if len(tmp) > 0:
		return tmp[0]
	else:
		raise RfBaseException("File path error.")
	

def check_line_is_exist(fp, line_list):
	for line in fp.readlines():
		line = line.strip('\n')
		if cmp(line, line_list) == 0:
			return 1
	return 0


def exec_shell(cmd):
	result = os.popen(cmd)
	return result.read()
