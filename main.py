import functools
import random
import itertools

import os
import gevent
import gevent.monkey

from pystache.loader import Loader
from pystache import render

from flask import Flask, abort, url_for

from translations import translations


app = Flask(__name__)

if not app.debug:
    gevent.monkey.patch_all()

loader = Loader()

home_template = loader.load_name("templates/home")


def slugify(string):
    return string.lower().replace(" ", "-")


routes = {}

for man, woman in translations:
    routes[(slugify(man), slugify(woman))] = (man, woman)


cache = {}


def render_template():
    def func_wrapper(func):
        @functools.wraps(func)
        def renderer(**kwargs):
            context = func(**kwargs)
            key = tuple(context.values())
            output = cache.get(key)

            if not output:
                output = render(home_template, context)
                cache[key] = output

            return output

        return renderer

    return func_wrapper


def get_context_data(man, woman, perm=False):
    permalink = url_for(
        "permalink",
        man=slugify(man),
        woman=slugify(woman),
    )

    title = "Manslator"
    if perm:
        title = f"Manslator - {man} is {woman}"

    return {
        "man": man,
        "woman": woman,
        "permalink": permalink,
        "perm": perm,
        "title": title,
        "description": "Are you confused with how to talk to and about women? Here is your helpful manslator.",
    }


@app.route("/<man>-is-<woman>/")
@render_template()
def permalink(man, woman):
    try:
        translation = routes[(man, woman)]
    except KeyError:
        abort(404)
    else:
        man, woman = translation
        return get_context_data(man, woman, perm=True)


@app.route("/")
@render_template()
def home():
    man, woman = random.choice(translations)

    return get_context_data(man, woman)
