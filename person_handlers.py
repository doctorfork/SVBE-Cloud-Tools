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
        person_role.role.role_type : person_role
        for person_role in models.PersonRole.all().filter('person = ', person)}
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

def SavePerson(person_json):
    """Saves the given person, or raises a ValueError."""

    # Check required fields.
    for field_name in ['fullName', 'birthday', 'roles', 'email']:
        if not field_name in person_json:
            raise ValueError(u'Missing required field ' + field_name)

    # Check if the given email is valid.
    if not IsValidEmail(person_json['email']):
        raise ValueError(u'Not a valid email address: %s' %
                         person_json['email'])

    if 'key' in person_json:
        person = models.OneOfUsPerson.get(person_json['key'])
        person.full_name = person_json['fullName']
        person.birthday = utils.ParseISODate(person_json['birthday']).date()
        person.email = person_json['email']
    else:
        person = models.OneOfUsPerson(
                full_name=person_json['fullName'],
                birthday=utils.ParseISODate(person_json['birthday']).date(),
                email=person_json['email'])

    # See if there's already a person with the same email.
    dup = _GetPersonByEmail(person_json['email'])
    if dup and (not person.is_saved() or dup.key() != person.key()):
        raise ValueError(
            u"There's already a person with that email (%s)" %
            person_json['email'])

    # Populate optional fields, if the data is present.
    if person_json.get('phoneNumber'):
        # TODO(attackcowboy): Maybe validate?
        person.phone_number = person_json['phoneNumber']

    if person_json.get('address'):
        person.address = person_json['address']
    else:
        person.address = None

    if person_json.get('mobileNumber'):
        person.mobile_number = person_json['mobileNumber']

    person.put()
    _UpdateRoles(person, person_json['roles'])
    return person


class SavePersonHandler(webapp2.RequestHandler):
    def post(self):
        """Attempts to edit an existing person, or create a new one.

        If the 'key' field is present in the given JSON, attempts to edit
        the person with that key; otherwise, creates a new person. If a key
        is given but no person exists with that key, throws a ValueError."""

        person = json.loads(self.request.body)
        try:
            person = SavePerson(person)
        except ValueError as ex:
            response = exc.HTTPBadRequest()
            response.content_type = 'text/plain'
            response.text = ex.args[0]
            raise response
        self.response.write(utils.CreateJsonFromModel(person))

HANDLERS = [
    ('/api/person/list', GetPersonListHandler),
    ('/api/person', SavePersonHandler),
    ('/api/person/by_name/(.+)', GetPersonByNameAndEmailHandler),
    ('/api/person/(.+)', GetPersonByIdHandler),
]
