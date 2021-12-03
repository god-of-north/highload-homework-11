from time import sleep

from flask import Flask
from .cache import cache, Redis


app = Flask(__name__)

redis = Redis(host = 'redis', port = 6379, db = 1)


def upper(word:str):
    print(f'---upper: {word}')
    sleep(3)
    return word.upper()

@cache(redis, 30, 1.0)
def upper_cached(word:str):
    print(f'---upper: {word}')
    sleep(3)
    return word.upper()

@app.route("/get_cached/<text>")
def get_cached(text:str):
    return redis.get_cached(text, lambda: upper(text), 30)

@app.route("/upper_cached/<text>")
def get_upper_cached(text:str):
    return upper_cached(text)

