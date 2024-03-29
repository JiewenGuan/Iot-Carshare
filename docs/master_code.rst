Master Code Documentation
*************************
The Master Pi consists of multiple modules due to the need for it to perform three primary functions.

- Serve the website for creating bookings.
- Accept socket connection from the Agent Pis and return the requests appropriately.
- Make an API available for querying the hosted database by the website or the socket connection.

The api/database and website are contained within two directories - carapi and website. These can based
hosted in separate locations, as the website access the datavase via an API.

AgentPi/socketresponder.py
==========================

.. automodule:: AgentPi.socketresponder
    :members:

AgentPi/masterpiresponder.py
============================

.. automodule:: AgentPi.masterpiresponder
    :members:

carapi/app/models.py
====================
This module defines the data models that are usedby the database and served
by the API. There are three clases defining the three key data objects,
which are representative of the tables i the database.

.. automodule:: MasterPi.carapi.app.models
    :members:

carapi/app/routes.py
====================
A list of function routes that perform database query logic,
and update the database as needed. For inherent functionality, see 
each individual function, but essentially they serve to answer
any query deemed relevant in the API by the website or the Master serving
the socket queries from an Agent. This is achieved using parameterised SQL.

.. automodule:: MasterPi.carapi.app.routes
    :members:

carapi/app/env.py
=================
This module is predominantly auto-populated during installation of dependencies.

.. automodule:: MasterPi.carapi.app.migrations.env
    :members:

carapi/carapi.py
================
Key to the database, this module creates a shell context that adds
the models and the database instance to the shell session. The inherent 
decorator registers the items returned. In this case we are returning 
a dictionary that references the tables in the database and the database
itself.

.. automodule:: MasterPi.carapi.carapi
    :members:

carapi/config.py
================

.. automodule:: MasterPi.carapi.config
    :members:

carapi/templates
================
This folder contains multiple html documents that serve to template the pages
that are generated throughout the website. They predominantly populate with
dynamic content as returned by either session information or database API calls
that populate with the application of conditional statements.

Importantly, the base.html file defines a template for inheritance into 
multiple pages to ensure conformity to the style across all pages.

forms.py
========

This module contains classes that define the structure of FlaskForms, both the data they record and importantly the conditions
in which the form is successfully submitted such as in the event of a username collission. 
It is predominantly the conditional code internal to these classes that performs the validation of user inputs.

.. automodule:: MasterPi.website.app.forms
    :members:

models.py
=========

This module defines the data models that are used by the website via classes, namely the User and the Car.

.. automodule:: MasterPi.website.app.models
    :members:

routes.py
=========
This module contains the templates for structuring dynamic content
on the pages. It returns objects that in turn render html based on
the status of numerous factors such as the user currently validated.

- :func:`auth_admin(f)`
- :func:`index()`
- :func:`login()`
- :func:`dashboard()`
- :func:`admin_user()`
- :func:`car_history(id)`
- :func:`car_edit(id)`
- :func:`car_report(id)`
- :func:`add_car()`
- :func:`user_history(id)`
- :func:`user_edit(id)`
- :func:`register()`
- :func:`logout()`
- :func:`book_car_request(id)`
- :func:`my_bookings()`
- :func:`car_info(id)`
- :func:`cancel_booking(id)`
- :func:`location(id)`
- :func:`make_select_list(arr)`

These are prefixed with decorators which are used to enforce certain validation
when particular pages are loaded. See the individual functions for further details.
These mappings as such are predominantly used to create forms, passing them to the
template for rendering.

.. automodule:: MasterPi.website.app.routes
    :members:

config.py
=========

.. automodule:: MasterPi.website.config
    :members:

website.py
==========
Entry point. No classes to instantiate.

.. automodule:: MasterPi.website.website
    :members: