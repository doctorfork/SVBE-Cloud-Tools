import datetime
from google.appengine.ext import db

class Person(db.Model):
    name = db.StringProperty()
    email = db.EmailProperty()
    start_date = db.DateProperty(auto_now_add=True)
    birthday = db.DateProperty()
    address = db.PostalAddressProperty()
    phone_number = db.PhoneNumberProperty()
    
    @property 
    def age(self):
        return int((datetime.date.today() - self.birthday).days / 365.2425)
    


#p = Person(key_name = 'foof')
#p.name = "Dave Nielsen"
#p.birthday = datetime.date(1988,11,12)
#p.put()

#p = Person.get_by_key_name('foof')
#p = Person.get(db.Key.from_path(u'Person', 'foof', _app=u'dev~active-bird-256'))
#p.email = 'fake@notreal.com'
#p.put()
#pprint.pprint(db.to_dict(p))
