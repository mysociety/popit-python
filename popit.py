#!/usr/bin/env python
# -*- coding: utf-8 -*-

import slumber

def build_popit_api(instance = 'www', hostname = 'popit.mysociety.org', port = 80, api_version = 'v1', user = None, password = None):
	url = 'http://' + '/'.join([instance.strip('/')+'.'+hostname.strip('/')+':'+str(port), 'api'])
	slumber_api = slumber.API(url, auth=(user, password))
	api = getattr(slumber_api, api_version)()
	return api