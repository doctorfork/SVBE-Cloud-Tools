import webapp2

import event_handler
import event_role_handler
import person_event_role_handler
import person_handlers
import main_handler
import roles_handlers

def GetSVBEApp():
    return webapp2.WSGIApplication([
        ('/', main_handler.MainHandler),
        ('/LoadRoles', roles_handlers.LoadRoles),
        ('/api/event', event_handler.EventHandler),
        ('/api/event/list', event_handler.EventListHandler),
        ('/api/event/register_person', event_handler.RegisterPersonHandler),
        ('/api/event/(.+)', event_handler.EventHandler),
        ('/api/person/list', person_handlers.GetPersonListHandler),
        ('/api/person', person_handlers.PersonHandler),
        ('/api/person/by_name/(.+)', person_handlers.GetPersonByPartialNameHandler),
        ('/api/roles/get', roles_handlers.GetRoles),
        ('/api/event_roles/get_by_event/(.+)', 
         event_role_handler.GetEventRolesByEventHandler),
        ('/api/person_event_roles/get_by_event/(.+)',
         person_event_role_handler.GetPersonEventRolesByEventHandler),
        ], debug=True)
