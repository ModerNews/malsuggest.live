import base64
import datetime
import logging
import os
import zoneinfo

import flask
from flask import Flask, render_template, make_response, request, abort, redirect, url_for
from flask_login import LoginManager

import malclient


class App(Flask):
    def __init__(self):
        super().__init__(__name__, static_folder='./static', template_folder='./templates')
        self.debug_value = False


app = App()


@app.get('/')
def index():
    url, code_verifier = malclient.generate_authorization_url('48563b906310d3fdb4cefa1c1877bfc3')
    logging.info(code_verifier)
    response = make_response(render_template('index.html', redirect_url=url + '&redirect_uri=' + os.getenv('MAL_REDIRECT', 'http://127.0.0.1:5000/redirect')), 200)
    response.set_cookie('code_verifier', value=base64.b64encode(code_verifier.encode()).decode(),
                        expires=(datetime.datetime.now(tz=zoneinfo.ZoneInfo('Europe/London')) + datetime.timedelta(minutes=3)))
    return response


@app.get('/redirect')
def redirect_receive():
    try:
        code_verifier = base64.b64decode(request.cookies.get('code_verifier').encode()).decode()
    except AttributeError:
        abort(410)
        return
    if not request.args.get('code'):
        abort(400)
        return
    token_response = malclient.fetch_token_schema_2(client_id=os.getenv('MAL_CLIENT_ID'),
                                                    client_secret=os.getenv('MAL_CLIENT_SECRET'),
                                                    code=request.args.get('code'),
                                                    code_verifier=code_verifier,
                                                    redirect_uri=os.getenv('MAL_REDIRECT', 'http://127.0.0.1:5000/redirect'))
    response = make_response(redirect(url_for('recommendations_page')), 302)
    response.set_cookie('access_token', value=token_response.get('access_token'), samesite='Strict', expires=(datetime.datetime.now() + datetime.timedelta(seconds=int(token_response.get('expires_in')))))
    response.set_cookie('refresh_token', value=token_response.get('refresh_token'), samesite='Strict', expires=(datetime.datetime.now() + datetime.timedelta(seconds=int(token_response.get('expires_in')))))
    response.delete_cookie('code_verifier')
    return response


@app.get('/recommendations')
def recommendations_page():
    if not app.debug_value:
        app.debug_value = True
        return render_template('loading.html')
    else:
        return render_template('results.html')

@app.errorhandler(410)
def code_verification_timeout(e):
    return render_template('errors/error.html', error_title='You were timed-out',
                           error_msg='What you were trying to do took too long, please try again')


@app.errorhandler(400)
def code_not_present(e):
    return render_template('errors/error.html', error_title='There was an error in your request',
                           error_msg='You did not provide code parameter')
