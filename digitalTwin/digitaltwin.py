"""
This is the main function that creates the blueprint, imports in the modules, and defines some generic routes such as the home and error pages.
"""
from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint, current_app
bp = Blueprint('digitaltwin', __name__) # Creates the name of the app
from .routes import contact, data_sources, help, manage_data, queue, reports, scenarios, settings, user
from .library import dataManager
from pathlib import Path

@bp.route('/home', methods = ['POST', 'GET'])
def home():
    data, next_url, prev_url = dataManager.listAvailableScenarios(1, 'desc')
    return render_template('home.html', data = data, next_url=next_url,
                           prev_url=prev_url)

@bp.route('/')
def homePage():
    return redirect("/home")

@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

