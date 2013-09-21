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


class TestGetRoles(unittest.TestCase):
  def setUp(self):
    self.tb = testbed.Testbed()
    self.tb.activate()
    self.tb.init_datastore_v3_stub()
    self.app = webtest.TestApp(app_definition.GetSVBEApp())

  def tearDown(self):
    self.tb.deactivate()

  def testGet(self):
    p1 = models.Role(role_type="Test Role 1")
    p1.put()
    p2 = models.Role(role_type="Test Role 2")
    p2.put()
    roles_json = json.dumps([p1.role_type, p2.role_type])
      
    response = self.app.get('/api/roles/get')
    self.assertEqual(response.status_int, 200)
    self.assertEqual(response.normal_body, roles_json)
    self.assertEqual(response.content_type, 'application/json')
