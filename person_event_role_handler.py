"""HTTP handlers for methods that deal with PersonEventRoles."""

# Class has no __init__ method (no-init)
# pylint: disable=W0232
# Class 'Event' has no 'get' member (no-member)
# pylint: disable=E1101
# Too few public methods (1/2) (too-few-public-methods)
# pylint: disable=R0903
# Method could be a function (no-self-use)
# pylint: disable=R0201

import webapp2 # pylint: disable=F0401
from webob import exc
import models
import json
import collections
import utils
import google.appengine.ext.db as db # pylint: disable=F0401

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

        person_event_roles = models.PersonEventRole.gql(
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

HANDLERS = [
    ('/api/person_event_roles/get_summary_by_event/(.+)',
     GetPersonEventRolesSummaryByEventHandler),
    ('/api/person_event_roles/get_by_event/(.+)',
     GetPersonEventRolesByEventHandler),
    ('/api/person_event_roles/remove/(.+)',
     RemovePersonEventRoleHandler),
]
