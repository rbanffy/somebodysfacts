# -*- coding:utf-8 -*-

from ndb import model, tasklets

import datetime
import logging
import random
import sys

class Fact(model.Model):
    author = model.StringProperty()
    poster_ip = model.StringProperty()
    posted_on = model.DateTimeProperty(auto_now_add = True)
    last_changed = model.DateTimeProperty(auto_now = True)
    text = model.TextProperty()
    language = model.StringProperty(default = 'en') # The language of the post
    # For selecting random instances
    random_index = model.ComputedProperty(
        lambda self : random.randint(0, sys.maxint))
    # For the Elo rating system
    # see http://en.wikipedia.org/wiki/Elo_rating_system
    total_opponent_ratings = model.FloatProperty(default = 0.)
    wins = model.IntegerProperty(default = 0)
    losses = model.IntegerProperty(default = 0)
    games = model.IntegerProperty(default = 0)
    elo_rating = model.FloatProperty(default = 400.)

    @property
    def k_factor(self):
        "Gives the correction (K) factor"
        if self.elo_rating <= 2100:
            return 32.
        elif self.elo_rating <= 2400:
            return 24.
        else:
            return 16.

    def expected_chance_against(self, fact):
        "Gives the expected odds of this fact winning a match with fact"
        return 1 / (1 + 10 ** ((self.elo_rating + fact.elo_rating) / 400.))

    @tasklets.tasklet
    def won_over(self, fact):
        """
        Self won a match over another fact. Recalculates Elo ratings and saves
        them

        fact1.won_over(fact2)
        """
        if self.key == fact.key:
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

        self.elo_rating = self.elo_rating + self.k_factor * \
            (1 - self.expected_chance_against(fact))
        self.total_opponent_ratings += fact.elo_rating
        self.games += 1
        self.wins += 1
        self.put_async()

        fact.elo_rating = fact.elo_rating - fact.k_factor * \
            (1 - fact.expected_chance_against(self))
        # TODO: check if Elo ratings can become negative
        fact.elo_rating = 0 if fact.elo_rating < 0 else fact.elo_rating
        fact.total_opponent_ratings += previous_elo_rating
        fact.games += 1
        fact.losses += 1
        f2 = fact.put_async()
        yield f1.get_result(), f2.get_result()


    @classmethod
    def random(cls, exclude = []):
        "Returns a random instance"
        # TODO: do this asychronously
        f = None
        while not f:
            position = random.randint(1, sys.maxint)
            f = cls.query(cls.random_index >= position).get()
            if f and f.key in [ e.key for e in exclude ]:
                logging.error('got an excluded: ' + str(f))
        return f

    @classmethod
    def random_pair(cls):
        "Returns two random distinct facts"
        # TODO: do this asynchronously
        pos1 = random.randint(1, sys.maxint)
        f1 = cls.query(cls.random_index <= pos1).get()
        if not f1:
            f1 = cls.query(cls.random_index > pos1).get()
        pos2 = random.randint(1, sys.maxint)
        f2 = cls.query(cls.random_index <= pos1).get()
        if not f2:
            f2 = cls.query(cls.random_index > pos1).get()
        # f1 and f2 only must be resolved here
        if f1 == f2:
            f2 = cls.random(exclude = [f1])
        return (f1, f2)

