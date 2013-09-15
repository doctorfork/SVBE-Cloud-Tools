import webapp2
import models
import json
import datetime
import utils

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
        self.response.write(json.dumps(
            [self.__AddRolesToPersonDict(item) for item in query.run()], 
            cls=utils.CustomJsonEncoder))


class PersonHandler(webapp2.RequestHandler):
    def __GetPersonByEmail(self, email):
        return models.OneOfUsPerson.all().filter("email = ", email).get()
    
    def post(self):
        person_json = json.loads(self.request.body)
        
        # See if there's already a person with the same email.
        if self.__GetPersonByEmail(person_json['email']):
            response = exc.HTTPBadRequest()
            response.content_type = 'text/plain'
            response.text = (
                "There's already a person with that email (%s)" % 
                    person_json['email'])
            raise response
        
        # Create the new Person.
        p = models.OneOfUsPerson(
            phone_number=person_json['phoneNumber'],
            address=person_json['address'],
            full_name=person_json['fullName'],
            birthday=datetime.date(
                year=int(person_json['birthdayYear']),
                month=int(person_json['birthdayMonth']),
                day=int(person_json['birthdayDay'])),
            email=person_json['email'],
            mobile_number=person_json['mobileNumber'])
        p.put()
        self.response.write('Saved a new person named %s' % p.full_name)
        
        for role_name in person_json['roles']:
            print 'Looking for role', role_name
            role = models.Role.get_by_key_name(role_name)
            person_role = models.PersonRole(person=p, role=role)
            person_role.put()
            print 'Also saved a role for', role_name

