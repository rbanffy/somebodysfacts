# -*- coding:utf-8 -*-

import random
import os

from google.appengine.ext import webapp
from ndb import context, tasklets

from models import *
from forms import *

class MainHandler(webapp.RequestHandler):
    def get(self):
        "The home"
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, {'hello':
                                                       'Hello webapp world'}))


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


@tasklets.tasklet
def battle(fact1, fact2):
    # the best fact has 40% chances of having a bad day
    if fact1.elo_rating > fact2.elo_rating and random.random > .4:
        yield fact1.won_over(fact2)
    else:
        yield fact2.won_over(fact1)


class ManyFightsHandler(webapp.RequestHandler):
    "Does a couple random fights"
    @context.toplevel
    def get(self, battles = 10):
        for i in range(battles):
            fact1 = Fact.random()
            fact2 = Fact.random(exclude = [fact1])
            battle(fact1, fact2)


class SingleFightHandler(webapp.RequestHandler):
    "Does one fight between two random facts"
    @context.toplevel
    def get(self):
        fact1 = Fact.random()
        fact2 = Fact.random(exclude = [fact1])
        battle(fact1, fact2)


def sync_battle(fact1, fact2):
    # the best fact has 40% chances of having a bad day
    if fact1.elo_rating > fact2.elo_rating and random.random > .4:
        return fact1.sync_won_over(fact2)
    else:
        return fact2.sync_won_over(fact1)


class SynchronousSingleFightHandler(webapp.RequestHandler):
    "Does one fight between two random facts"
    def get(self):
        fact1 = Fact.random()
        fact2 = Fact.random(exclude = [fact1])
        sync_battle(fact1, fact2)


@tasklets.tasklet
def init_fact_database(n = 10):
    if Fact.query().count(1) == 0:
        logging.warning('Bootstrapping facts')
        futures = []
        for i in range(n):
            futures.append(Fact(text = 'Fact %d' % i).put_async())
        raise tasklets.Return(futures)


class InitFactDatabaseHandler(webapp.RequestHandler):
    "If there are no facts, provide 10 nice ones"
    @context.toplevel
    def get(self):
        init_fact_database()


@tasklets.tasklet
def randomize_rating(f):
    f.elo_rating = random.normalvariate(400, 20)
    raise tasklets.Return(f.put_async())


class RandomizeRatingsHandler(webapp.RequestHandler):
    @context.toplevel
    def get(self):
        Fact.query().map_async(randomize_rating)
