# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from domain import Option


BASE_URL = 'http://ru.inshaker.com'
SEARCH_URL = BASE_URL + '/cocktails/search'
USER_AGENT = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) \
AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7'}


class Inshaker(object):

    MAX_RESULT_COUNT = 20

    @staticmethod
    def parse_option(tag):
        name = tag.a.div.text.encode('utf-8')
        link = tag.a['href'].encode('utf-8')
        img_link = tag.a.img['lazy-src'].encode('utf-8')
        return Option(name, link, img_link)

    @staticmethod
    def search(query):
        response = requests.get(SEARCH_URL,
                                headers=USER_AGENT,
                                params={'q': query})
        soup = BeautifulSoup(response.text, 'html.parser')
        options = soup.find_all('li')
        return map(Inshaker.parse_option, options)

    @staticmethod
    def recipe(option):
        recipe_text = option.name + '\n\n'
        response = requests.get(BASE_URL + option.link, headers=USER_AGENT)
        soup = BeautifulSoup(response.text, 'html.parser')
        steps = soup.find('ul', {'class': 'steps'})
        steps = map(lambda step: step.text.encode('utf-8'), steps)
        recipe_text += '\n'.join(steps)
        return recipe_text

    @staticmethod
    def default_option():
        option = Option(
            'Боярский',
            '/cocktails/208-boyarskiy',
            '/uploads/cocktail/hires/208/icon_Chuck-Norris__highres.jpg')
        message = '''Либо ты слишком пьян, чтобы выразить мысль,
либо я не знаю такого коктейля. Но лишний Боярский лишним не бывает.

'''
        return message, option

if __name__ == '__main__':
    _, option = Inshaker.default_option()
    print Inshaker.recipe(option)
