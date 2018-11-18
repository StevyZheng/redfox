#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy
import sys
import os
import json
import logging
import traceback
import signal
import atexit
from common import *
from . import RfBaseException


class RfBaseLogging(object):
    def __init__(self,
                 name=None,
                 logfile=RF_LOG_FILEL,
                 loglevel=RF_LOG_LEVEL,
                 logconsole=True,
                 lockfile=""):
        if not name:
            name = self.__class__.__name__
        
        self.name = name
        self.loglevel = loglevel
        self.logfile = logfile
        self.logconsole = logconsole
        self.agent_host_name = None
        
        if logfile:
            logdir = os.path.dirname(logfile)
            if not os.path.exists(logdir):
                os.makedirs(logdir)
            if not os.path.exists(logfile):
                f = open(logfile, 'w+')
                f.close()
            self.logger = self.__init_logger(self.name, self.logfile, self.loglevel, self.logconsole)
        else:
            self.logger = None
        signal.signal(signal.SIGHUP, self.__logRotateHandler)
        
    def __init_logger(self, name, logfile, loglevel, logconsole):
        logger = logging.Logger(name)
        formatter = logging.Formatter(RF_LOG_FORMAT)
        logger.setLevel(loglevel)
        
        # file logger
        handler = logging.FileHandler(logfile)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # stream logger
        if logconsole and sys.stdin.isatty():
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def __map_level(self, lvl):
        level_list = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warn": logging.WARNING,
            "warning": logging.WARNING,
            "err": logging.ERROR,
            "error": logging.ERROR,
        }
        if lvl not in level_list:
            raise Exception("unknow log level: " + lvl)
        return level_list[lvl]

    def __logRotateHandler(self, sig=None, frm=None):
        self.__clear_logger()
        self.logger = self.__init_logger(
            self.name,
            self.logfile,
            self.loglevel,
            self.logconsole
        )
        self.logger.info("Received SIGHUP, rotating log")
    
    def __clear_logger(self):
        if not hasattr(self, "logger"):
            return
        if self.logger:
            for handler in self.logger.handlers:
                handler.close()
            del self.logger
            
    def debug(self, s):
        self.logger.debug(s)
    
    def info(self, s):
        self.logger.info(s)
        
    def warn(self,s):
        self.logger.warn(s)
    
    def log(self, s):
        self.info(s)
    
    def err(self, err=""):
        self.logger.error(err)
        raise RfBaseException(err)
    
    def log_exception(self):
        ex_type, ex, tb = sys.exc_info()
        info = traceback.format_exception(ex_type, ex, tb)
        lines = "Trap exception:\n" + "".join(info).strip()
        self.log(lines)
