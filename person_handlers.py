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


class GetPersonByPartialNameHandler(webapp2.RequestHandler):
    def __AddRolesToPersonDict(self, person):
        """Returns the dict form of the given person, with its roles added."""
        dict_form = person.ToDict()
        dict_form['roles'] = [
            {'role_type': person_role.role.role_type, 
             'key': str(person_role.role.key())}
            for person_role in person.roles]
        return dict_form
            
    def get(self, prefix):
        """Returns a list of all people whose names begin with prefix."""
        query = models.OneOfUsPerson.all().search(
            prefix, properties=['full_name'])
        self.response.content_type = 'application/json'
        self.response.write(utils.CreateJsonFromModel([p for p in query.run()]))

class GetPersonByIdHandler(webapp2.RequestHandler):
  def get(self, person_id):
      try:
          p = models.OneOfUsPerson.get(person_id)
      except db.BadKeyError:
          raise exc.HTTPNotFound('No person found with id ' + person_id)
      self.response.content_type = 'application/json'
      self.response.write(utils.CreateJsonFromModel(p))


class CreatePersonHandler(webapp2.RequestHandler):
    def __GetPersonByEmail(self, email):
        return models.OneOfUsPerson.all().filter("email = ", email).get()
    
    def __IsValidEmail(self, email):
      email_regexp = re.compile(r'[^@]+@[^@]+[.][^@]+')
      return re.match(email_regexp, email) is not None
    
    def post(self):
        person_json = json.loads(self.request.body)
        
        if 'email' not in person_json or not self.__IsValidEmail(person_json['email']):
          response = exc.HTTPBadRequest()
          response.content_type = 'text/plain'
          if 'email' not in person_json:
            response.text = u'You must provide an email address'
          else:
            response.text = u'Not a valid email address: %s' % person_json['email']
          raise response
        
        # See if there's already a person with the same email.
        if self.__GetPersonByEmail(person_json['email']):
            response = exc.HTTPBadRequest()
            response.content_type = 'text/plain'
            response.text = (
                u"There's already a person with that email (%s)" % 
                    person_json['email'])
            raise response
            
        # Check other required fields.
        for field_name in ['fullName', 'birthday', 'roles']:
          if not field_name in person_json:
            response = exc.HTTPBadRequest()
            response.content_type = 'text/plain'
            response.text = u'Missing required field ' + field_name
            raise response
        
        birthday = utils.ParseISODate(person_json['birthday']).date()
                    
        # Create the new Person.
        p = models.OneOfUsPerson(
            full_name=person_json['fullName'],
            birthday=birthday)
        
        # Populate optional fields, if the data is present.
        if 'phoneNumber' in person_json:
          p.phone_number=person_json['phoneNumber']
        
        if 'address' in person_json:
          p.address=person_json['address'] 
        
        if 'email' in person_json:
          p.email=person_json['email']
          
        if 'mobileNumber' in person_json:
          p.mobile_number=person_json['mobileNumber']
        
        p.put()
        self.response.write('Saved a new person named %s' % p.full_name)
        
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

