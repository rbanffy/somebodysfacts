# -*- coding:utf-8 -*-

# A series of snippets, mostly useful for the interactive console

# Add a bunch of facts

from models import *

for i in range(10):
  Fact(text = 'fact %d' % i).put()


# Time how long it takes to grab a random entry from the datastore

from models import *
import sys
import random
import datetime

before = datetime.datetime.now()
number = 100
for i in range(number):
  r = Fact.random().random_index

print (datetime.datetime.now() - before).seconds / float(number)


# Do a couple battles in the population

from models import *

before = datetime.datetime.now()

num_battles = 500

for i in range(num_battles):
  fact1 = Fact.random()
  fact2 = Fact.random(exclude = [fact1])
  fact1.won_over(fact2)

print float((datetime.datetime.now() - before).seconds) / num_battles


# Print he average Elo rating for the fact population

from models import *

print sum([f.elo_rating for f in Fact.all()]) / len([f for f in Fact.all()])
