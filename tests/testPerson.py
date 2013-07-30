import datetime
import models
import unittest

from google.appengine.ext import db
from google.appengine.ext import testbed


class TestPerson(unittest.TestCase):

  def setUp(self):
    self.tb = testbed.Testbed()
    self.tb.activate()
    self.tb.init_datastore_v3_stub()

  def tearDown(self):
    self.tb.deactivate()

  def testCreate(self):
    p = models.Person(full_name='John Smith')
    p.put()
    self.assertEqual(1, len(models.Person.all().fetch(2)))

  def testAge(self):
    p = models.Person(full_name='John Smith')
    years_19 = datetime.timedelta(365 * 19 + 5)
    p.birthday = datetime.date.today() - years_19

    self.assertEqual(p.age, 19)
