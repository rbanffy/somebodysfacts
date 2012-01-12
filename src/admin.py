# -*- coding:utf-8 -*-

import inspect
import os

from google.appengine.ext import webapp
from ndb import context, tasklets
from google.appengine.ext.webapp import template

import models
# import forms #will be used later for custom forms

class AdminRootHandler(webapp.RequestHandler):
    def get(self):
        """
        The main admin handler
        Lists the kinds of objects that can be managed
        """
        kinds = [ (name, slugify(name)) for name, obj
                  in inspect.getmembers(models)
                  if inspect.isclass(obj) ]
        path = os.path.join(os.path.dirname(__file__),
                            'admin_templates/admin_root.html')
        self.response.out.write(template.render(path, {'kinds': kinds}))


class ListHandler(webapp.RequestHandler):
    "Deals with entity listings of a given kind"
    def get(self, classname):
        raise NotImplementedError


class AddHandler(webapp.RequestHandler):
    "Adds an entity of a given kind"
    pass


class DetailsHandler(webapp.RequestHandler):
    "Shows the details of an entity"
    pass


class EditHandler(webapp.RequestHandler):
    "Edits an entity"
    pass


class DeleteHandler(webapp.RequestHandler):
    "Handles entity deletion"
    def get(self):
        "shows confirmation form"
        raise NotImplementedError

    def post(self):
        "deletes"
        raise NotImplementedError


ADMIN_ROUTES = [
    ('/admin', AdminRootHandler),
    ('/admin/<classname>', ListHandler),
    ('/admin/<classname>/add', AddHandler),
    ('/admin/<classname>/<objecid>', DetailsHandler),
    ('/admin/<classname>/<objecid>/edit', EditHandler),
    ('/admin/<classname>/<objecid>/delete', DeleteHandler),
    ]

