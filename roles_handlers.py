import webapp2
import models

class GetRoles(webapp2.RequestHandler):
    def get(self):
        """Returns all the valid roles."""
        self.response.write(json.dumps([r.role_type for r in models.Role.all()]))

               
class LoadRoles(webapp2.RequestHandler):
    def get(self):
        # Role Names to put into datastore:
        role_names = [
            "Accountant",
            "Announcements",
            "Apprentice",
            "Cleaning",
            "Course Instructor",
            "Delivery",
            "Director",
            "Event Leader",
            "Event Setup",
            "Event Wrapup",
            "Food Coordinator",
            "Homework Mechanic",
            "Intake",
            "Inventory",
            "Mechanic",
            "Mentor",
            "Officer",
            "Orientation",
            "Outgoing Donations",
            "Photographer",
            "Prequal",
            "President",
            "Record Keeper",
            "Recycling",
            "Registration",
            "Sales",
            "Secretary",
            "Treasurer",
            "Volunteer Coordinator",]
        for r in role_names:
            role = models.Role(key_name=r,role_type=r)
            role.put()
            self.response.write('Added role: %s <br/>' % r)
        self.response.write('Roles Loaded.<br/>')
