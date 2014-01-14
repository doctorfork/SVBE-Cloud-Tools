"""Definition for the entire SVBE app.

Lists all the handler paths and their classes."""

# F0401:  9,0: Unable to import 'webapp2'
# pylint: disable=F0401
import webapp2

import event_handler
import event_role_handler
import person_event_role_handler
import person_handlers
import main_handler
import roles_handlers
import admin_handler

def GetSVBEApp():
    """Returns the SVBE WSGI application."""

    return webapp2.WSGIApplication([
        ('/', main_handler.MainHandler),
        ('/LoadRoles', roles_handlers.LoadRoles),
        ('/api/roles/get', roles_handlers.GetRoleTypes),
        ('/api/event_roles/get_by_event/(.+)',
         event_role_handler.GetEventRolesByEventHandler),
        ] +
        event_handler.handlers +
        person_handlers.handlers +
        person_event_role_handler.handlers +
        admin_handler.handlers, debug=True)
