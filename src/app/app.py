import base64
import datetime
import logging
import os
import zoneinfo

import flask
from flask import Flask, render_template, make_response, request, abort, redirect, url_for
from flask_login import LoginManager

import malclient

from base_paths import page_base_blueprint
from error_handlers import error_handler_blueprint
from recommendation_paths import recommendations_blueprint

class App(Flask):
    def __init__(self):
        super().__init__(__name__, static_folder='../static', template_folder='../templates')
        self.debug_value = False


app = App()

app.register_blueprint(page_base_blueprint)
app.register_blueprint(recommendations_blueprint)

app.register_blueprint(error_handler_blueprint)
