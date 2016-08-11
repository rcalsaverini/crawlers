"""
Analysis of home advantage in Soccer games.
"""
from __future__ import division
from matplotlib.pyplot import show

import pymongo
import pandas

collection = pymongo.Connection().soccer.matches
data = pandas.DataFrame(list(collection.find({}, {'_id': 0, 'url': 0})))
data['spread'] = data.home_score - data.away_score

home_scores = data[data.home_team == 'Corinthians'].home_score.value_counts()
away_scores = data[data.away_team == 'Corinthians'].away_score.value_counts()

scores = pandas.DataFrame({'home': home_scores / home_scores.sum(), 'away': away_scores / away_scores.sum()})
scores.reset_index().head().sort('index').set_index('index').plot(style='o-')
show()