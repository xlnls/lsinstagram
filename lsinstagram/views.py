# -*- coding=utf-8 -*-

from lsinstagram import app
from flask import render_template
from models import Image,User
@app.route('/')
def index():
    image  = Image.query()

    return render_template('index.html')
