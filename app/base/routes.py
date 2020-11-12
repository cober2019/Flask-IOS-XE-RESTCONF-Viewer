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
    global device, username, password

    login_form = LoginForm(request.form)
    if 'login' in request.form:

        device = request.form['device']
        username = request.form['username']
        password = request.form['password']

        if device and username and password:
            return redirect(url_for('base_blueprint.get_config', module='Cisco-IOS-XE-native:native'))

        return render_template('accounts/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html', form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/logout')
def logout():
    """User Logout"""

    logout_user()
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/config/<module>')
def get_config(module):
    """Get RESTCONF config from device"""

    global rest_call

    rest_call = GetRest.ApiCalls()
    get_restconf = GetRest.get_config_restconf(username, password, device, module=module, rest_obj=rest_call)

    # Checks for valid IP, credentials, and check if RESTCONF is enabled
    if get_restconf == 'Access Denied':
        flash("Login Failed")
        return redirect(url_for('base_blueprint.login'))
    elif get_restconf[1] == 404:
        flash("404: Verify that RESTCONF is enabled")
        return redirect(url_for('base_blueprint.login'))
    elif get_restconf[1] == 'JSONError':
        flash("An Error Occured, Check IP")
        return redirect(url_for('base_blueprint.login'))
    else:
        return render_template('config.html', restconf=get_restconf[0], lists=get_restconf[1], json=get_restconf[2], module=module)


@blueprint.route('/config', methods=['POST'])
def submit_leaf():
    """Submit requested configuration for proccessing"""

    if request.form.get("container"):
        # Get data from the POST message, call funtion and place data into the called funtions URI
        container = request.form.get("container")
        get_restconf = rest_call.request_container(username, password, device, container)

        # Render template with variables, that template/html is return to JS funtions and printed in HTML
        return jsonify(
            {'data': render_template('submitrestconf.html', object_list=get_restconf[0], lists=get_restconf[1],
                                     container=get_restconf[2])})

    elif request.form.get("lists"):

        lists = request.form.get("lists")
        get_restconf = rest_call.request_lists(username, password, device, lists)

        return jsonify({'data': render_template('submitrestconf.html', object_list=get_restconf[0],
                                                leafs=get_restconf[1], lists=get_restconf[2])})

    elif request.form.get("leaf"):

        lists = request.form.get("lists")
        get_restconf = rest_call.request_leaf(username, password, device, lists)

        return jsonify(
            {'data': render_template('submit_leaf.html', object_list=get_restconf[0], lists=get_restconf[1])})

    elif request.form.get("module"):

        module = request.form.get("module")
        get_restconf = GetRest.get_config_restconf(username, password, device, module, rest_call)

        return jsonify({'data': render_template('config.html', restconf=get_restconf[0], lists=get_restconf[1],
                                                json=get_restconf[2])})


@blueprint.route('/custom_query', methods=['POST'])
def get_custom_config():
    """Gets configuration via YANG model"""

    module = request.form.get("module")
    get_restconf = GetRest.get_config_restconf(username, password, device, module=module, rest_obj=rest_call)
    if get_restconf[0] == 404:
        return render_template('json_error.html', restconf=get_restconf[1])
    else:
        return render_template('config.html', restconf=get_restconf[0], lists=get_restconf[1], json=get_restconf[2], module=module)


@blueprint.route('/custom_query')
def custom_query():
    return render_template('custom_query.html', device=device)


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
