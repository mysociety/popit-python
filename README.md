#popit-python #

Python bindings to connect to the [PopIt](https://github.com/mysociety/popit) API. You can *create*, *read*, *update* and *delete* any items from PopIt through this Binding. Actually, this is only a convenient wrapper around [PopIt's](https://github.com/mysociety/popit) RESTful API.


## How do I use this when I want to... ##

First, you'll need to get the PopIt binding object. Make sure PopIt as running and that you have all the information you need. Then get the object use the `PopIt` constructor. 

	from popit import PopIt
	
    api = PopIt(instance = 'professors', \
    	hostname = '127-0-0-1.org.uk', port = 3000, api_version = 'v1', \
        user = 'test@test.co.uk', password = 'tJo1zBum')

* `instance` Name of the instance you created. There can be more than one for one installation.
* `hostname` The Hostname of the PopIt server.
* `api_version` The version of the PopIt API. Since there may be changes in the way you access the data in PopIt you want to have a stable API version. We recommend that you use the latest version, if possible.  
* `port` The port, PopIt is accessible through. This probably is `80` or `3000`. `80` is the default.
* `user` Your username. You will not be able to write anything if you haven't provided your username and password.
* `password` The password for the user.

### …create something? ###

This PopitWrapper lets you easily create a new item by name. This can be a `person`, `organisation` or `position`. There may be other options that you can find in the [PopIt API documentation](https://github.com/mysociety/popit/wiki/API-Overview). 

    new = api.person.post({'name': 'Albert Keinstein'})
    print(new)
    
	# get the id of the newly created item
    id = new['result']['_id']


### …read something ###

If you want to get a single item from PopIt, use `name(id)`.

	# you need a valid ID for example from the create process.
    result = api.person(id).get()
    print(result)
    
To get all Items from a kind, use `name`.

    results = api.person.get()
    print(results)

### …update something? ###

    result = api.person(id).put({"name": "Albert Einstein"})
    print(result)
    
### …delete something? ###

    successful = api.person(id).delete()
    
### …get an error? ###

This is easy. This wrapper helps you with various error messages that help you get the wrapper working. Here are some explanations for error messages. 

**HttpClientError: Client Error 404**
You are looking for an item that does not exist. Please provide a valid id. This Error can happen when you ty to *create*, *read*, *update* or *delete* an item. 

**HttpClientError: Client Error 401**
You wanted to *create*, *update* or *delete* an item but provided a wrong username or password. 

*Note*: You won't see this error before you actually try to modify any data. 

**SchemaError: 'foo does not exist. Try one of these schemas: organisation, position, person.'**
This happens when you try to get data from a schema that does not exist (in this case `foo`). The available schemas are determined when you first create the api object. 

### …get more information abou what's going on internally? ###

Enable logging. 

    logging.basicConfig(level = logging.WARN	, format=FORMAT) 

## Requirements ##

* slumber (`pip install slumber`)

## How to run the tests ##

* Copy the config_example.py to config_test.py
* Change the entries in the testconfig.py to you local test server
* Install [`oktest`](http://www.kuwata-lab.com/oktest/ "Website of oktest") (`pip install oktest`)
* run `python test.py`
