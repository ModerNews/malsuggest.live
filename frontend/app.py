import base64
import datetime
import logging
import zoneinfo

import flask
from flask import Flask, render_template, make_response, request, abort
from flask_login import LoginManager

import malclient


class App(Flask):
    def __init__(self):
       super().__init__(__name__, static_folder='./static', template_folder='./templates')


app = App()


@app.get('/')
def index():
    return make_response(render_template('index.html', redirect_url='https://google.com'), 200)


app.run('0.0.0.0', 5000)