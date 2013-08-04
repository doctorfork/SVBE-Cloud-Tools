import webapp2
import models
import json

class EventHandler(webapp2.RequestHandler):
    def get(self):
        """Writes the keys of all existing events to the response, as a JSON list."""
        self.response.write(json.dumps([e.key for e in models.Event.all()]))
        
    def get(self, event_key):
        """Writes a JSON representation of the event with the given key to the response.
        If there is no such event, writes code 404.
        """
        event = models.Event.get(event_key)
        if event:
            self.response.write(json.dumps(event))
        else:
            self.response.set_status(403, 'No event found with key %s' % key)
        
    def post(self):
        json = json.loads(self.request.body)
        event = models.Event(
            event_title=json['event_title'],
            start_time=json['start_time'],
            stop_time=json['stop_time'],
            setup_time=json['setup_time'],
            address=json['address'])
        event.put()
        
