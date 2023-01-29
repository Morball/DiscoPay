from app import app
from flask import render_template, request, redirect, url_for
from app.models.models import db, Subscription


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/success")
def success():
    return render_template('success.html')

@app.route("/cancelled")
def failure():
    return render_template('cancelled.html')
