import models
import csv
import person_handlers

def UploadPeople(request):
  """Bulk saves a CSV of Person records to the Datastore.

  A form POST to this handler should contain a file in the field "file".
  There should be a header row with the field names matching the JSON properties.
  The "roles" field, however, should simply be a pipe ("|") separated list of
  role types to be saved with the Person.

  Example:
  phoneNumber,address,fullName,email,birthday,mobileNumber,roles
  1234,123 Main,Stan Fakerton,stan@fake.com,2014-01-14T03:31:15.138Z,5678,"Apprentice,Sales"

  Args:
    request: A webapp2 request object.
  """
  for row in csv.DictReader(request.POST['file'].file):
    # Reformat roles from CSV string:
    row['roles'] = [{'roleType': role.strip()} for role in row['roles'].split(',')]
    try:
      person_handlers.SavePerson(row)
    except ValueError as e:
      print e.args[0]

HANDLERS = [
    ('/admin/person/upload', UploadPeople),
#    ('/admin/event/upload', UploadEvents),
]
