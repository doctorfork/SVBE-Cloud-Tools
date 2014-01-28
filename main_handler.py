"""Handler for the / (root path of the application)."""

import webapp2  # pylint: disable=F0401

# Class has no __init__ method (no-init)
# pylint: disable=W0232
# Too few public methods (1/2) (too-few-public-methods)
# pylint: disable=R0903
# Instance of 'MainHandler' has no 'redirect' member (no-member)
# pylint: disable=E1101

class MainHandler(webapp2.RequestHandler):
    def get(self):
        """Shows the 'main menu' for the application."""
        self.redirect('/static/html/index.html')
