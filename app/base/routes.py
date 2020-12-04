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
import string

device = None
username = None
password = None
rest_call = None
keys = []


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
    response = GetRest.get_config_restconf(username, password, device, module=module, rest_obj=rest_call)

    if response == 'Access Denied':
        flash("Login Failed")
        return redirect(url_for('base_blueprint.login'))
    elif response == 401:
        flash("401: Verify Credentials")
        return redirect(url_for('base_blueprint.login'))
    elif response == 404:
        flash("404: Verify that RESTCONF is enabled")
        return redirect(url_for('base_blueprint.login'))
    elif response[1] == 'JSONError':
        flash("An Error Occured, Check IP")
        return redirect(url_for('base_blueprint.login'))
    else:
        if response[0] == 404:
            return render_template('config.html', restconf=response[0], json=response[1], lists=None)
        else:
            return render_template('config.html', restconf=response[0], lists=response[1], json=response[2],
                                   module=module)


@blueprint.route('/config', methods=['POST'])
def submit_leaf():
    """Submit requested configuration for proccessing"""

    global keys
    container = request.form.get("container")

    if request.form.get("container"):

        response = rest_call.request_container(username, password, device, request.form.get("container"))
        keys = response[1]

        return jsonify( {'data': render_template('submitrestconf.html', object_list=response[0], lists=response[1], container=response[2])})

    elif request.form.get("lists"):

        response = rest_call.request_lists(username, password, device, request.form.get("lists"))

        return jsonify({'data': render_template('submitrestconf.html', container=container, object_list=response[0],
                                                leafs=response[1], config=response[2], lists=keys,
                                                current_list=request.form.get("lists"))})

    elif request.form.get("module"):

        response = GetRest.get_config_restconf(username, password, device, request.form.get("module"), rest_call)

        return jsonify({'data': render_template('config.html', restconf=response[0], lists=response[1], json=response[2])})

    elif request.form.get("full_config"):

        response = GetRest.get_config_restconf(username, password, device, module=request.form.get("full_config"), rest_obj=rest_call)

        return jsonify({'data': render_template('submitrestconf.html', response_code=response[0], object_list=response[2])})


@blueprint.route('/custom_query')
def custom_query():
    return render_template('custom_query.html', device=device)


@blueprint.route('/custom_query', methods=['POST'])
def get_custom_config():
    """Gets configuration via YANG model"""

    global keys

    response = GetRest.get_config_restconf(username, password, device, module=request.form.get("query"),
                                           rest_obj=rest_call)

    try:
        keys = response[1]
    except (IndexError, TypeError):
        keys = []

    if response[0] == '404 Not Found' or response[0] == 404:
        return render_template('json_error.html', response='404 Not Found')
    elif response[0] == 204:
        return render_template('no_content.html', response='204 No Content')
    elif response[0] == 200:
        # Returned OK response but couldn't decode JSON
        return render_template('view_custom_query.html', json=response[2], lists=keys)

    # Returned valid response and JSON conversion was sucessful
    if request.form.get("query").rfind("/") == -1:
        if keys[0] == 'error':
            return render_template('json_error.html', response='404 Not Found')
        else:
            return redirect(url_for('base_blueprint.get_config', module=request.form.get("query")))
    elif request.form.get("query").rfind("?") == -1:
        if keys[0] == 'error':
            return render_template('json_error.html', response='404 Not Found')
        else:
            return render_template('view_custom_query.html', json=response[2], lists=keys)
    else:
        return render_template('view_custom_query.html', json=response[2], lists=keys)


@blueprint.route('/query_submit_leaf', methods=['POST'])
def submit_custom_leaf():
    """Submit requested configuration for proccessing"""

    if request.form.get("container"):

        response = rest_call.request_container(username, password, device, request.form.get("container"))

        return jsonify({'data': render_template('custom_config.html', object_list=response[0], lists=keys, container=response[2])})

    elif request.form.get("lists"):

        response = rest_call.request_custom_lists(username, password, device, request.form.get("lists"))

        return jsonify({'data': render_template('query_submit_leaf.html', container=keys, object_list=response[0],
                                                leafs=response[1], config=response[2])})

    elif request.form.get("module"):

        response = GetRest.get_config_restconf(username, password, device, request.form.get("module"), rest_call)

        return jsonify({'data': render_template('config.html', restconf=response[0], lists=response[1], json=response[2])})

    elif request.form.get("full_config"):

        response = GetRest.get_config_restconf(username, password, device, module=request.form.get("full_config"), rest_obj=rest_call)

        return jsonify({'data': render_template('submitrestconf.html', response_code=response[0], object_list=response[2])})
