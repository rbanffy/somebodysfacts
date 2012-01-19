# -*- coding:utf-8 -*-

import inspect
import os

import webapp2
from google.appengine.ext.ndb.model import Model, Key
from google.appengine.ext.ndb import context, tasklets
from google.appengine.ext.webapp import template

import logging

import models
# import forms #will be used later for custom forms

import debug_tools


debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

class AdminRootHandler(webapp2.RequestHandler):
    def get(self):
        """
        The main admin handler
        Lists the kinds of objects that can be managed
        """
        kinds = [ name for name, obj
                  in inspect.getmembers(models)
                  if inspect.isclass(obj) ]
        path = os.path.join(os.path.dirname(__file__),
                            'admin_templates/admin_root.html')
        self.response.out.write(template.render(path, {'kinds': kinds}))


class ListHandler(webapp2.RequestHandler):
    "Deals with entity listings of a given kind"
    def get(self, kindname, offset = 0):
        kind = models.__dict__[kindname]
        #debug_tools.setup(); import pdb ; pdb.set_trace()
        instances = [ o.key.id() for o in kind.query().fetch(100,
                                                             offset = offset) ]
        path = os.path.join(os.path.dirname(__file__),
                            'admin_templates/admin_list.html')
        self.response.out.write(template.render(path, {'kind': kindname,
                                                       'instances': instances}))




class AddHandler(webapp2.RequestHandler):
    "Adds an entity of a given kind"
    pass


class DetailsHandler(webapp2.RequestHandler):
    "Shows the details of an entity"
    def get(self, kindname, object_id):
        kind = models.__dict__[kindname]
        entity = Key(kind, int(object_id)).get()
        detail_names = ['author', 'text']
        details = { name:entity.__dict__['_values'][name]
                    for name in detail_names }
        debug_tools.setup(); import pdb ; pdb.set_trace()



class EditHandler(webapp2.RequestHandler):
    "Edits an entity"
    pass


class DeleteHandler(webapp2.RequestHandler):
    "Handles entity deletion"
    def get(self):
        "shows confirmation form"
        raise NotImplementedError

    def post(self):
        "deletes"
        raise NotImplementedError


app = webapp2.WSGIApplication(
    routes = [
        (r'/admin$', AdminRootHandler),
        (r'/admin/(\w+)$', ListHandler),
        (r'/admin/(\w+)/add$', AddHandler),
        (r'/admin/(\w+)/(\w+)$', DetailsHandler),
        (r'/admin/(\w+)/(\w+)/edit$', EditHandler),
        (r'/admin/(\w+)/(\w+)/delete$', DeleteHandler),
    ],
    debug = debug)

