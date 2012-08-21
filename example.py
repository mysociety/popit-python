#!/usr/bin/env python
# -*- coding: utf-8 -*-

from popit import PopIt
from pprint import pprint

def main():
	api = PopIt(instance = 'professors', hostname = '127-0-0-1.org.uk', port = 3000, user = 'test@test.co.uk', password = 'tJo1zBum')

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

	# read all
	results = api.person().get()
	pprint(results)

	# Delete
	print("DELETE")
	result = api.person(id).delete()
	pprint(result)

if __name__ == '__main__':
	main()