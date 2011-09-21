# -*- coding:utf-8 -*-

import random

from google.appengine.ext import webapp
from models import *
from forms import *

class MainHandler(webapp.RequestHandler):
    def get(self):
        "The home"
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, {'hello':
                                                       'Hello webapp world'}))

    def post(self):
        raise NotImplementedError


class FactFightHandler(webapp.RequestHandler):
    "Handles a fact fight page"
    def get(self):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError


class SubmitAFactHandler(webapp.RequestHandler):
    "Handles the fact submission page"
    def get(self):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError


def battle(fact1, fact2):
    # the best fact has 40% chances of having a bad day
    if fact1.elo_rating > fact2.elo_rating and random.random > .4:
        fact1.won_over(fact2)
    else:
        fact2.won_over(fact1)


class ManyFightsHandler(webapp.RequestHandler):
    "Does a couple random fights"
    def get(self, battles = 10):
        for i in range(battles):
            fact1 = Fact.random()
            fact2 = Fact.random(exclude = [fact1])
            battle(fact1, fact2)

    def post(self):
        raise NotImplementedError


class InitFactDatabaseHandler(webapp.RequestHandler):
    "If there are no facts, provide 10 nice ones"
    def get(self, battles = 10):

        if Fact.query().count() == 0:
            logging.warning('Bootstrapping facts')
            for i in range(10):
                Fact(text = 'Fact %d' % i).put()

    def post(self):
        raise NotImplementedError

class SingleFightHandler(webapp.RequestHandler):
    "Does one fight between two random facts"
    def get(self):

        fact1 = Fact.random()
        fact2 = Fact.random(exclude = [fact1])
        battle(fact1, fact2)

    def post(self):
        raise NotImplementedError

