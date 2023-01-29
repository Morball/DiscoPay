from flask import Flask,session

app = Flask(__name__)
app.config.from_pyfile("config/config.py")
from app.models.models import db

from app.views.home import routes
from app.views.api import payments
from app.views.api import subscriptions
