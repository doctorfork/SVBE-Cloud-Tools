"""Handlers for event-related functionality

Handles creating events, viewing lists of events, and viewing details
of single events.
"""

# Class has no __init__ method (no-init)
# pylint: disable=W0232
#
# Instance of 'EventListHandler' has no 'response' member (no-member)
# pylint: disable=E1101
#
# Too few public methods (1/2) (too-few-public-methods)
# pylint: disable=R0903

from google.appengine.ext import db  # pylint: disable=F0401
from webob import exc
import collections
import datetime
import json
import models
import re
import time
import utils
import webapp2  # pylint: disable=F0401

class EventListHandler(webapp2.RequestHandler):
    def get(self):
        """Writes the all existing events to the response."""
        self.response.content_type = 'application/json'
        self.response.write(
            utils.CreateJsonFromModel([obj for obj in models.Event.all()]))


class EventHandler(webapp2.RequestHandler):
    def get(self, event_key):
        """Handles retrieving a single event."""
        try:
            event = models.Event.get(event_key)
        except db.BadKeyError:
            raise exc.HTTPNotFound('Event not found')
        self.response.write(utils.CreateJsonFromModel(event))


    def post(self):
        """Handles creating a new event, or editing an existing one."""
        event_json = json.loads(self.request.body)

        if 'key' in event_json:
            event = models.Event.get(event_json['key'])
        else:
            event = models.Event()

        start = utils.ParseISODate(event_json['startTime'])
        start_date = start.date()
        setup_time = datetime.datetime.combine(
            start_date,
            utils.ParseISODate(event_json['setupTime']).time())

        stop_time = datetime.datetime.combine(
            start_date,
            utils.ParseISODate(event_json['stopTime']).time())

        event.event_title = event_json['eventTitle']
        event.setup_time = setup_time
        event.start_time = start
        event.stop_time = stop_time
        event.address = event_json['address']
        event.put()

        # Look up the roles in roles
        for role_name, count in event_json['roles'].iteritems():
            role = models.Role.get_by_key_name(role_name)
            if not role:
                raise exc.HTTPNotFound('Role not found')
            event_role = models.EventRole(
                role=role, role_num=count, event=event, parent=event)
            event_role.put()
        # TODO(AttackCowboy): populate form from json--Steal from
        # populate with test data
        self.response.write(utils.CreateJsonFromModel(event))


def PrintPersonEventRoles(event_key):
    """Prints all PersonEventRoles associated with event_key.

    Useful for debugging.
    """
    person_event_roles = models.PersonEventRole.gql(
        "WHERE event = KEY(:1)", event_key)

    roles_and_counts = collections.defaultdict(int)
    for per in person_event_roles:
        roles_and_counts[per.role.role_type] += 1
    print dict(roles_and_counts.items())


class RegisterPersonHandler(webapp2.RequestHandler):
    def __RegisterNewPersonInRole(self, person_key, event, role_key):
        """Registers a new person for an event with a given role."""

        person_role = models.PersonRole.gql(
            "WHERE person = KEY(:1) and role = KEY(:2)",
            person_key, role_key).get()
        if not person_role:
            raise exc.HTTPNotFound('Role with key %r not found' % role_key)

        # See if this person is already registered for this event.
        existing_registration = models.PersonEventRole.all().filter(
            "person = ", person_role.person).ancestor(person_role).get()
        if existing_registration:
            json_exception = exc.HTTPBadRequest()
            json_exception.content_type = 'text/plain'
            json_exception.text = (
                'This person (%s) is already registered for this '
                'event as a(n) %s') % (person_role.person.full_name,
                                         person_role.role.role_type)
            raise json_exception

        p = models.PersonEventRole(
            person=person_role.person, event=event, role=person_role.role,
            parent=person_role)
        p.put()

    def post(self):
        keys_json = json.loads(self.request.body)

        print 'Before registering new person'
        PrintPersonEventRoles(keys_json['eventKey'])

        person = models.OneOfUsPerson.get(keys_json['personKey'])
        if not person:
            raise exc.HTTPNotFound('Person not found')

        event = models.Event.get(keys_json['eventKey'])
        if not event:
            raise exc.HTTPNotFound('Event not found')

        print self.__RegisterNewPersonInRole(keys_json['personKey'], event,
                                             keys_json['roleKey'])

        print 'After registering new person'
        PrintPersonEventRoles(keys_json['eventKey'])

HANDLERS = [
    ('/api/event', EventHandler),
    ('/api/event/list', EventListHandler),
    ('/api/event/register_person', RegisterPersonHandler),
    ('/api/event/(.+)', EventHandler),
]
