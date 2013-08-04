import datetime
import webapp2
import models
import json
import re

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
    

class EventHandler(webapp2.RequestHandler):
    def get(self):
        """Writes the keys of all existing events to the response."""
        self.response.write(json.dumps([e.key for e in models.Event.all()]))
        
    def get(self, event_key):
        """Writes a JSON form of the event with the given key to the response.
        If there is no such event, writes code 404.
        """
        event = models.Event.get(event_key)
        if event:
            self.response.write(json.dumps(event))
        else:
            self.response.set_status(403, 'No event found with key %s' % key)
        
    def post(self):
        event_json = json.loads(self.request.body)
        
        event_date = datetime.datetime.strptime(
            event_json['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
        setup_time = event_date + ParseTime(event_json['setupTime'])
        start_time = event_date + ParseTime(event_json['startTime'])
        stop_time = event_date + ParseTime(event_json['stopTime'])
        
        event = models.Event(
            event_title=event_json['title'],
            setup_time=setup_time,
            start_time=start_time,
            stop_time=stop_time,
            address=event_json['address'])
        event.put()
        
        # Look up the roles in roles
        for role_name, count in event_json['roles'].iteritems():
            role = models.Role.get_by_key_name(role_name)
            event_role = models.EventRole(
                role=role, role_num=count, event=event)
            event_role.put()
