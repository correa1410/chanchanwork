from flask import Flask
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = '12345'
Session(app)

from . import routes
