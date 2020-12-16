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
import app.Modules.FileCommands as GetPyang
import string
import os

device = None
username = None
password = None
rest_call = None
port = None
keys = []


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    global device, username, password, port

    login_form = LoginForm(request.form)
    if 'login' in request.form:

        device = request.form['device']
        username = request.form['username']
        password = request.form['password']
        port = request.form['port']
        
        if not port:
            port = 443

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
    response = GetRest.get_config_restconf(username, password, device, port, rest_obj=rest_call, module=module)

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
            return render_template('config.html', restconf=response[1], json=response[2], lists=None)
        else:
            return render_template('config.html', restconf=response[1], lists=response[2], json=response[3],
                                   module=module)


@blueprint.route('/config', methods=['POST'])
def submit_leaf():
    """Submit requested configuration for proccessing"""

    global keys
    container = request.form.get("container")

    if request.form.get("container"):

        response = rest_call.request_container(username, password, device, request.form.get("container"), port)
        keys = response[1]

        return jsonify( {'data': render_template('submitrestconf.html', object_list=response[0], lists=response[1], container=response[2])})

    elif request.form.get("lists"):

        response = rest_call.request_lists(username, password, device, request.form.get("lists"), port)

        return jsonify({'data': render_template('submitrestconf.html', container=container, object_list=response[0],
                                                leafs=response[1], config=response[2], lists=keys,
                                                current_list=request.form.get("lists"))})

    elif request.form.get("module"):

        response = GetRest.get_config_restconf(username, password, device, port, request.form.get("module"), rest_call)

        return jsonify({'data': render_template('config.html', restconf=response[0], lists=response[1], json=response[2])})

    elif request.form.get("full_config"):

        response = GetRest.get_config_restconf(username, password, device, port, module=request.form.get("full_config"), rest_obj=rest_call)

        return jsonify({'data': render_template('submitrestconf.html', response_code=response[0], object_list=response[3])})


@blueprint.route('/custom_query')
def custom_query():
    return render_template('custom_query.html', device=device)


@blueprint.route('/custom_query', methods=['POST'])
def get_custom_config():
    """Gets configuration via YANG model"""

    global keys
    # Replace query slashes to uri readable form
    if '=' in request.form.get("query"):
        find_slashes = request.form.get("query").split('=')[-1].replace('/', '%2f')
        query = request.form.get("query").replace(request.form.get("query").split('=')[-1], find_slashes)
    else:
        query = request.form.get("query")

    response = GetRest.get_config_restconf(username, password, device, port, rest_call, module=query)

    try:
        keys = response[2]
    except (IndexError, TypeError):
        pass

    if response[0] == '404 Not Found' or response[0] == 404:
        return render_template('json_error.html', response='404 Not Found')
    elif response[0] == 204:
        return render_template('no_content.html', response='204 No Content')
    elif response[0] == 200:
        return render_template('view_custom_query.html', json=response[3], lists=keys, leafs=response[2])


@blueprint.route('/query_submit_leaf', methods=['POST'])
def submit_custom_leaf():
    """Submit requested configuration for proccessing"""

    if request.form.get("depth_1"):
        response = rest_call.request_depth_one(username, password, device, request.form.get("depth_1"), port, rest_call)

        return jsonify({'data': render_template('depth_one.html', container=keys, object_list=response[3],
                                                leafs=response[2], config=response[3])})

    elif request.form.get("depth_2"):
        response = rest_call.request_depth_two(username, password, device, request.form.get("depth_2"), port, rest_call)

        return jsonify({'data': render_template('depth_two.html', leafs=response[2], config=response[3])})

    elif request.form.get("depth_3"):
        response = rest_call.request_depth_three(username, password, device, request.form.get("depth_3"), port, rest_call)

        return jsonify({'data': render_template('depth_three.html',  config=response[3])})

    elif request.form.get("depth_4"):
        response = rest_call.request_depth_four(username, password, device, request.form.get("depth_4"), port, rest_call)

        return jsonify({'data': render_template('depth_four.html', config=response[3])})

@blueprint.route('/pyang_query')
def pyang_query():
    
    if os.name != 'nt':
        yangs = []
        capabilities = GetRest.get_capabilities(username, password, device, rest_call)
        pyang_data = GetPyang.get_yang()
        for i in capabilities[1]:
            for h in pyang_data:
                if i == h:
                    yangs.append(i)
            
        return render_template('pyang_query.html', yang_model=yangs)
    else:
        return render_template('not_compatible.html')



@blueprint.route('/pyang_query', methods=['POST'])
def present_pyang():
    
    if request.form.get('modelType') == 'standard':
        get_model = GetPyang.get_standard_tree(request.form.get('model'))
        return render_template('display_yang.html', tree=get_model)
    elif request.form.get('modelType') == 'dynamic':
        GetPyang.get_dynamic_tree(request.form.get('model'))
        return render_template('jstree.html')
    elif request.form.get('modelType') == 'yin':
        yin = GetPyang.get_yin(request.form.get('model'))
        return render_template('display_yang.html', tree=yin)
    
