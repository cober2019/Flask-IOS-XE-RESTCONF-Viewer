
.. image:: https://travis-ci.com/cober2019/Flask-IOS-XE-RESTCONF-Viewer.svg?branch=main
    :target: https://travis-ci.com/cober2019/Flask-IOS-XE-RESTCONF-Viewer
.. image:: https://img.shields.io/badge/Fugi_IOS_XE_v16.09.04-passing-green
    :target: -
.. image:: https://img.shields.io/badge/Fugi_IOS_XE_v16.07.02-passing-green
    :target: -
.. image:: https://img.shields.io/badge/RESTCONF-required-blue
    :target: -
    

**RESTCONF Viewer**
====================


**Description:**
_________________

    View configuration using RESTCONF protocol. Available Modules:
    
        + ietf-interfaces:interfaces
        + Cisco-IOS-XE-native:native
        + ietf-interfaces:interfaces-state
        + Custom Module allows you to enter ANY Module. Compatibility required for device

**Docker Link:**
        - https://hub.docker.com/r/cober2019/ios_xe_restconf_viewer
**Docker Commands:**
        - docker pull cober2019/ios_xe_restconf_viewer
        - docker run -p 5000:5000  -d cober2019/ios_xe_restconf_viewer:v1.0
        
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





    
    
