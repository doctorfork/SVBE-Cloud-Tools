import datetime
import models
import unittest
import webtest
import webapp2
import json

import app_definition
import person_handlers
import models

from google.appengine.ext import db
from google.appengine.ext import testbed


class TestGetPersonList(unittest.TestCase):
  def setUp(self):
    self.tb = testbed.Testbed()
    self.tb.activate()
    self.tb.init_datastore_v3_stub()
    self.app = webtest.TestApp(app_definition.GetSVBEApp())

  def tearDown(self):
    self.tb.deactivate()

  def testGet(self):
    p = models.OneOfUsPerson(full_name='John Smith')
    p.put()
    person_json = json.dumps([p.ToDict()])
      
    response = self.app.get('/api/person/list')
    self.assertEqual(response.status_int, 200)
    self.assertEqual(response.normal_body, person_json)
    self.assertEqual(response.content_type, 'application/json')


class TestGetPersonByPartialName(unittest.TestCase):
  def setUp(self):
    self.tb = testbed.Testbed()
    self.tb.activate()
    self.tb.init_datastore_v3_stub()
  
    self.app = webtest.TestApp(app_definition.GetSVBEApp())

  def testGet(self):  
    person1 = models.OneOfUsPerson(full_name='John Smith')
    person1.put()
    person2 = models.OneOfUsPerson(full_name='John Paul Jones')
    person2.put()
    
    role1 = models.Role(role_type='Fixer')
    role1.put()
    role2 = models.Role(role_type='Breaker')
    role2.put()
    
    # Person1 is a Fixer and a Breaker
    models.PersonRole(person=person1, role=role1).put()
    models.PersonRole(person=person1, role=role2).put()
    
    # Person2 is just a Fixer.
    models.PersonRole(person=person2, role=role1).put()
    
    # Try the common first name. We should get both people.
    response = self.app.get('/api/person/by_name/john')
    self.assertEqual(response.status_int, 200)
    self.assertEqual(response.content_type, 'application/json')
    response_obj = json.loads(response.normal_body)
    
    self.assertTrue(isinstance(response_obj, list))
    self.assertEqual(len(response_obj), 2)
    self.assertEqual(response_obj[0]['full_name'], 'John Smith')
    self.assertEqual(response_obj[1]['full_name'], 'John Paul Jones')
    
    # Both people's roles should also be included.
    self.assertEqual(len(response_obj[0]['roles']), 2)
    self.assertEqual(response_obj[0]['roles'][0]['role_type'], 'Fixer')
    self.assertEqual(response_obj[0]['roles'][1]['role_type'], 'Breaker')
    
    self.assertEqual(len(response_obj[1]['roles']), 1)
    self.assertEqual(response_obj[1]['roles'][0]['role_type'], 'Fixer')
    
    # Now try a different prefix.
    response = self.app.get('/api/person/by_name/john%20paul')
    self.assertEqual(response.status_int, 200)
    response_obj = json.loads(response.normal_body)
    self.assertEqual(len(response_obj), 1)
    self.assertEqual(response_obj[0]['full_name'], 'John Paul Jones')

