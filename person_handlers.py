import webapp2
import models
import json
import datetime
import utils

class GetPersonList(webapp2.RequestHandler):
    def get(self):
        """Returns all the people in data store"""
        self.response.write(
            json.dumps([p.ToDict() for p in models.Person.all()]))


class GetPersonByPartialName(webapp2.RequestHandler):
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
        self.response.write(json.dumps(
            [self.__AddRolesToPersonDict(item) for item in query.run()], 
            cls=utils.CustomJsonEncoder))


class PersonHandler(webapp2.RequestHandler): 
    def post(self):
        print self.request.body
        person_json = json.loads(self.request.body)
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
        
class PersonTest(webapp2.RequestHandler):
    def get(self):
        p = models.Person(key_name = 'foof',full_name = "Dave Nielsen")
        p.full_name = "Dave Fork"
        p.birthday = datetime.date(1988,11,12)
        p.put()

        p = models.Person.get_by_key_name('foof')
        p.email = 'fake@notreal.com'
        p.put()
        pprint.pprint(db.to_dict(p))


class OneOfUsPersonTest(webapp2.RequestHandler):
    def get(self):
        ooup = models.OneOfUsPerson(key_name='poof',full_name = "Alfred E. Newman")
        ooup.put()
        last_name_test =  ooup.last_name == "Newman"
        if last_name_test:
            self.response.write('Passed: last name test')
        else:
            self.response.write('Failed: last name test')
        # PersonRole test
        # r = models.Role.get_by_key_name('Delivery')
        r = models.Role(key_name='Delivery',role_type='Delivery')
        r.put()
        p_r = models.PersonRole(key_name=r.role_type+"_"+ooup.last_name, person=ooup,role=r)
        p_r.put()
        # p_r_test = models.PersonRole.get_by_key_name

        ooup.email = 'fake1@notreal.com'
        ooup.birthday = datetime.date(1988,11,12)
        ooup.address = db.PostalAddress('1600 Ampitheater Pkwy., Mountain View, CA')

