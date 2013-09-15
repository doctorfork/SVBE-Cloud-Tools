import datetime
import models
import unittest
import webtest
import webapp2
import json

import person_handlers
import models

from google.appengine.ext import db
from google.appengine.ext import testbed

class TestGetPersonList(unittest.TestCase):
  def setUp(self):
    self.tb = testbed.Testbed()
    self.tb.activate()
    self.tb.init_datastore_v3_stub()
    
    app = webapp2.WSGIApplication([('/', person_handlers.GetPersonList)])
    self.testapp = webtest.TestApp(app)

  def tearDown(self):
    self.tb.deactivate()

  def testGet(self):
      p = models.OneOfUsPerson(full_name='John Smith')
      p.put()
      person_json = json.dumps([p.ToDict()])
      
      response = self.testapp.get('/')
      self.assertEqual(response.status_int, 200)
      self.assertEqual(response.normal_body, person_json)
      self.assertEqual(response.content_type, 'application/json')

# class TestGetPersonByPartialName(unittest.TestCase):
#     def setUp(self):
#       self.tb = testbed.Testbed()
#       self.tb.activate()
#       self.tb.init_datastore_v3_stub()
# 
#       app = webapp2.WSGIApplication([('/', person_handlers.GetPersonList)])
#       self.testapp = webtest.TestApp(app)