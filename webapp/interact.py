from flask import Flask, render_template, request
import json
import sys
sys.path.append('..')
from notebook.user_actions import login, logout
from notebook.get_interactions import get_interactions
from notebook.generate_data import generate_data

app = Flask(__name__)
# URLs

BASE_URL = "https://api.interact.io/v2"
INTERACTIONS_URL = "/interactions"
LOGIN = "/login"

# Users

christian_usr = "christian@interact.io"
christian_pwd = "interact"
michael_usr = "michael@interact.io"
michael_pwd = "mzi"
sebastian_usr = "sebastian@interact.io"
sebastian_pwd = "interact"

MICHAEL = login(michael_usr, michael_pwd, BASE_URL, LOGIN)
CHRISTIAN = login(christian_usr, christian_pwd, BASE_URL, LOGIN)
SEBASTIAN = login(sebastian_usr, sebastian_pwd, BASE_URL, LOGIN)

get_interactions(MICHAEL, BASE_URL, INTERACTIONS_URL, store=True)
get_interactions(CHRISTIAN, BASE_URL, INTERACTIONS_URL, store=True)
get_interactions(SEBASTIAN, BASE_URL, INTERACTIONS_URL, store=True)

print " * Ready"

# Server

@app.route('/')
def interact():
    return render_template('interactions.html')

@app.route('/interactions')
def interactions():

    frequency = int(request.args['frequency'])
    period = int(request.args['period'])

    _, i_michael = generate_data(MICHAEL, frequency, period)
    _, i_sebastian = generate_data(SEBASTIAN, frequency, period)
    _, i_christian = generate_data(CHRISTIAN, frequency, period)

    response = {'MICHAEL': i_michael, 'SEBASTIAN': i_sebastian, 'CHRISTIAN': i_christian}

    return json.dumps(response, separators=(',', ':'))

@app.route('/refresh')
def refresh():
    get_interactions(MICHAEL, BASE_URL, INTERACTIONS_URL, store=True)
    get_interactions(CHRISTIAN, BASE_URL, INTERACTIONS_URL, store=True)
    get_interactions(SEBASTIAN, BASE_URL, INTERACTIONS_URL, store=True)

    return json.dumps({'refreshed': True}, separators=(',', ':'))


if __name__ == '__main__':
    app.run(debug=True)