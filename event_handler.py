import datetime
import time
import webapp2
from webob import exc
import models
import json
import re
import utils
from google.appengine.ext import db


class EventListHandler(webapp2.RequestHandler):
    def get(self):
        """Writes the all existing events to the response."""
        #TODO(AttackCowboy):make role serializable-we removed ToDictWithRoles 
        print models.Event.all()[0]
        self.response.write(utils.CreateJsonFromModel(models.Event.all()))


class EventHandler(webapp2.RequestHandler):
    def get(self, event_key):
        try:
            e = models.Event.get(event_key)
        except db.BadKeyError:
            raise exc.HTTPNotFound('Event not found')
        self.response.write(utils.CreateJsonFromModel(e))
            
        
    def post(self):
        event_json = json.loads(self.request.body)
        
        if 'key' in event_json:
            event = models.Event.get(event_json['key'])
        else:
            event = models.Event()
            
        event_date = utils.ParseISODate(event_json['date']).date()
        setup_time = datetime.datetime.combine(
            event_date,
            utils.ParseISODate(event_json['setupTime']).time())
        start_time = datetime.datetime.combine(
            event_date,
            utils.ParseISODate(event_json['startTime']).time())
        stop_time = datetime.datetime.combine(
            event_date,
            utils.ParseISODate(event_json['stopTime']).time())
        
        event.event_title=event_json['title']
        event.setup_time=setup_time
        event.start_time=start_time
        event.stop_time=stop_time
        event.address=event_json['address']
        event.put()
        
        # Look up the roles in roles
        for role_name, count in event_json['roles'].iteritems():
            role = models.Role.get_by_key_name(role_name)
            if not role:
                raise exc.HTTPNotFound('Role not found')
            event_role = models.EventRole(
                role=role, role_num=count, event=event)
            event_role.put()
        #TODO(AttackCowboy):populate form from json--Steal from populate with test data
        self.response.write(utils.CreateJsonFromModel(event))
        

class RegisterPersonHandler(webapp2.RequestHandler):
    def post(self):
        keys_json = json.loads(self.request.body)
        person = models.OneOfUsPerson.get(keys_json['personKey'])
        if not person: 
            raise exc.HTTPNotFound('Person not found')
            
        event = models.Event.get(keys_json['eventKey'])
        if not event:
            raise exc.HTTPNotFound('Event not found')
            
        person_role = models.PersonRole.gql(
            "WHERE person = KEY(:1) and role = KEY(:2)",
            keys_json['personKey'], keys_json['roleKey']).get()
        if not person_role:
            raise exc.HTTPNotFound('Role with key %r not found' % keys_json['roleKey'])

        p = models.PersonEventRole(
            person=person, event=event, role=person_role.role)
        p.put()
