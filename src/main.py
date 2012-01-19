#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '1.2')

import webapp2 as webapp
from google.appengine.api import users, xmpp

import logging

debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

from models import *
from handlers import *


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'something-very-very-secret',
}

app = webapp2.WSGIApplication(
    routes = [
        (r'/', MainHandler),
        (r'/fact_fight', FactFightHandler),
        (r'/submit', SubmitAFactHandler),
        (r'/ten_fights', ManyFightsHandler),
        (r'/init', InitFactDatabaseHandler),
        (r'/randomize', RandomizeRatingsHandler),
        (r'/fight', SingleFightHandler),
        (r'/fight_sync', SynchronousSingleFightHandler),
        ],
    debug = debug,
    config = config)



