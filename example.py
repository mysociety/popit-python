#!/usr/bin/env python
# -*- coding: utf-8 -*-

from popit import build_popit_api
from pprint import pprint

api = build_popit_api(instance = 'professors', hostname = '127-0-0-1.org.uk', port = 3000, user = 'domoritz@gmail.com', password = 'tJo1zBum')

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