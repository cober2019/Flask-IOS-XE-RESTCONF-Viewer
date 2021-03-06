
.. image:: https://travis-ci.com/cober2019/Flask-IOS-XE-RESTCONF-Viewer.svg?branch=main
    :target: https://travis-ci.com/cober2019/Flask-IOS-XE-RESTCONF-Viewer
.. image:: https://img.shields.io/badge/Fugi_IOS_XE_v16.09.04-passing-green
    :target: -
.. image:: https://img.shields.io/badge/Fugi_IOS_XE_v16.07.02-passing-green
    :target: -
.. image:: https://img.shields.io/badge/DevnetSandbox-passing-green
    :target: -
.. image:: https://img.shields.io/badge/RESTCONF-required-blue
    :target: -
.. image:: https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg
    :target: https://developer.cisco.com/codeexchange/github/repo/cober2019/Flask-IOS-XE-RESTCONF-Viewer


**RESTCONF Viewer**
====================


**Description:**
_________________

    View configuration using RESTCONF protocol. Available Modules:
    
        + ietf-interfaces:interfaces
        + Cisco-IOS-XE-native:native
        + ietf-interfaces:interfaces-state
        + Custom Module allows you to enter ANY Module. Compatibility required for device

**!!!Use Docker image(Ubuntu) instead of cloning to your own image. Fix in progress for file path issues!!!**

**Docker Link:**
        - https://hub.docker.com/r/cober2019/ios_xe_restconf_viewer
**Docker Commands:**
        - docker pull cober2019/ios_xe_restconf_viewer:latest
        - docker run -p 5000:5000  -d cober2019/ios_xe_restconf_viewer:latest
        
**Usage:**
___________

    + SideNav - Using side navigation for static modules. Once clicked, keys/lists will appear as buttons. Click a button to render configurationsfor keys/lists.
    + SideNav (Custom Query) - Click side navigation button. The next screen will have a URI and an input box. Insert module in the box, press enter. Navigate config with buttons.

**Outputs:**
____________

**Devnet:** 

If you dont have access to IOS-XE devices please use Devnet: https://developer.cisco.com/site/standard-network-devices/ (Credenitals Provided In Sandbox)
    
.. image:: https://github.com/cober2019/Flask-IOS-XE-RESTCONF-Viewer/blob/main/images/Devnet.PNG

**Main Page/Index**

.. image:: https://github.com/cober2019/Flask-IOS-XE-RESTCONF-Viewer/blob/main/images/Main.PNG

**Main page when value selected**

.. image:: https://github.com/cober2019/Flask-IOS-XE-RESTCONF-Viewer/blob/main/images/MainSelected.PNG

**Custom Query**

.. image:: https://github.com/cober2019/Flask-IOS-XE-RESTCONF-Viewer/blob/main/images/CustomQuery.PNG

**Custom Submit (Can produce different outputs)**

.. image:: https://github.com/cober2019/Flask-IOS-XE-RESTCONF-Viewer/blob/main/images/QuerySubmit.PNG

**YANG Converter (This feature is not available when using Windows)**

**Notice when using windows:**

.. image:: https://github.com/cober2019/Flask-IOS-XE-RESTCONF-Viewer/blob/main/images/NotForWindows.PNG

+ The program gets your device capabilities and compares it to the local YANG model directory. If a match, you will be able to view the model via dropdown menu.
+ Convert YANG files to standard tree, Dynamic Tree, and YIN. Outputs will be displayed when the "View Model" button is clicked.
+ Not all YANG models will produce an output. Some may produce a standard tree but not dynamic tree.

**YANG Menu:**

.. image:: https://github.com/cober2019/Flask-IOS-XE-RESTCONF-Viewer/blob/main/images/PYANGMenu.PNG

**Standard Tree:**

.. image:: https://github.com/cober2019/Flask-IOS-XE-RESTCONF-Viewer/blob/main/images/Standard.PNG

**Dynamic Tree:**

.. image:: https://github.com/cober2019/Flask-IOS-XE-RESTCONF-Viewer/blob/main/images/Dynamic.PNG

**YIN:**

.. image:: https://github.com/cober2019/Flask-IOS-XE-RESTCONF-Viewer/blob/main/images/yin.PNG




    
    
