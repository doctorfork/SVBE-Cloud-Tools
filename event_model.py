import datetime
from google.appengine.ext import db

class Event(db.Model):
	category = db.StringProperty()
	location = db.PostalAddresProperty()
	start_time = db.DateTimeProperty()
	end_time = db.DateTimeProperty()
	setup_time = db.DateTimeProperty()
	leader = db.ReferenceProperty()
	volunteer_group = db.ReferenceProperty()
	
	@property
	def date(self):
		return self.start_time.date()
		
		
		
'''Class method:
def notify_leader(self):
	leader = Person.get(self.leader)
	email = Person.email
'''