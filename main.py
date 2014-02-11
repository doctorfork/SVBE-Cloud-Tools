"""Main entry point for the application"""

# Disable the invalid-name checker, which would otherwise complain
# about 'app'.
# pylint: disable=C0103

import app_definition

app = app_definition.GetSVBEApp()
