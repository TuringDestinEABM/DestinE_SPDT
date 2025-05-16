"""
This is the main function that creates the blueprint, imports in the modules, and defines some generic routes such as the home and error pages.
"""
from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
bp = Blueprint('digitaltwin', __name__) # Creates the name of the app
from .routes import live_data, map, contact

@bp.route('/home')
def home():
    return render_template('home.html')

@bp.route('/')
def homePage():
    return redirect("/home")

@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


