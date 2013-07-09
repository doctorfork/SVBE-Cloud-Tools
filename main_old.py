#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import models
import datetime
import pprint
import json
from google.appengine.ext import db


class MainHandler(webapp2.RequestHandler):
    def get(self):
	    #key_name = self.request.get('keyname')
	    key_name = self.request.get('foof')
	    p = models.Person.get_by_key_name(key_name)
	    self.response.write(str(db.to_dict(p)))
	    #OneOfUsPersonTest

class PersonTest(webapp2.RequestHandler):
    def get(self):
        p = models.Person(key_name = 'foof',full_name = "Dave Nielsen")
        p.full_name = "Dave Fork"
        p.birthday = datetime.date(1988,11,12)
        p.put()

        p = models.Person.get_by_key_name('foof')
        #p = Person.get(db.Key.from_path(u'Person', 'foof', _app=u'dev~active-bird-256'))
        p.email = 'fake@notreal.com'
        p.put()
        pprint.pprint(db.to_dict(p))

class OneOfUsPersonTest(webapp2.RequestHandler):
    def get(self):
        ooup = models.OneOfUsPerson(key_name = 'poof',full_name = "Alfred E. Newman")
        ooup.email = 'fake1@notreal.com'
        ooup.birthday = datetime.date(1988,11,12)
        # the start date is commented out to test the auto_now_add feature
        # ooup.start_date = datetime.date(1911,11,11)
        ooup.active = True
        if ooup.is_youth():
            independent = False
        ooup.roles = [models.Role.role_type.get_by_key_name('Assistant')]
        ooup.volunteer_hours = 0
        ooup.volunteer_points = 0
        ooup.put()
        #p = models.Person.get_by_key_name('poof')
        pprint.pprint(db.to_dict(ooup))
        self.response.write('End of OneOfUsTest')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/OneOfUsPersonTest', OneOfUsPersonTest),    
], debug=True)
