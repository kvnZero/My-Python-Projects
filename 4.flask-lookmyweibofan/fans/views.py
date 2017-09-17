from . import app
from flask import render_template,request,redirect,url_for

@app.route('/')
def index():
    return ("Hello World")
