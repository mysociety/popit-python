#!/usr/bin/env python
# -*- coding: utf-8 -*-

from popit import *
from slumber.exceptions import *
import logging
from pprint import pprint
from oktest import test, ok
import oktest

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

	@test("constructor should set right memembers")
	def _(self):
		for i, k in enumerate(keys):
			v = vals[i]
			ok(getattr(self.p, k)) == v

	@test("should raise error when non existent schema called")
	def _(self):
		def f():
			self.p.sadfhoi83jhk3323
		ok (f).raises(SchemaError)


class CreateTest(object):
	@classmethod
	def before_all(cls):
		cls.p = PopIt(**conf)

	def before(self):
		self.p = self.__class__.p

	@test("can create person")
	def _(self):
		self.p.person.post({'name': 'Albert Keinstein'})


class UpdateTest(object):
	@classmethod
	def before_all(cls):
		cls.p = PopIt(**conf)

	def before(self):
		self.p = self.__class__.p
		new = self.p.person.post({'name': 'Albert Keinstein'})
		self.id = new['result']['_id']

	@test("can edit person's name")
	def _(self):
		self.p.person(self.id).put({"name": "Albert Einstein"})
		result = self.p.person(self.id).get()
		ok(result['result']['name']) == "Albert Einstein"
		
class DeleteTest(object):
	@classmethod
	def before_all(cls):
		cls.p = PopIt(**conf)

	def before(self):
		self.p = self.__class__.p
		new = self.p.person.post({'name': 'Albert Keinstein'})
		self.id = new['result']['_id']

	@test("can delete person")
	def _(self):
		result = self.p.person(self.id).delete()
		ok(result) == True
		def f():
			result = self.p.person(self.id).get()
		ok (f).raises(HttpClientError)

## invoke tests
if __name__ == '__main__':
	oktest.main()