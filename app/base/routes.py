# -*- encoding: utf-8 -*-

from flask import jsonify, render_template, redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm
from app.base.models import User
from app.base.util import verify_pass
import app.Modules.ParseFuntion as GetRest

device = None
username = None
password = None
rest_call = None


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():

    global device, username, password, rest_call

    login_form = LoginForm(request.form)
    if 'login' in request.form:

        device = request.form['device']
        username = request.form['username']
        password = request.form['password']

        if device and username and password:

            rest_call = GetRest.ApiCalls()
            return redirect(url_for('base_blueprint.get_config'))

        return render_template('accounts/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/logout')
def logout():
    """User Logout"""

    logout_user()
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/config')
def get_config():
    """Get RESTCONF config from device"""

    get_restconf = GetRest.get_config_restconf(username, password, device)

    # If 'Access Denied' is returned redirect login page, notify user, else render template with variables
    if get_restconf == 'Access Denied':
        flash("Login Failed")
        return redirect(url_for('base_blueprint.login'))
    else:
        return render_template('config.html', restconf=get_restconf[0], leafs=get_restconf[1], json=get_restconf[2])


@blueprint.route('/config', methods=['POST'])
def submit_leaf():

    if request.form.get("container"):

        # Get data from the POST message, call funtion and place data into the called funtions URI
        container = request.form.get("container")
        get_restconf = rest_call.request_container(username, password, device, container)

        # If 'Access Denied' is returned redirect login page, notify user, else render template with variables
        if get_restconf == 'Access Denied':
            return redirect(url_for('base_blueprint.login'))
        else:
            # Render template with variables, that template/html is return to JS funtions and printed in HTML
            return jsonify({'data': render_template('submitrestconf.html', object_list=get_restconf[0], leafs=get_restconf[1],
                                                    container=get_restconf[2])})

    elif request.form.get("leaf"):

        lists = request.form.get("leaf")
        get_restconf = rest_call.request_leaf(username, password, device, lists)

        # If 'Access Denied' is returned redirect login page, notify user, else render template with variables
        if get_restconf == 'Access Denied':
            return redirect(url_for('base_blueprint.login'))
        else:
            # Render template with variables, that template/html is return to JS funtions and printed in HTML
            return jsonify(
                {'data': render_template('submitrestconf.html', object_list=get_restconf[0], leafs=get_restconf[1])})


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500