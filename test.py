#!/usr/bin/env python
# -*- coding: utf-8 -*-

from popit_api import *
from slumber.exceptions import *
import logging
from pprint import pprint
from oktest import test, ok, NG, DIFF

DIFF = repr

logging.basicConfig(level = logging.WARN, format=FORMAT)

# load configuration
import config_test
keys = [x for x in dir(config_test) if not x.startswith("__")]
vals = map(lambda x: eval('config_test.'+x), keys)
conf = dict(zip(keys, vals))


class GetterSetterTest(object):

	## invoked only once before all tests
	@classmethod
	def before_all(cls):
		cls.p = PopIt(**conf)

	## invoked before each test
	def before(self):
		self.p = self.__class__.p

	@test("constructor should set right members")
	def _(self):
		for i, k in enumerate(keys):
			v = vals[i]
			ok(getattr(self.p, k)) == v

	@test("should raise error when non existent schema called")
	def _(self):
		def f():
			self.p.sadfhoi83jhk3323
		ok (f).raises(SchemaError)


class StatusTest(object):
	@classmethod
	def before_all(cls):
		cls.p = PopIt(**conf)

	def before(self):
		self.p = self.__class__.p

	@test("is_online should return true")
	def _(self):
		ok(self.p.is_online()) == True

	@test("api_version should return right version")
	def _(self):
		ok(self.p.get_api_version()) == conf['api_version']

	@test("get_url should return a string")
	def _(self):
		ok(self.p.get_url()).is_a(str)


class LazyTest(object):
	def before(self):
		self.p = PopIt(lazy=True)

	@test("lazy init should not set anything")
	def _(self):
		ok(self.p.initialized) == False
		

	@test("set_up should initialize the wrapper")
	def _(self):
		self.p.set_up(**conf)
		ok(self.p.initialized) == True

class AuthenticationTest(object):
	@classmethod
	def before_all(cls):
		wrong_conf = conf.copy()
		wrong_conf['password'] = '3h45hk345h'
		cls.p = PopIt(**wrong_conf)

	def before(self):
		self.p = self.__class__.p

	@test("wrong credentials should not fail when only reading")
	def _(self):
		def f():
			self.p.persons.get()
		NG (f).raises(HttpClientError)

	@test("wrong credentials should raise exception when saving")
	def _(self):
		
		def f():
			self.p.persons.post({'name': 'Albert Keinstein'})
		ok (f).raises(HttpClientError)


class CreateTest(object):
	@classmethod
	def before_all(cls):
		cls.p = PopIt(**conf)

	def before(self):
		self.p = self.__class__.p

	@test("can create person")
	def _(self):
		self.p.persons.post({'name': 'Albert Keinstein'})

	@test("can create organization")
	def _(self):
		self.p.organizations.post({'name': 'Space Party'})


class ReadUpdateDeleteTest(object):
	@classmethod
	def before_all(cls):
		cls.p = PopIt(**conf)

	def before(self):
		self.p = self.__class__.p
		new = self.p.persons.post({
			'name': 'Albert Keinstein', 
			'links': [{ 
				'url': 'http://www.wikipedia.com/AlbertEinstein',
       			'comment': 'Wikipedia'
       		}]
		})
		self.id = new['result']['id']

	@test("can read person's name")
	def _(self):
		result = self.p.persons(self.id).get()
		data = result['result'] 
		ok(data['name']) == "Albert Keinstein"

	@test("can read person's links")
	def _(self):
		result = self.p.persons(self.id).get()
		data = result['result']
		ok(data['links'][0]['url']) == "http://www.wikipedia.com/AlbertEinstein"
		ok(data['links'][0]['comment']) == "Wikipedia"

	@test("can edit person's name")
	def _(self):
		self.p.persons(self.id).put({"name": "Albert Einstein"})
		result = self.p.persons(self.id).get()
		ok(result['result']['name']) == "Albert Einstein"

	@test("can delete person")
	def _(self):
		result = self.p.persons(self.id).delete()
		ok(result) == True
		def f():
			result = self.p.persons(self.id).get()
		ok (f).raises(HttpClientError)

	@test("cannot delete person twice")
	def _(self):
		result = self.p.persons(self.id).delete()
		ok(result) == True
		
		def f():
			self.p.persons(self.id).delete()
		ok (f).raises(HttpClientError)

## invoke tests
if __name__ == '__main__':
	import oktest
	oktest.main()
