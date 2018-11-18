#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy

__version__ = "0.0.1"


class RfBaseException (Exception):
        """When we manually raise exception, we should use this rather than
        generic Exceptions. We should catch explicitly raised exceptions (which
        are generally not bugs, but by design), but let bugs dump traces (which
        better helps debugging).
        """
        pass