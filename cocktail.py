# -*- coding: utf-8 -*-

import inshaker
import random

provider = inshaker.Inshaker


def empty_search():
    message, option = provider.default_option()
    return message + provider.recipe(option)


def ordinal_search(options):
    option = random.choice(options)
    message = 'Я знаю {} таких коктейлей. Попробуй такой:\n\n'.format(
        len(options))
    if len(options) == provider.MAX_RESULT_COUNT:
        message = 'Оу! Да я знаю кучу таких коктейлей.'\
            ' Будь конкретней в своих запросах.\n\n'
    if len(options) == 1:
        message = ''
    return message + provider.recipe(option)


def coctail_msg(query):
    options = provider.search(query)
    if len(options) == 0:
        return empty_search()
    return ordinal_search(options)
