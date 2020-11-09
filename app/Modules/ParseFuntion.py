"""Helper class/methods to GET RESTCONF Config"""

import requests
import warnings
import json


def get_config_restconf(username, password, device):
    """Requested Initial request for config via REST"""

    config = None
    response = None

    warnings.filterwarnings('ignore', message='Unverified HTTPS request')
    uri = f"https://{device}/restconf/data/Cisco-IOS-XE-native:native"
    headers = {"Content-Type": 'application/yang-data+json', 'Accept': 'application/yang-data+json'}

    # Request config. If wrong IP or access-denied == value return Access Denied to caller
    try:
        response = requests.get(uri, headers=headers, verify=False, auth=(username, password))
        config = json.loads(response.text)
        if config.get('errors', {}).get('error', {})[0].get('error-tag', {}) == 'access-denied':
            return "Access Denied"
    except requests.exceptions.ConnectionError:
        return "Access Denied"
    except KeyError:
        # If key error or auth index doesnt exist, format config to json, get keys, and tuple retuen to caller
        format_res = json.dumps(response.json(), sort_keys=True, indent=4)
        leafs = [k for k in config.get('Cisco-IOS-XE-native:native').keys()]

        return config, leafs, format_res


class ApiCalls:

    def __init__(self):

        self.container = None
        self.leaf = None
        self.config_keys = None

    def request_container(self, username, password, device, container):
        """Get request leaf from config"""

        self.reset()
        self.container = container
        warnings.filterwarnings('ignore', message='Unverified HTTPS request')

        # Build uri based of button click which provides the leaf value
        uri = f"https://{device}/restconf/data/Cisco-IOS-XE-native:native/{self.container}"
        headers = {"Content-Type": 'application/yang-data+json', 'Accept': 'application/yang-data+json'}
        response = requests.get(uri, headers=headers, verify=False, auth=(username, password))

        # Format and return config to caller
        config = json.loads(response.text)
        format_res = json.dumps(response.json(), sort_keys=True, indent=4)

        try:
            leafs = [k for k in config.get(f'Cisco-IOS-XE-native:{self.container}').keys()]
            self.config_keys = leafs
        except AttributeError:
            leafs = ''
            self.config_keys = leafs

        return format_res, leafs, self.container

    def request_leaf(self, username, password, device, leaf):
        """Get request leaf from config"""

        self.leaf = leaf
        warnings.filterwarnings('ignore', message='Unverified HTTPS request')

        # Build uri based of button click which provides the leaf value
        uri = f"https://{device}/restconf/data/Cisco-IOS-XE-native:native/{self.container}/{self.leaf}"
        headers = {"Content-Type": 'application/yang-data+json', 'Accept': 'application/yang-data+json'}
        response = requests.get(uri, headers=headers, verify=False, auth=(username, password))

        # Format and return config to caller
        config = json.loads(response.text)
        format_res = json.dumps(response.json(), sort_keys=True, indent=4)

        return format_res, self.config_keys

    def reset(self):
        self.config_keys = None
