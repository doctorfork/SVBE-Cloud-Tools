import datetime
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class Contact(polymodel.PolyModel):
   phone_number = db.PhoneNumberProperty()
   address = db.PostalAddressProperty()

class Person(Contact):
    full_name = db.StringProperty(required=True)
    @property
    def last_name(self):
        return self.full_name.split(' ')[-1]
    email = db.EmailProperty()
    birthday = db.DateProperty()
    address = db.PostalAddressProperty()
    mobile_number = db.PhoneNumberProperty()
    @property 
    def age(self):
        return int((datetime.date.today() - self.birthday).days / 365.2425)
    
class OneOfUsPerson(Person):
    """a person having a working relationship with the organization.
    properties include a unique ID, a start date, and qualifications
    """
    def is_youth(self)
        return self.age < 18
    start_date = db.DateProperty(auto_now_add=True)
    active = db.BooleanProperty()
    independent = db.BooleanProperty()
    # roles link to the role class
    roles = db.ListProperty(item_type=db.Key)
    events = db.ListProperty()
    volunteer_hours = db.IntegerProperty()
    volunteer_points = db.IntegerProperty()
    @property
    def start_year(self):
        return self.start_date.year
    
class BusinessContact(Contact):
    name = db.StringProperty(required=True)
    contact_person = db.ReferenceProperty(Person)
    main_number = db.PhoneNumberProperty()

class Event(polymodel.PolyModel):
    date = db.DateProperty()
    start_time = db.TimeProperty()
    stop_time = db.TimeProperty()
    address = db.PostalAddressProperty()
    event_leader = db.ReferenceProperty(Person)
    # the roles may need to be a list of [role, num_needed, [participants] [waitlist] [removed]]
    event_roles = db.ListProperty()

class DonationIn(db.Model):
    date = db.DateProperty()
    donor = db.ReferenceProperty(Contact)
    # list of each bike by serial #, description & est. value
    # I'd like to make a less - SVBE specific rendering of this design intent
    bikes = db.ListProperty()
    cash = db.FloatProperty()
    other = db.ListProperty()

class Purchase(db.Model):
    date = db.DateProperty()
    buyer = db.ReferenceProperty(Contact)
    sku = db.ReferenceProperty(sku)
    amount = db.FloatProperty()
    seller = db.ReferenceProperty(Contact)

class Bike(db.Model):
    pass

class sku(db.Model):
    pass

class Role(db.Model):
    role_type = db.CategoryProperty()

class PersonEvent(db.Model):
    person = db.ReferenceProperty(OneOfUsPerson, required = True, collection_name = 'events')
    event = db.ReferenceProperty(Event, required = True, collection_name = 'people')
    title = db.StringProperty()         

p = Person(key_name = 'foof',
           name='Dave Nielsen')
#p.name = "Dave Nielsen"
#p.birthday = datetime.date(1988,11,12)
#p.put()

#p = Person.get_by_key_name('foof')
#p = Person.get(db.Key.from_path(u'Person', 'foof', _app=u'dev~active-bird-256'))
#p.email = 'fake@notreal.com'
#p.put()
#pprint.pprint(db.to_dict(p))
