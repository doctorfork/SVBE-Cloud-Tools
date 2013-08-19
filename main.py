import webapp2
import models
import datetime
import pprint
import json
from google.appengine.ext import db

import event_handler
import event_role_handler
import person_event_role_handler
import person_handlers

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # Redirect to the event picker, which lets a trained operator
        # register people for events.
        self.redirect('/static/html/index.html')


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


class GetRoles(webapp2.RequestHandler):
    def get(self):
        """Returns all the valid roles."""
        self.response.write(json.dumps([r.role_type for r in models.Role.all()]))
               
class LoadRoles(webapp2.RequestHandler):
    def get(self):
        # Role Names to put into datastore:
        role_names = [
            "Accountant",
            "Announcements",
            "Apprentice",
            "Cleaning",
            "Course Instructor",
            "Delivery",
            "Director",
            "Event Leader",
            "Event Setup",
            "Event Wrapup",
            "Food Coordinator",
            "Homework Mechanic",
            "Intake",
            "Inventory",
            "Mechanic",
            "Mentor",
            "Officer",
            "Orientation",
            "Outgoing Donations",
            "Photographer",
            "Prequal",
            "President",
            "Record Keeper",
            "Recycling",
            "Registration",
            "Sales",
            "Secretary",
            "Treasurer",
            "Volunteer Coordinator",]
        for r in role_names:
            role = models.Role(key_name=r,role_type=r)
            role.put()
            self.response.write('Added role: %s <br/>' % r)
        self.response.write('Roles Loaded.<br/>')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/OneOfUsPersonTest', person_handlers.OneOfUsPersonTest),
    ('/AttendenceTest', AttendenceTest),
    ('/LoadRoles', LoadRoles),
    ('/api/event', event_handler.EventHandler),
    ('/api/event/list', event_handler.EventListHandler),
    ('/api/event/register_person', event_handler.RegisterPersonHandler),
    ('/api/event/(.+)', event_handler.EventHandler),
    ('/api/person/list', person_handlers.GetPersonList),
    ('/api/person', person_handlers.PersonHandler),
    ('/api/person/by_name/(.+)', person_handlers.GetPersonByPartialName),
    ('/api/roles/get', GetRoles),
    ('/api/event_roles/get_by_event/(.+)', 
     event_role_handler.GetEventRolesByEventHandler),
    ('/api/person_event_roles/get_by_event/(.+)',
     person_event_role_handler.GetPersonEventRolesByEventHandler),
    ], debug=True)
