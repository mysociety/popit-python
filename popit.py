#!/usr/bin/env python
# -*- coding: utf-8 -*-

import slumber
from pprint import pprint

def build_url(instance = 'www', hostname = None, port = 80, api_version = ''):
	return 'http://' + '/'.join([instance.strip('/')+'.'+hostname.strip('/')+':'+str(port), 'api' , api_version])


url = build_url(instance = 'professors', hostname = '127-0-0-1.org.uk', port = 3000)

api = slumber.API(url, auth=('domoritz@gmail.com', 'tJo1zBum')).v1()

# Create
print("CREATE")
new = api.person.post({'name': 'Albert Keinstein'})
pprint(new)

id = new['result']['_id']

# Update
print("UPDATE")
result = api.person(id).put({"name": "Albert Einstein"})
pprint(result)

# Read
print("READ")
result = api.person(id).get()
pprint(result)

# Delete
print("DELETE")
result = api.person(id).delete()
pprint(result)

# META
print("META")
pprint(api.get())