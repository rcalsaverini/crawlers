"""
Crawling brazilian soccer results from
http://futpedia.globo.com/campeonato/campeonato-brasileiro/2011#/fase=fase-unica/rodada=1

With:
http://www.clips.ua.ac.be/pages/pattern-web
"""
from datetime import datetime

import hashlib

from pattern import web
from dateutil.parser import parse as parse_date
import pymongo


BASE_URL = 'http://futpedia.globo.com/campeonato/campeonato-brasileiro/{}#/fase=fase-unica/rodada=1'


class Season(object):
    def __init__(self, year):
        self.year = year
        self.url = web.URL(BASE_URL.format(self.year), unicode=True, method='GET')

    def get_dom(self):
        return web.DOM(web.download(self.url, cached=True))

    def matches(self):
        dom = self.get_dom()
        for round in dom('ul.jogos'):
            round_number = int(round('li.lista-classificacao-jogo')[0].attrs['data-rodada'])
            for match in round('a'):
                yield self.parse_match(match, round_number)

    def parse_match(self, match_element, round):
        teams = match_element('div.info-jogo')[0]
        home_team = teams.by_class('time mandante')[0]('meta[itemprop="name"]')[0].attrs['content']
        away_team = teams.by_class('time visitante')[0]('meta[itemprop="name"]')[0].attrs['content']
        score = teams('div.placar')[0]
        home_score = score.by_class('mandante font-face')[0].content
        away_score = score.by_class('visitante font-face')[0].content
        url = match_element('link[itemprop="url"]')[0].attrs["href"]
        time = parse_date(match_element('span.horario')[0].content).time()
        date = parse_date(match_element('time[itemprop="startDate"]')[0].attrs['datetime']).date()
        stadium = match_element('div.data-local span[itemprop="name"]')[0].content
        to_hash = u"{}/{}/{}x{}".format(self.year, round, home_team, away_team).encode('utf8')
        return {
            '_id': hashlib.sha1(to_hash).hexdigest(),
            'year': self.year,
            'url': url,
            'date': datetime.combine(date, time),
            'stadium': stadium,
            'round': round,
            'home_team': home_team,
            'away_team': away_team,
            'home_score': int(home_score),
            'away_score': int(away_score)
        }


if __name__ == "__main__":
    collection = pymongo.Connection().soccer.matches
    for year in range(2003, 2013,1):
        current = 0
        for match in Season(year).matches():
            if match['round'] > current:
                current = match['round']
                print "Round {} of {}".format(current, year)
            collection.insert(match)