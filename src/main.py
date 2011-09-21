#!/usr/bin/env python2.5
# -*- coding:utf-8 -*-

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import users, xmpp

from google.appengine.ext.webapp import template

import logging

import debug_tools
try:
    import ipdb as pdb
except ImportError:
    import pdb

from models import *
from handlers import *

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/fact_fight', FactFightHandler),
                                          ('/submit', SubmitAFactHandler),
                                          ('/random', ManyFightsHandler),
                                          ('/init', InitFactDatabaseHandler),
                                          ('/fight', SingleFightHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
