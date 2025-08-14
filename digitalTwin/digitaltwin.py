"""
This is the main function that creates the blueprint, imports in the modules, and defines some generic routes such as the home and error pages.
"""
from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
bp = Blueprint('digitaltwin', __name__) # Creates the name of the app
from .routes import Legacysubmit, contact, createScenario, data_sources, help, live_data, map, queue, reports, settings, user
from .library import getData
import json
from pathlib import Path

@bp.route('/home', methods = ['POST', 'GET'])
def home():
    data = reports.listAvailableReports()
    return render_template('home.html', data = data)

@bp.route('/')
def homePage():
    data = reports.listAvailableReports()
    return redirect("/home", data = data)

@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
