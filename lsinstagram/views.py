# -*- coding=utf-8 -*-

from lsinstagram import app

@app.route('/')
def index():
    return 'hello'
