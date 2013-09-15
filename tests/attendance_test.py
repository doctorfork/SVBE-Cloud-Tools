class AttendenceTest(webapp2.RequestHandler):
    def get(self):
        leader = models.OneOfUsPerson.get_or_insert('poof',full_name = "Alfred E. Newman")
        leader.put()
        event = models.Event.get_or_insert('roof',date = datetime.date(2013,7,14),
                                            event_leader = leader)
        event.put()
        assist_role = models.Role.get_or_insert('Assistant',role_type = 'Assistant')
        assist_role.put()

        person_at_event_doing_role = models.PersonEventRole(person = leader, event = event,
                                                            role = assist_role)
        person_at_event_doing_role.put()
        self.response.write(db.to_dict(person_at_event_doing_role))
