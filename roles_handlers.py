"""HTTP handlers for Role objects."""

# Class has no __init__ method (no-init)
# pylint: disable=W0232
#
# Instance of 'EventListHandler' has no 'response' member (no-member)
# pylint: disable=E1101
#
# Too few public methods (1/2) (too-few-public-methods)
# pylint: disable=R0903

import webapp2 # pylint: disable=F0401
import models
import json

class GetRoleTypes(webapp2.RequestHandler):
    def get(self):
        """Returns all the valid roles."""
        self.response.content_type = 'application/json'
        self.response.write(json.dumps(
            [role.role_type for role in models.Role.all()]))


class LoadRoles(webapp2.RequestHandler):
    def get(self):
        """Initialized the database with the names of all valid roles."""
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
            "Volunteer Coordinator"]
        for name in role_names:
            role = models.Role(key_name=name, role_type=name)
            role.put()
            self.response.write('Added role: %s <br/>' % name)
        self.response.write('Roles Loaded.<br/>')
