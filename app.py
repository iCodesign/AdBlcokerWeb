# coding: utf-8

from datetime import datetime

from flask import Flask, request
from flask import render_template

from views.todos import todos_view

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test/')
def test():
    return render_template('test.html')

@app.route('/instructions/')
def instructions():
    lang = request.args.get('lang', 'en')
    return render_template('instructions_%s.html' % lang)