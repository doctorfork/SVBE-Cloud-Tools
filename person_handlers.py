import webapp2
import models
import json
import datetime
import utils
import re
from webob import exc

class GetPersonListHandler(webapp2.RequestHandler):
    def get(self):
        """Returns all the people in data store"""
        self.response.content_type = 'application/json'
        self.response.write(
            utils.CreateJsonFromModel(
                [p for p in models.Person.all()]))


class GetPersonByNameAndEmailHandler(webapp2.RequestHandler):
    def get(self, token):
        """Returns a list of all people whose name or eamil contains token."""
        query = models.OneOfUsPerson.all().search(
            token, properties=['full_name', 'email'])
        self.response.content_type = 'application/json'
        self.response.write(utils.CreateJsonFromModel(
          [p for p in query.run()]))


class GetPersonByIdHandler(webapp2.RequestHandler):
  def get(self, person_id):
      try:
          p = models.OneOfUsPerson.get(person_id)
      except db.BadKeyError:
          raise exc.HTTPNotFound('No person found with id ' + person_id)
      self.response.content_type = 'application/json'
      self.response.write(utils.CreateJsonFromModel(p))
      
  def delete(self, person_key):
      if not person_key:
          response = exc.HTTPBadRequest()
          response.content_type = 'text/plain'
          response.text = (
                u"There's already a person with that email (%s)" % 
                    person_json['email'])
          raise response
            
      p = models.OneOfUsPerson.get(person_key)
      if not p:
          response = exc.HTTPBadRequest()
          response.content_type = 'text/plain'
          response.text = (
              u"There's already a person with that email (%s)" % 
                  person_json['email'])
          raise response
          
      # Temporary "sample" delete functionality.
      p.full_name = 'DELETED'
      p.put()
      self.response.write(utils.CreateJsonFromModel(p))

PHONE_PATTERN = re.compile(r'^(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}$')
EMAIL_PATTERN = re.compile(r'^[^@]+@[^@]+[.][^@]+$')


def IsValidPhone(phone):
  return PHONE_PATTERN.match(phone) is not None


def IsValidEmail(email):
  return EMAIL_PATTERN.match(email) is not None


class SavePersonHandler(webapp2.RequestHandler):
    def __GetPersonByEmail(self, email):
        return models.OneOfUsPerson.all().filter("email = ", email).get()

    def __UpdateRoles(self, person, new_roles):
        """Bring the existing PersonRoles for person in line with new_roles.

        All roles not appearing in new_roles get marked as inactive if
        they existed and weren't already inactive. Conversely, roles
        in new_roles that aren't already represented as PersonRoles
        get created and marked as active.
        """
        existing_roles = {
            r.role.role_type : r
            for r in models.PersonRole.all().filter('person = ', person)}
        new_roles = {role['role']['roleType'] : role for role in new_roles}

        all_roles = set(existing_roles.keys()) | set(new_roles.keys())

        for role_type in all_roles:
            if role_type in new_roles:
                # Create or activate the role
                if role_type in existing_roles:
                    existing_role = existing_roles[role_type]
                    if existing_role.active != new_roles[role_type]['active']:
                        existing_role.active = new_roles[role_type]['active']
                        existing_role.put()
                        print 'Updating role', role_type, 'to have',
                        print existing_role.active
                    else:
                        print 'Role', role_type, 'has correct activation'
                else:
                    # This is a new role. Make sure it makes sense.
                    print 'Looking for role', role_type
                    role = models.Role.all().filter(
                        'role_type = ', role_type).get()
                    if not role:
                        response = exc.HTTPBadRequest()
                        response.content_type = 'text/plain'
                        response.text = u'Invalid role name: %s' % role_type
                        raise response

                    if new_roles[role_type]['active']:
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
                    print  'Role', role_type, 'marked as inactive'


    def post(self):
        person_json = json.loads(self.request.body)

        # Check required fields.
        for field_name in ['fullName', 'birthday', 'roles', 'email']:
          if not field_name in person_json:
            response = exc.HTTPBadRequest()
            response.content_type = 'text/plain'
            response.text = u'Missing required field ' + field_name
            raise response

        if not IsValidEmail(person_json['email']):
          response = exc.HTTPBadRequest()
          response.content_type = 'text/plain'
          response.text = u'Not a valid email address: %s' % (
              person_json['email'])
          raise response

        if 'key' in person_json:
            p = models.OneOfUsPerson.get(person_json['key'])
            p.full_name = person_json['fullName']
            p.birthday = utils.ParseISODate(person_json['birthday']).date()
        else:
            p = models.OneOfUsPerson(
                full_name=person_json['fullName'],
                birthday=utils.ParseISODate(person_json['birthday']).date())
        
        # See if there's already a person with the same email.
        dup = self.__GetPersonByEmail(person_json['email'])
        if dup and (not p.is_saved() or dup.key() != p.key()):
            response = exc.HTTPBadRequest()
            response.content_type = 'text/plain'
            response.text = (
                u"There's already a person with that email (%s)" % 
                    person_json['email'])
            raise response
            
        
        # Populate optional fields, if the data is present.
        if 'phoneNumber' in person_json:
          p.phone_number = person_json['phoneNumber']
        
        if 'address' in person_json:
          p.address = person_json['address'] 
        
        if 'email' in person_json:
          p.email = person_json['email']
          
        if 'mobileNumber' in person_json:
          p.mobile_number = person_json['mobileNumber']
        
        p.put()
        self.__UpdateRoles(p, person_json['roles'])
        self.response.write(utils.CreateJsonFromModel(p))
