#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import jsonify
import calls
from functools import wraps

def check_auth(username, password):
    return username == 'admin' and password == 'secret'

def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'DNS Auth'

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth: 
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated

 
app = Flask("my app")
 
@app.route('/add-domain', methods = ['POST'])
@requires_auth
def add_domain():
    calls.add_domain(request.form['domain'], request.form['ip'])
    calls.reload_dns()
    return "", 200

@app.route('/remove-domain', methods = ['POST'])
@requires_auth
def remove_domain():
    calls.remove_domain(request.form['domain'])
    calls.reload_dns()
    return "", 200
 
@app.route('/block-domain', methods = ['POST'])
@requires_auth
def block_domain():
    calls.block_domain(request.form['domain'])
    calls.reload_dns()
    return "", 200

@app.route('/unblock-domain', methods = ['POST'])
@requires_auth
def unblock_domain():
    calls.unblock_domain(request.form['domain'])
    calls.reload_dns()
    return "", 200

app.run(host='0.0.0.0', port=8053)
