# -*- coding:utf-8 -*-

from google.appengine.api import users
from google.appengine.ext import db

import datetime
import logging
import random
import sys

class Fact(db.Model):
    author = db.UserProperty()
    poster_ip = db.StringProperty()
    posted_on = db.DateTimeProperty(auto_now_add = True)
    last_changed = db.DateTimeProperty(auto_now = True)
    text = db.TextProperty()
    language = db.StringProperty(default = 'en') # The language of the post
    # For selecting random instances
    random_index = db.IntegerProperty()
    # For the Elo rating system - see http://en.wikipedia.org/wiki/Elo_rating_system
    total_opponent_ratings = db.FloatProperty(default = 0.)
    wins = db.IntegerProperty(default = 0)
    losses = db.IntegerProperty(default = 0)
    games = db.IntegerProperty(default = 0)
    elo_rating = db.FloatProperty(default = 400.)

    def __init__(self, *args, **kwargs):
        super(Fact, self).__init__(*args, **kwargs)
        self.random_index = random.randint(0, sys.maxint)

    @property
    def k_factor(self):
        """
        Gives the correction (K) factor
        """
        if self.elo_rating <= 2100:
            return 32.
        elif self.elo_rating <= 2400:
            return 24.
        else:
            return 16.

    def expected_chance_against(self, fact):
        """
        Gives the expected odds of this fact winning a match with fact
        """
        return 1 / (1 + 10 ** ((self.elo_rating + fact.elo_rating) / 400.))

    def won_over(self, fact):
        """
        Instance won a match over another fact. Recalculates Elo ratings and saves them

        fact1.won_over(fact2)
        """
        if self == fact:
            raise ValueError('A fact cannot compete with itself')

        previous_elo_rating = self.elo_rating
        
        # +------+-----+
        # |Result|Score|
        # +------+-----+
        # |Win   |1    |
        # +------+-----+
        # |Draw  |0.5  |
        # +------+-----+
        # |Loss  |0    |
        # +------+-----+

        self.elo_rating = self.elo_rating + self.k_factor * (1 - self.expected_chance_against(fact))
        self.total_opponent_ratings += fact.elo_rating
        self.games += 1
        self.wins += 1
        self.put()
        
        fact.elo_rating = fact.elo_rating + fact.k_factor + (1 - fact.expected_chance_against(self))
        fact.total_opponent_ratings += previous_elo_rating
        fact.games += 1
        fact.losses += 1
        fact.put()

    @classmethod
    def random(cls, exclude = []):
        """
        Returns a random instance
        """
        f = None
        while f not in exclude:
            position = random.randint(1, sys.maxint)
            f = cls.all().filter('random_index >', position).order('random_index').get()
            if f:
                return f
            else:
                f = cls.all().filter('random_index <=', position).order('-random_index').get()
                return f if f else None
