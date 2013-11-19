import webapp2
import models
import json
import collections
import utils

class GetPersonEventRolesSummaryByEventHandler(webapp2.RequestHandler):
    def get(self, event_key):
        """Fetches a summary of person event roles for an event, given the key.
        
        Returns a list of roles and counts, JSON serialized."""
        
        person_event_roles = models.PersonEventRole.gql(
            "WHERE event = KEY(:1)", event_key)
  
        roles_and_counts = collections.defaultdict(int)
        for per in person_event_roles:
            roles_and_counts[per.role.role_type] += 1
            
        self.response.write(json.dumps(dict(roles_and_counts.items())))

        
class GetPersonEventRolesByEventHandler(webapp2.RequestHandler):
    def get(self, event_key):
        """Fetches a list of person event roles for an event, given the key.
        
        Returns PersonEventRole objects with the Person and Role
        objects expanded, JSON serialized.
        """

        person_event_roles =  models.PersonEventRole.gql(
            "WHERE event = KEY(:1)", event_key)
        
        self.response.content_type = 'application/json'

        self.response.write(
            utils.CreateJsonFromModel([{
                'person': per.person,
                'role': per.role
                } for per in person_event_roles]))

