import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # Redirect to the event picker, which lets a trained operator
        # register people for events.
        self.redirect('/static/html/index.html')
