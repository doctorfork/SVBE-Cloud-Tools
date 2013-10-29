import datetime
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.ext import search

class Contact(polymodel.PolyModel):
    """Any contact, person or business, with the organization"""
    phone_number = db.PhoneNumberProperty()
    address = db.PostalAddressProperty()

class Person(Contact):
    """Any person that comes into contact with the organization"""
    full_name = db.StringProperty(required=True)
    @property
    def last_name(self):
        return self.full_name.split(' ')[-1]
    email = db.EmailProperty()
    birthday = db.DateProperty()
    mobile_number = db.PhoneNumberProperty()
    @property 
    def age(self):
        return int((datetime.date.today() - self.birthday).days / 365.2425)
    def is_youth(self):
        return self.age < 18

class OneOfUsPerson(search.SearchableModel, Person):
    """a person having a relationship with the organization.
    properties include a start date, and qualifications
    could be a volunteer, staff person, director, officer etc.
    """
    responsible_adult = db.ReferenceProperty(Person,
        collection_name='responsible_adults')
    emergency_contact = db.ReferenceProperty(Person,
        collection_name='emergency_contacts')                                             
    # independent refers to youth with permission to work independently
    independent = db.BooleanProperty()
    volunteer_hours = db.IntegerProperty()
    volunteer_points = db.IntegerProperty()
    
    @classmethod
    def SearchableProperties(cls):
        return [['full_name', 'email'], search.ALL_PROPERTIES]
    
    def ToDict(self):
        return dict([(p, getattr(self, p)) for p in self.properties()] +
                    [('key', str(self.key()))])
  
class Event(polymodel.PolyModel):
    """Any event the organization runs or participates in"""
    event_title = db.StringProperty()
    start_time = db.DateTimeProperty()
    stop_time = db.DateTimeProperty()
    setup_time = db.DateTimeProperty()
    address = db.PostalAddressProperty()
    event_leader = db.ReferenceProperty(Person)
   
    @property
    def date(self):
        return self.start_time.date()
        
    def ToDict(self):
        return dict([(p, getattr(self, p)) for p in self.properties()] +
                    [('key', str(self.key()))])

    def ToDictWithRoles(self):
        dict_without_roles = self.ToDict()
        dict_without_roles['roles'] = self.eventrole_set.get().ToDict()
        return dict_without_roles
                     
    #do we want a length/duration property?


class Role(db.Model):
    role_type = db.StringProperty(required=True)
    role_brief_description = db.StringProperty()
    role_info_URL = db.LinkProperty()
    
    def ToDict(self):
        return dict([(p, getattr(self, p)) for p in self.properties()] +
                    [('key', str(self.key()))])
    
class EventRole(db.Model):
    """role and number of people needed to fill that role for an Event
    """
    role = db.ReferenceProperty(Role)
    role_num = db.IntegerProperty()
    event = db.ReferenceProperty(Event)
    
    def ToDict(self):
        return dict([(p, getattr(self, p)) for p in self.properties()] +
                    [('key', str(self.key()))])

class PersonRole(db.Model):
    """A person's role within the organization"""
    person = db.ReferenceProperty(Contact, collection_name='roles',required=True)
    role = db.ReferenceProperty(Role, collection_name='doers',required=True)
    start_date = db.DateTimeProperty()
    active = db.BooleanProperty()

class PersonEventRole(db.Model):
    """Attendence model, stores Person, Event they attended,
	 and their Role at the event."""
    person = db.ReferenceProperty(OneOfUsPerson, required = True,
                                  collection_name = 'event_role')
    event = db.ReferenceProperty(Event, required = True, 
                                 collection_name = 'person_roll')
    #is role required?
    role = db.ReferenceProperty(Role, required = True,
                                collection_name = 'person_event')

                                
class Business(Contact):
    """For a later stage of developement"""

    name = db.StringProperty(required=True)
    contact_person = db.ReferenceProperty(Person,
        collection_name='contacts_for_business' )
    alt_contact_person = db.ReferenceProperty(Person,
        collection_name='alt_contacts_for_business')
    main_number = db.PhoneNumberProperty()


class DonationIn(db.Model):
    """For a later stage of developement"""
    date = db.DateProperty()
    donor = db.ReferenceProperty(Contact, collection_name='donors')
    intake = db.ReferenceProperty(OneOfUsPerson, collection_name='intake_people')
    # I'd like to make a less - SVBE specific rendering of this design intent
    bikes = db.ListProperty(item_type=db.Key)
    cash = db.FloatProperty()
    other = db.ListProperty(item_type=db.Key)

class DonationOut(db.Model):
    """For a later stage of developement"""
    date = db.DateProperty()
    recipient = db.ReferenceProperty(Contact)
    bikes = db.ListProperty(item_type=db.Key)    

class Sku(db.Model):
    """For a later stage of developement"""
    pass   

class Purchase(db.Model):
    """For a later stage of developement"""
    date = db.DateProperty()
    buyer = db.ReferenceProperty(Contact, collection_name='buyers')
    sku = db.ReferenceProperty(Sku)
    amount = db.FloatProperty()
    seller = db.ReferenceProperty(Contact, collection_name='sellers')

class Bike(db.Model):
    """For a later stage of developement"""
    description = db.StringProperty()
    seq_number = db.IntegerProperty()
    est_start_value = db.FloatProperty()
    est_final_value = db.FloatProperty()
    wheel_size = db.StringProperty()
    frame_size = db.FloatProperty()
    color = db.StringProperty()
    gender = db.StringProperty()
