# -*- coding:utf-8 -*-

from ndb import model

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
    random_index = model.IntegerProperty(repeated = False)
    # For the Elo rating system
    # see http://en.wikipedia.org/wiki/Elo_rating_system
    total_opponent_ratings = model.FloatProperty(default = 0.)
    wins = model.IntegerProperty(default = 0)
    losses = model.IntegerProperty(default = 0)
    games = model.IntegerProperty(default = 0)
    elo_rating = model.FloatProperty(default = 400.)

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
        logging.error(self)
        self.put()

        fact.elo_rating = fact.elo_rating + fact.k_factor + \
            (1 - fact.expected_chance_against(self))
        fact.total_opponent_ratings += previous_elo_rating
        fact.games += 1
        fact.losses += 1
        fact.put()

    @classmethod
    def random(cls, exclude = []):
        "Returns a random instance"
        f = None
        while True:
            position = random.randint(1, sys.maxint)
            f = cls.query(cls.random_index >= position).get()
            # f = cls.query(cls.random_index >= position).\
            #     order(cls.random_index).get()
            logging.debug(f)
            if f and f not in exclude:
                logging.error(f)
                return f
