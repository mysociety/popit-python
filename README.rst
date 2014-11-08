popit-python
============

Python bindings to connect to the `PopIt <https://github.com/mysociety/popit>`_ API. You can *create*, *read*, *update* and *delete* any items from PopIt through this Binding. Actually, this is only a convenient wrapper around `PopIt's <https://github.com/mysociety/popit>`_ RESTful API.

Installation
------------
PopIt-Python is available as a module on PyPi, to install, simply run::

    pip install PopIt-Python

Alternatively, clone this repo and install as you see fit.

How do I use this when I want to...
-----------------------------------

First, you'll need to get the PopIt binding object. Make sure PopIt as running and that you have all the information you need. Then get the object use the `PopIt` constructor. ::

    from popit_api import PopIt

    api = PopIt(instance='professors',
                hostname='127-0-0-1.org.uk',
                port=3000,
                api_version='v0.1',
                api_key='f093903b7a1aa9688b36241502beadc7')

* ``instance`` Name of the instance you created. There can be more than one for one installation.
* ``hostname`` The hostname of the PopIt server.
* ``api_version`` The version of the PopIt API. Since there may be changes in the way you access the data in PopIt you want to have a stable API version. We recommend that you use the latest version, if possible.
* ``port`` The port that PopIt is listening on. This probably is ``80`` or ``3000``. ``80`` is the default.
* ``api_key`` This is the API key you can request by clicking
  'Get API key' in the PopIt web interface for your instance, as
  `described in the documentation <http://popit.poplus.org/docs/api/#authentication>`_.

If you're still using an older PopIt instance and have not upgraded
your account for the new, more secure authentication system, instead
of ``api_key`` you can supply ``user`` and ``password``:

* ``user`` Your username, the email address that you created the instance with
* ``password`` The password you were emailed when creating the instance

…create something?
~~~~~~~~~~~~~~~~~~

This PopitWrapper lets you easily create a new item by name. This can be a ``person``, ``organization`` or ``position``. There may be other options that you can find in the `PopIt API documentation <http://popit.poplus.org/docs/api/>`_. ::

    new_person = api.persons.post({'name': 'Albert Keinstein'})
    print(new_person)

    # get the id of the newly created item
    id = new_person['result']['_id']


…read something
~~~~~~~~~~~~~~~~

If you want to get a single item from PopIt, use ``name(id)``. ::

    # you need a valid ID for example from the create process.
    person = api.persons(id).get()
    print(person)

To get all Items from a kind, use `get()`. ::

    people = api.persons.get()
    print(people)

…update something?
~~~~~~~~~~~~~~~~~~

::

    result = api.persons(id).put({"name": "Albert Einstein"})
    print(result)

…delete something?
~~~~~~~~~~~~~~~~~~

::

    successfully_deleted = api.persons(id).delete()

…get an error?
~~~~~~~~~~~~~~

This is easy. This wrapper helps you with various error messages that help you get the wrapper working. Here are some explanations for error messages.

**HttpClientError: Client Error 404**
You are looking for an item that does not exist. Please provide a valid id. This Error can happen when you ty to *create*, *read*, *update* or *delete* an item.

**HttpClientError: Client Error 401**
You wanted to *create*, *update* or *delete* an item but provided a wrong username or password.

*Note*: You won't see this error before you actually try to modify any data.

**SchemaError: 'foo does not exist. Try one of these schemas: organizations, positions, persons.'**
This happens when you try to get data from a schema that does not exist (in this case ``foo``). The available schemas are determined when you first create the api object.

…get more information about what's going on internally?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enable logging. ::

    logging.basicConfig(level=logging.WARN, format=FORMAT)

Requirements
------------

If you don't use pip to install the module, you'll also need:

* requests (``pip install requests==0.14.2``)
* slumber (``pip install slumber``)

Note you need to specify the version of requests, because slumber does not and it is not compatible with requests >= 1.0.0 yet. It also needs to be specified and installed before slumber, else slumber's requirements.txt will override it and your specified version won't be installed.

How to run the tests
--------------------

* Copy the file ``config_example.py`` to ``config_test.py``
* Change the entries in ``config_test.py`` to refer to your local test server
* Install `oktest <http://www.kuwata-lab.com/oktest/>`_ (``pip install oktest``)
* Make sure PopIt is running. You cannot test this wrapper without a running PopIt instance.
* run ``python test.py``
