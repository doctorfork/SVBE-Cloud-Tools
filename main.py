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
#	    key_name = self.request.get('keyname')
#	    p = models.Person.get_by_key_name(key_name)
#	    self.response.write(str(db.to_dict(p)))
        self.response.write('Hello world!')

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
        last_name_test =  ooup.last_name == "Newman"
        if last_name_test:
            self.response.write('Passed: last name test')
        else:
            self.response.write('Failed: last name test')
        
            

        # ooup.email = 'fake1@notreal.com'
        # ooup.birthday = datetime.date(1988,11,12)
        # ooup.address = db.PostalAddress('1600 Ampitheater Pkwy., Mountain View, CA')

        


##        if ooup.is_youth():
##            ooup.independent = False
##        else:
##            ooup.independent = True
##
##        assist_role = models.Role.get_or_insert('Assistant',role_type = 'Assistant')
##        assist_role.put()
##        ooup.roles = [assist_role.key()]
##        ooup.volunteer_hours = 0
##        ooup.volunteer_points = 0
##        ooup.put()
##        #p = models.Person.get_by_key_name('poof')
##        pprint.pprint(db.to_dict(ooup))
##        self.response.write('End of OneOfUsPersonTest')

class AttendenceTest(webapp2.RequestHandler):
    def get(self):
        leader = models.OneOfUsPerson.get_or_insert('poof',full_name = "Alfred E. Newman")
        leader.put()
        event = models.Event.get_or_insert('roof',date = datetime.date(2013,7,14),
                                            event_leader = leader)
        event.put()
        assist_role = models.Role.get_or_insert('Assistant',role_type = 'Assistant')
        assist_role.put()
        
        person_at_event_doing_role = models.PersonEventRole(person = leader, event = event, 
                                                            role = assist_role)
        person_at_event_doing_role.put()
        self.response.write(db.to_dict(person_at_event_doing_role))



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/OneOfUsPersonTest', OneOfUsPersonTest),
    ('/AttendenceTest', AttendenceTest)    
], debug=True)
