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

def GetSVBEApp():
    """Returns the SVBE WSGI application."""

    return webapp2.WSGIApplication([
        ('/', main_handler.MainHandler),
        ('/LoadRoles', roles_handlers.LoadRoles),
        ('/api/event', event_handler.EventHandler),
        ('/api/event/list', event_handler.EventListHandler),
        ('/api/event/register_person', event_handler.RegisterPersonHandler),
        ('/api/event/(.+)', event_handler.EventHandler),
        ('/api/person/list', person_handlers.GetPersonListHandler),
        ('/api/person', person_handlers.SavePersonHandler),
        ('/api/person/by_name/(.+)',
         person_handlers.GetPersonByNameAndEmailHandler),
        ('/api/person/(.+)', person_handlers.GetPersonByIdHandler),
        ('/api/roles/get', roles_handlers.GetRoleTypes),
        ('/api/event_roles/get_by_event/(.+)',
         event_role_handler.GetEventRolesByEventHandler),
        ('/api/person_event_roles/get_summary_by_event/(.+)',
         person_event_role_handler.GetPersonEventRolesSummaryByEventHandler),
        ('/api/person_event_roles/get_by_event/(.+)',
         person_event_role_handler.GetPersonEventRolesByEventHandler),
        ('/api/person_event_roles/remove/(.+)',
         person_event_role_handler.RemovePersonEventRoleHandler)
        ], debug=True)
