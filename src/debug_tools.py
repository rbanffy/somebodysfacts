# -*- coding:utf-8 -*-

def setup():
    import sys
    for attr in ('stdin', 'stdout', 'stderr'):
        setattr(sys, attr, getattr(sys, '__%s__' % attr))
