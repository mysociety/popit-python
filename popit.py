#!/usr/bin/env python
# -*- coding: utf-8 -*-

import slumber
import logging
from pprint import pprint
from requests.exceptions import *
from slumber.exceptions import *

FORMAT = "[PopIt | %(levelname)s] %(message)s"
log = logging.getLogger(__name__)

if __name__ == '__main__':
	logging.basicConfig(level = logging.DEBUG, format=FORMAT)
	log.setLevel(logging.DEBUG)

class SchemaError(NameError):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class NotInitializedError(RuntimeError):
	def __str__(self):
		return "The PopIt api wrapper is not yet initialized. Check if PopIt is running and then retry."
		

class PopIt(object):
	def __init__(self, lazy = False, **args):
		""" Lazy means that you have to call PopIt(true) AND then set_up()
		"""
		self.initialized = False
		if not lazy:
			self.set_up(**args)

	def set_up(self, **args):
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

		self.initialized = True

	def __str__(self):
		if self.initialized:
			return str(self.__url()+'/'+self.api_version)
		else:
			return str(self)

	def get_url(self):
		if self.initialized:
			return self.__url()
		else:
			raise NotInitializedError()

	def get_api_version(self):
		if self.initialized:
			return self.api_version
		else:
			raise NotInitializedError()

	def is_online(self):
		if self.initialized:
			try:
				# protocol ping
				self.api.get()
			except ConnectionError, e:
				return False
			else:
				return True
		else:
			raise NotInitializedError()

	def getGenericApi(self):
		return self.api

	def __getattr__(self, key):
		if not self.initialized:
			raise NotInitializedError()
		if key in self.schemas:
			return self.api.__call__(key)
		else:
			raise SchemaError('{} does not exist. Try one of these schemas: {}.'.format(key, ', '.join(self.schemas)))

	def __schemas(self):
		schemas_dict = self.api.get()['meta'];
		schemas = [x[:x.find('_api_url')] for x in schemas_dict.keys() if x.find('_api_url') > 0]
		log.debug('Available schemas: {0}'.format(schemas))
		return schemas

	def __api(self):
		slumber = self.__slumber_api()
		return getattr(slumber, self.api_version)()

	def __slumber_api(self):
		url = self.__url()
		return slumber.API(url, auth=(self.user, self.password))

	def __url(self):
		url = 'http://{instance}.{hostname}:{port}/api'.format(instance = self.instance, hostname = self.hostname, port = self.port)
		log.debug('PopIt Url: {0}'.format(url))
		return url