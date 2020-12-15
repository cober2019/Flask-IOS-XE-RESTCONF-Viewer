"""Helper class/methods to GET RESTCONF Config"""

import requests
import warnings
import json


def custom_xpath(config, parent_key):

    values = []
    lists = [k for k in config[parent_key]]
    leafs = [leaf for leaf in lists[0].keys()]

    for i in lists:
        values.append(i.get(leafs[0]))

    return lists, leafs, values

def validate_json(response):
    """Validates JSON from response"""
    try:
        format_res = json.dumps(response.json(), sort_keys=True, indent=4)
        return format_res
    except json.JSONDecodeError:
        return 'JSONError'

def get_capabilities(username, password, device, port, rest_obj):

    modules = []
    response = None
    warnings.filterwarnings('ignore', message='Unverified HTTPS request')
    uri = f"https://{device}:{port}/restconf/data/netconf-state/capabilities"
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
                models = [i for i in config['ietf-netconf-monitoring:capabilities']['capability']]
                for i in models:
                    try:
                        modules.append(i.split('module=')[1].split('&')[0] + '.yang')
                    except IndexError:
                        pass
            except AttributeError:
                pass

            return config, modules, format_response

    except requests.exceptions.ConnectionError:
        return "Access Denied"
    except json.JSONDecodeError:
        # Sometime you can get 200 OK, but a decoder error
        no_config.append(response.status_code)

        return response.status_code, modules, response.text


def get_config_restconf(username, password, device, port, rest_obj, module='Module'):
    """Requested Initial request for config via REST"""

    no_config = []
    leafs = []
    filler = []
    response = None
    rest_obj.module = module

    warnings.filterwarnings('ignore', message='Unverified HTTPS request')
    uri = f"https://{device}:{port}/restconf/data/{module}"
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
                lists = [k for k in config[parent_key].keys()]
                return response.status_code, config, lists, format_response, leafs
            except AttributeError as error:
                paths = custom_xpath(config, parent_key)
                return response.status_code, config, paths[1], format_response, paths[2]

    except requests.exceptions.ConnectionError:
        return "Access Denied"
    except json.JSONDecodeError:
        # Sometime you can get 200 OK, but a decoder error
        no_config.append(response.status_code)

        return response.status_code, leafs, no_config, response.text, filler


class ApiCalls:
    """Python class that requests data"""

    def __init__(self):

        self._module = None
        self.container = None
        self.lists = None
        self.leaf = None
        self.config_keys = None

    def request_container(self, username, password, device, container, port):
        """Get request leaf from config"""

        self.reset()
        self.container = container
        warnings.filterwarnings('ignore', message='Unverified HTTPS request')

        # Build uri based of button click which provides the leaf value
        uri = f"https://{device}:{port}/restconf/data/{self.module}/{self.container}"
        headers = {"Content-Type": 'application/yang-data+json', 'Accept': 'application/yang-data+json'}
        response = requests.get(uri, headers=headers, verify=False, auth=(username, password))

        # Format and return config to caller
        config = json.loads(response.text)
        format_res = json.dumps(response.json(), sort_keys=True, indent=4)
        format_container = self._module.split(":")[0] + f':{self.container}'

        try:
            leafs = [k for k in config.get(f'{format_container}').keys()]
            print(leafs)
            self.config_keys = leafs
        except AttributeError:
            leafs = ''
            self.config_keys = leafs

        return format_res, leafs, self.container

    def request_lists(self, username, password, device, lists, port):
        """Get request leaf from config"""

        self.lists = lists

        warnings.filterwarnings('ignore', message='Unverified HTTPS request')

        # Build uri based of button click which provides the leaf value
        uri = f"https://{device}:{port}/restconf/data/{self.module}/{self.container}/{self.lists}"
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

    def request_custom_lists(self, username, password, device, lists, port):
        """Get request leaf from config"""

        self.lists = lists

        # Used to replace slashes in xpath filters. Usually used for interfaces
        if '/' in self._module and '/' in self.lists:
            conversion = lists.replace('/', '%2f')
            self.lists = self._module + '=' + conversion
            uri = f"https://{device}:{port}/restconf/data/{self.lists}"
        else:
            # Build uri based of button click which provides the leaf value
            uri = f"https://{device}:{port}/restconf/data/{self.module}/{self.lists}"

        headers = {"Content-Type": 'application/yang-data+json', 'Accept': 'application/yang-data+json'}
        response = requests.get(uri, headers=headers, verify=False, auth=(username, password))
        config = json.loads(response.text)
        get_keys = dict.fromkeys(json.loads(response.text))
        parent_key = list(get_keys.keys())[0]
        format_res = json.dumps(response.json(), sort_keys=True, indent=4)

        try:
            leafs = [k for k in config.get(f'{parent_key}').keys()]
            self.config_keys = leafs
        except AttributeError as error:
            leafs = ''
            self.config_keys = leafs

        return format_res, leafs, self.config_keys

    def request_leaf(self, username, password, device, leaf, port):
        """Get request leaf from config"""

        self.leaf = leaf
        warnings.filterwarnings('ignore', message='Unverified HTTPS request')

        # Build uri based of button click which provides the leaf value
        uri = f"https://{device}:{port}/restconf/data/{self.module}/{self.container}/{self.lists}/{self.leaf}"
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
