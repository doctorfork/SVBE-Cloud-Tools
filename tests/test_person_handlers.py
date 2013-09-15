import datetime
import models
import unittest
import webtest
import webapp2
import json
from webob import exc

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


class TestCreatePersonHandler(unittest.TestCase):
  def setUp(self):
    self.tb = testbed.Testbed()
    self.tb.activate()
    self.tb.init_datastore_v3_stub()
    self.app = webtest.TestApp(app_definition.GetSVBEApp())
    role = models.Role(role_type=u'Fixer')
    role.put()
    
  def testPost(self):  
    # Trying to create a person without an email address should fail.
    response = self.app.post_json('/api/person', {'fullName': 'John Smith'}, 
                                  expect_errors=True)
    self.assertEqual(response.status_int, 400)  # Bad request
    response.mustcontain('must provide an email')
    
    # Minimal email validation is done.
    response = self.app.post_json('/api/person', 
                                  {'fullName': 'John Smith', 'email': 'foo'},
                                  expect_errors=True)
    self.assertEqual(response.status_int, 400)
    response.mustcontain('Not a valid email address')
    
    # This should work.
    response = self.app.post_json('/api/person', 
                                  {'fullName': 'John Smith', 'email': 'foo@bar.com',
                                   'birthdayYear': 1980, 'birthdayMonth': 1,
                                   'birthdayDay': 1, 'roles': []})
    self.assertEqual(response.status_int, 200)
    new_person = models.OneOfUsPerson.all().filter('full_name = ', 'John Smith').get()
    self.assertEquals(new_person.email, 'foo@bar.com')
    self.assertEquals(new_person.birthday, datetime.date(year=1980, month=1, day=1))
    
    # We shouldn't be able to save another person with the same email address.
    response = self.app.post_json('/api/person', 
                                  {'fullName': 'John Q Public', 'email': 'foo@bar.com',
                                   'birthdayYear': 1970, 'birthdayMonth': 1,
                                   'birthdayDay': 1, 'roles': []},
                                   expect_errors=True)
    self.assertEqual(response.status_int, 400)
    response.mustcontain('already a person with that email')
    
    # Specifying optional fields and roles also should work.
    response = self.app.post_json('/api/person', 
                                  {'fullName': 'John Q Public', 
                                   'email': 'baz@bar.com',
                                   'birthdayYear': 1970,
                                   'birthdayMonth': 1,
                                   'birthdayDay': 1, 
                                   'phoneNumber': '555-1212',
                                   'address': '123 Anywhere St',
                                   'mobileNumber': '666-5555',
                                   'roles': ['Fixer']})
    self.assertEqual(response.status_int, 200)
    new_person = models.OneOfUsPerson.all().filter('email = ', 'baz@bar.com').get()
    self.assertEqual(new_person.full_name, 'John Q Public')
    self.assertEqual(new_person.email, 'baz@bar.com')
    self.assertEqual(new_person.phone_number, '555-1212')
    self.assertEqual(new_person.address, '123 Anywhere St')
    self.assertEqual(new_person.mobile_number, '666-5555')

    # Person should be a Fixer.
    person_role = models.PersonRole.all().filter('person = ', new_person).get()
    self.assertEqual(person_role.role.role_type, 'Fixer')
    
    