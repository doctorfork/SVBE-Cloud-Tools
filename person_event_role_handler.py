import webapp2
import models
import json
import collections
import utils
import google.appengine.ext.db as db

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
                'key': per.key(),
                'person': per.person,
                'role': per.role
                } for per in person_event_roles]))


class RemovePersonEventRoleHandler(webapp2.RequestHandler):
    def post(self, person_event_role_key):
        """Remove the PersonEventRole with the given key.

        This effectively unregisters a person from an event."""

        doomed_person_event_role = models.PersonEventRole.get(
            person_event_role_key)

        if not doomed_person_event_role:
            raise exc.HTTPNotFound('No person event role found with id' +
                                   person_event_role_key)
            
        db.delete(doomed_person_event_role)
