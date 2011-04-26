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
from forms import *

class MainHandler(webapp.RequestHandler):
    def get(self):
        """
        The home
        """
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, {'hello': 'Hello webapp world'}))
    
    def post(self):
        raise NotImplementedError



def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
