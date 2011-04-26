# -*- coding:utf-8 -*-

# A series of snippets, mostly useful for the interactive console

# Add a bunch of facts

from models import *

for i in range(10):
  Fact().put()


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
  if fact1.elo_rating > 1.1 * fact2.elo_rating:
    fact1.won_over(fact2)
  else:
    fact2.won_over(fact1)

print float((datetime.datetime.now() - before).seconds) / num_battles
