import datetime
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

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

class OneOfUsPerson(Person):
    """a person having a relationship with the organization.
    properties include a start date, and qualifications
    could be a volunteer, staff person, director, officer etc.
    """
    responsible_adult = db.ReferenceProperty(Person,
        collection_name='responsible adults')
    # each new role added may need its own start date
    start_date = db.DateProperty(auto_now_add=True)
    # the active switch may be necessary for each role
    active = db.BooleanProperty()
    # independent refers to youth with permission to work independently
    independent = db.BooleanProperty()
    # roles link to the role class
    roles = db.StringListProperty()
    volunteer_hours = db.IntegerProperty()
    volunteer_points = db.IntegerProperty()
    @property
    def start_year(self):
        return self.start_date.year

    
class BusinessContact(Contact):
    name = db.StringProperty(required=True)
    contact_person = db.ReferenceProperty(Person,
        collection_name='contacts_for_business' )
    alt_contact_person = db.ReferenceProperty(Person,
        collection_name='alt_contacts_for_business')
    main_number = db.PhoneNumberProperty()

class Event(polymodel.PolyModel):
    # How does this classify multi-day events?
    # can we use DateTimeProperty for start_time and end_time
    # with date being an @property of start_time?
    # also should we have an event title?
    date = db.DateProperty()
    start_time = db.TimeProperty()
    stop_time = db.TimeProperty()
    address = db.PostalAddressProperty()
    event_leader = db.ReferenceProperty(Person)
    # event_roles is a list of type EventRole
    # isn't this the same as the eventroll_set property created by the reference property in EventRoll?
    # if so how do I access it because it didn't show up in my test
    event_roles = db.ListProperty(item_type=db.Key)

class DonationIn(db.Model):
    date = db.DateProperty()
    donor = db.ReferenceProperty(Contact, collection_name='donors')
    intake = db.ReferenceProperty(OneOfUsPerson, collection_name='intake_people')
    # I'd like to make a less - SVBE specific rendering of this design intent
    bikes = db.ListProperty(item_type=db.Key)
    cash = db.FloatProperty()
    other = db.ListProperty(item_type=db.Key)

class DonationOut(db.Model):
    date = db.DateProperty()
    recipient = db.ReferenceProperty(Contact)
    bikes = db.ListProperty(item_type=db.Key)    

class Sku(db.Model):
    pass   

class Purchase(db.Model):
    date = db.DateProperty()
    buyer = db.ReferenceProperty(Contact, collection_name = 'buyers')
    sku = db.ReferenceProperty(Sku)
    amount = db.FloatProperty()
    seller = db.ReferenceProperty(Contact, collection_name = 'sellers')

class Bike(db.Model):
    description = db.StringProperty()
    seq_number = db.IntegerProperty()
    est_value = db.FloatProperty()
    
class Role(db.Model):
    role_type = db.StringProperty()
    role_brief_description = db.StringProperty()
    rold_info_URL = db.LinkProperty()
    
class EventRole(db.Model):
    """role and number of people needed to fill that role for an event
    """
    role = db.ReferenceProperty(Role)
    role_num = db.IntegerProperty()
    event = db.ReferenceProperty(Event)

class PersonEvent(db.Model):
    person = db.ReferenceProperty(OneOfUsPerson, required = True,
                                  collection_name = 'events')
    #do we still need event if we track event_roll?
    event = db.ReferenceProperty(Event, required = True, collection_name = 'people')
    event_roles = db.ListProperty(item_type = db.Key)
    event_hours = db.IntegerProperty()

class PersonRole(db.Model):
    person = db.ReferenceProperty(OneOfUsPerson, required = True)
    role = db.ReferenceProperty(Role, required = True)
    start_date = db.DateTimeProperty(auto_now_add=True)
    active = db.BooleanProperty(default=True)
    
#Role Names to put into datastore:
##	"Assistant",
##        "Delivery",
##        "Director",
##        "Event Leader",
##        "Event Setup",
##        "Event Wrapup",
##        "Food Coordinator",
##        "Homework Mechanic",
##        "Intake",
##        "Inventory",
##        "Mechanic",
##        "Mentor",
##        "Officer",
##        "Orientation",
##        "Outgoing Donations",
##        "Photographer",
##        "Prequal",
##        "President",
##        "Record Keeper",
##        "Recycling",
##        "Registration",
##        "Sales",
##        "Secretary",
##        "Volunteer Coordinator",
