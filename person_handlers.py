"""Handlers for HTTP methods involving Person objects."""

# Class has no __init__ method (no-init)
# pylint: disable=W0232
#
# Instance of 'EventListHandler' has no 'response' member (no-member)
# pylint: disable=E1101
#
# Too few public methods (1/2) (too-few-public-methods)
# pylint: disable=R0903

import webapp2 # pylint: disable=F0401
import models
import json
import datetime
import utils
import re
from webob import exc
from google.appengine.ext import db # pylint: disable=F0401

class GetPersonListHandler(webapp2.RequestHandler):
    def get(self):
        """Returns all the people in data store"""
        self.response.content_type = 'application/json'
        self.response.write(
            utils.CreateJsonFromModel(
                [person for person in models.Person.all()]))


class GetPersonByNameAndEmailHandler(webapp2.RequestHandler):
    def get(self, token):
        """Returns a list of all people whose name or email contains token."""
        query = models.OneOfUsPerson.all().search(
            token, properties=['full_name', 'email'])
        self.response.content_type = 'application/json'
        self.response.write(utils.CreateJsonFromModel(
            [person for person in query.run()]))


class GetPersonByIdHandler(webapp2.RequestHandler):
    def get(self, person_id):
        """Returns a Person given an ID."""
        try:
            person = models.OneOfUsPerson.get(person_id)
        except db.BadKeyError:
            raise exc.HTTPNotFound('No person found with id ' + person_id)
        self.response.content_type = 'application/json'
        self.response.write(utils.CreateJsonFromModel(person))

    def delete(self, person_key):
        """Attempts to delete the Person with the given key."""
        if not person_key:
            response = exc.HTTPBadRequest()
            response.content_type = 'text/plain'
            response.text = u'No key provided to delete.'
            raise response

        person = models.OneOfUsPerson.get(person_key)
        if not person:
            response = exc.HTTPBadRequest()
            response.content_type = 'text/plain'
            response.text = u'No person found with key ' + person_key
            raise response

        # Temporary "sample" delete functionality.
        person.full_name = 'DELETED'
        person.put()
        self.response.write(utils.CreateJsonFromModel(person))

PHONE_PATTERN = re.compile(r'^(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}$')
EMAIL_PATTERN = re.compile(r'^[^@]+@[^@]+[.][^@]+$')


def IsValidPhone(phone):
    return PHONE_PATTERN.match(phone) is not None


def IsValidEmail(email):
    return EMAIL_PATTERN.match(email) is not None

def _UpdateRoles(person, new_roles):
    """Bring the existing PersonRoles for person in line with new_roles.

    All roles not appearing in new_roles get marked as inactive if
    they existed and weren't already inactive. Conversely, roles
    in new_roles that aren't already represented as PersonRoles
    get created and marked as active.
    """
    print new_roles
    existing_roles = {
        r.role.role_type : r
        for r in models.PersonRole.all().filter('person = ', person)}
    new_roles = {role['roleType'] : role for role in new_roles}

    all_roles = set(existing_roles.keys()) | set(new_roles.keys())

    for role_type in all_roles:
        if role_type in new_roles:
            # Create or activate the role
            if role_type in existing_roles:
                existing_role = existing_roles[role_type]
                if not existing_role.active:
                    existing_role.active = True
                    existing_role.put()
                    print 'Activating role', role_type
                else:
                    print 'Role', role_type, 'is already active'
            else:
                # This is a new role. Make sure it makes sense.
                print 'Looking for role', role_type
                role = models.Role.all().filter('role_type = ', role_type).get()
                if not role:
                    raise ValueError(u'Invalid role name: %s' % role_type)

                person_role = models.PersonRole(
                    person=person, role=role,
                    active=True, parent=person)
                person_role.put()
                print 'Also saved a role for', role_type
        else:
            # This role was active for this user at one point, but
            # isn't anymore. If it's not already inactive, make it
            # so.
            existing_role = existing_roles[role_type]
            if existing_role.active:
                existing_role.active = False
                existing_role.put()
                print 'Role', role_type, 'marked as inactive'

def _GetPersonByEmail(email):
    return models.OneOfUsPerson.all().filter("email = ", email).get()

def SavePerson(person):
    def check_required_fields(person):
        # Check required fields.
        for field_name in ['fullName', 'birthday', 'roles', 'email']:
            if not field_name in person:
                raise ValueError(u'Missing required field ' + field_name)

    def check_valid_email(email):
        if not IsValidEmail(email):
            raise ValueError(u'Not a valid email address: %s' % email)

    def check_duplicate_email(p, email):
        # See if there's already a person with the same email.
        dup = _GetPersonByEmail(email)
        if dup and (not p.is_saved() or dup.key() != p.key()):
            raise ValueError(
                u"There's already a person with that email (%s)" % email)

    check_required_fields(person)
    check_valid_email(person['email'])

    if 'key' in person:
        p = models.OneOfUsPerson.get(person['key'])
        p.full_name = person['fullName']
        p.birthday = utils.ParseISODate(person['birthday']).date()
        p.email = person['email']
    else:
        p = models.OneOfUsPerson(
                full_name=person['fullName'],
                birthday=utils.ParseISODate(person['birthday']).date(),
                email=person['email'])

    check_duplicate_email(p, person['email'])

    # Populate optional fields, if the data is present.
    if person.get('phoneNumber'):
        # TODO(attackcowboy): Maybe validate?
        p.phone_number = person['phoneNumber']

    if person.get('address'):
        p.address = person['address']
    else:
        p.address = None

    if person.get('mobileNumber'):
        p.mobile_number = person['mobileNumber']

    p.put()
    _UpdateRoles(p, person['roles'])
    return p


class SavePersonHandler(webapp2.RequestHandler):
    def post(self):
        person = json.loads(self.request.body)
        try:
            p = SavePerson(person)
        except ValueError as e:
            response = exc.HTTPBadRequest()
            response.content_type = 'text/plain'
            response.text = e.args[0]
            raise response
        self.response.write(utils.CreateJsonFromModel(p))

HANDLERS = [
    ('/api/person/list', GetPersonListHandler),
    ('/api/person', SavePersonHandler),
    ('/api/person/by_name/(.+)', GetPersonByNameAndEmailHandler),
    ('/api/person/(.+)', GetPersonByIdHandler),
]
