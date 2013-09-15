import event_handler
import event_role_handler
import person_event_role_handler
import person_handlers

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/OneOfUsPersonTest', person_handlers.OneOfUsPersonTest),
    ('/AttendenceTest', AttendenceTest),
    ('/LoadRoles', LoadRoles),
    ('/api/event', event_handler.EventHandler),
    ('/api/event/list', event_handler.EventListHandler),
    ('/api/event/register_person', event_handler.RegisterPersonHandler),
    ('/api/event/(.+)', event_handler.EventHandler),
    ('/api/person/list', person_handlers.GetPersonList),
    ('/api/person', person_handlers.PersonHandler),
    ('/api/person/by_name/(.+)', person_handlers.GetPersonByPartialName),
    ('/api/roles/get', GetRoles),
    ('/api/event_roles/get_by_event/(.+)', 
     event_role_handler.GetEventRolesByEventHandler),
    ('/api/person_event_roles/get_by_event/(.+)',
     person_event_role_handler.GetPersonEventRolesByEventHandler),
    ], debug=True)
    