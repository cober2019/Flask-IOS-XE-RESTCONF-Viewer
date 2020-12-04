"""Helper class/methods to GET RESTCONF Config"""

import requests
import warnings
import json


def validate_json(response):
    """Validates JSON from response"""
    try:
        format_res = json.dumps(response.json(), sort_keys=True, indent=4)
        return format_res
    except json.JSONDecodeError:
        return 'JSONError'


def get_config_restconf(username, password, device, module, rest_obj):
    """Requested Initial request for config via REST"""

    no_config = []
    leafs = []
    response = None
    rest_obj.module = module
    warnings.filterwarnings('ignore', message='Unverified HTTPS request')
    uri = f"https://{device}/restconf/data/{module}"
    headers = {"Content-Type": 'application/yang-data+json', 'Accept': 'application/yang-data+json'}

    # Request config. If wrong IP or access-denied == value return Access Denied to caller
    try:
        response = requests.get(uri, headers=headers, verify=False, auth=(username, password))
        if response.status_code == 401:
            return response.status_code
        else:

            config = json.loads(response.text)
            get_keys = dict.fromkeys(json.loads(response.text))
            parent_key = list(get_keys.keys())[0]
            format_response = validate_json(response)

            try:
                leafs = [k for k in config.get(f'{parent_key}').keys()]
            except AttributeError:
                pass

            return config, leafs, format_response

    except requests.exceptions.ConnectionError:
        return "Access Denied"
    except json.JSONDecodeError:
        # Sometime you can get 200 OK, but a decoder error
        no_config.append(response.status_code)

        return response.status_code, leafs, response.text


class ApiCalls:
    """Python class that requests data"""

    def __init__(self):

        self._module = None
        self.container = None
        self.lists = None
        self.leaf = None
        self.config_keys = None

    def request_container(self, username, password, device, container):
        """Get request leaf from config"""

        self.reset()
        self.container = container
        warnings.filterwarnings('ignore', message='Unverified HTTPS request')

        # Build uri based of button click which provides the leaf value
        uri = f"https://{device}/restconf/data/{self.module}/{self.container}"
        headers = {"Content-Type": 'application/yang-data+json', 'Accept': 'application/yang-data+json'}
        response = requests.get(uri, headers=headers, verify=False, auth=(username, password))

        # Format and return config to caller
        config = json.loads(response.text)
        format_res = json.dumps(response.json(), sort_keys=True, indent=4)
        format_container = self._module.split(":")[0] + f':{self.container}'

        try:
            leafs = [k for k in config.get(f'{format_container}').keys()]
            self.config_keys = leafs
        except AttributeError:
            leafs = ''
            self.config_keys = leafs

        return format_res, leafs, self.container

    def request_lists(self, username, password, device, lists):
        """Get request leaf from config"""

        self.lists = lists

        warnings.filterwarnings('ignore', message='Unverified HTTPS request')

        # Build uri based of button click which provides the leaf value
        uri = f"https://{device}/restconf/data/{self.module}/{self.container}/{self.lists}"
        headers = {"Content-Type": 'application/yang-data+json', 'Accept': 'application/yang-data+json'}
        response = requests.get(uri, headers=headers, verify=False, auth=(username, password))
        config = json.loads(response.text)
        format_res = json.dumps(response.json(), sort_keys=True, indent=4)

        try:
            leafs = [k for k in config.get(f'{lists}').keys()]
            self.config_keys = leafs
        except AttributeError:
            leafs = ''
            self.config_keys = leafs

        return format_res, leafs, self.config_keys

    def request_custom_lists(self, username, password, device, lists):
        """Get request leaf from config"""

        self.lists = lists

        warnings.filterwarnings('ignore', message='Unverified HTTPS request')

        # Build uri based of button click which provides the leaf value
        uri = f"https://{device}/restconf/data/{self.module}/{self.lists}"
        headers = {"Content-Type": 'application/yang-data+json', 'Accept': 'application/yang-data+json'}
        response = requests.get(uri, headers=headers, verify=False, auth=(username, password))
        config = json.loads(response.text)
        format_res = json.dumps(response.json(), sort_keys=True, indent=4)

        try:
            leafs = [k for k in config.get(f'{lists}').keys()]
            self.config_keys = leafs
        except AttributeError:
            leafs = ''
            self.config_keys = leafs

        return format_res, leafs, self.config_keys

    def request_leaf(self, username, password, device, leaf):
        """Get request leaf from config"""

        self.leaf = leaf
        warnings.filterwarnings('ignore', message='Unverified HTTPS request')

        # Build uri based of button click which provides the leaf value
        uri = f"https://{device}/restconf/data/{self.module}/{self.container}/{self.lists}/{self.leaf}"
        headers = {"Content-Type": 'application/yang-data+json', 'Accept': 'application/yang-data+json'}
        response = requests.get(uri, headers=headers, verify=False, auth=(username, password))

        format_res = json.dumps(response.json(), sort_keys=True, indent=4)

        return format_res, self.config_keys

    def reset(self):
        self.config_keys = None

    @property
    def module(self):
        return self._module

    @module.setter
    def module(self, value):
        self._module = value
