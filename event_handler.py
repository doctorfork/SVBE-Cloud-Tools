import datetime
import time
import webapp2
from webob import exc
import models
import json
import re
import utils
from google.appengine.ext import db

def ParseTime(time_string):
    """Parses a time like '06:00 PM' and returns it as a datetime.timedelta"""
    time_re = re.compile('([0-9][0-9]):([0-9][0-9]) (AM|PM)')
    m = time_re.search(time_string)
    if not m:
        return None
    hour = int(m.group(1))
    minute = int(m.group(2))
    if m.group(3) == 'PM': hour += 12
    return datetime.timedelta(hours=hour, minutes=minute)

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
            
        event_date = datetime.datetime.strptime(
            event_json['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
        setup_time = event_date + ParseTime(event_json['setupTime'])
        start_time = event_date + ParseTime(event_json['startTime'])
        stop_time = event_date + ParseTime(event_json['stopTime'])
        
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
