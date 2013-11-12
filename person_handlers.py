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
            json.dumps([p.ToDict() for p in models.Person.all()]))


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

PHONE_PATTERN = re.compile(r'^(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}$')
EMAIL_PATTERN = re.compile(r'^[^@]+@[^@]+[.][^@]+$')


def IsValidPhone(phone):
  return PHONE_PATTERN.match(phone) is not None


def IsValidEmail(email):
  return EMAIL_PATTERN.match(email) is not None


class CreatePersonHandler(webapp2.RequestHandler):
    def __GetPersonByEmail(self, email):
        return models.OneOfUsPerson.all().filter("email = ", email).get()

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
          response.text = u'Not a valid email address: %s' % person_json['email']
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
        if dup and dup.key() != p.key():
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
        self.response.write('Saved person named %s' % p.full_name)
        
        # Also save the person's roles, if any were provided.
        for role_name in person_json['roles']:
            print 'Looking for role', role_name
            role = models.Role.all().filter('role_type = ', role_name).get()
            if not role:
              response = exc.HTTPBadRequest()
              response.content_type = 'text/plain'
              response.text = u'Invalid role name: %s' % role_name
              raise response
              
            person_role = models.PersonRole(person=p, role=role, parent=p)
            person_role.put()
            print 'Also saved a role for', role_name

