#!/usr/bin/env python
# -*- coding: utf-8 -*-

import slumber
import logging
from pprint import pprint

FORMAT = "[PopIt | %(levelname)s] %(message)s"
log = logging.getLogger(__name__)

if __name__ == '__main__':
	logging.basicConfig(level = logging.DEBUG, format=FORMAT)
	log.setLevel(logging.DEBUG)


class Method(object):
    def __init__(self, client, method_name):
        self.client = client
        self.method_name = method_name

    def __getattr__(self, key):
        return Method(self.client, '.'.join((self.method_name, key)))

    def __call__(self, *args, **kwargs):
        print self.method_name, args, kwargs
        return self.client.__call__(*args, **kwargs)

class PopIt(object):
	def __init__(self, **args):
		defaults = {
			'instance': 'www',
			'hostname': 'popit.mysociety.org',
			'port': 80,
			'api_version': 'v1',
			'user': None,
			'password': None
		}
		defaults.update(args)
		self.__dict__.update(defaults)

		self.api = self.__api()
		self.schemas = self.__schemas()

	def getGenericApi(self):
		return self.api

	def __schemas(self):
		schemas_dict = self.api.get()['meta'];
		schemas = [x[:x.find('_api_url')] for x in schemas_dict.keys() if x.find('_api_url') > 0]
		log.debug('Avalable schemas: ' + str(schemas))
		return schemas

	def __getattr__(self, key):
		if key in self.schemas:
			return self.api.__call__(key)

	def __api(self):
		slumber = self.__slumber_api()
		return getattr(slumber, self.api_version)()

	def __slumber_api(self):
		url = self.__url()
		return slumber.API(url, auth=(self.user, self.password))

	def __url(self):
		url = 'http://{instance}.{hostname}:{port}/api'.format(instance = self.instance, hostname = self.hostname, port = self.port)
		log.debug('PopIt Url: {}'.format(url))
		return url