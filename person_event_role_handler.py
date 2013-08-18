import webapp2
import models
import json

class GetPersonEventRolesByEventHandler(webapp2.RequestHandler):
    def get(self, event_key):
        """Fetches a list of person event roles for an event, given the key.
        
        Returns a list of roles and counts, JSON serialized."""
        event = models.Event.get(event_key)
        if not event: 
            self.error(404)
            return
    
        self.response.write(json.dumps(
            [(event_role.role.ToDict(), event_role.role_num) 
             for event_role in event.eventrole_set.run()]))