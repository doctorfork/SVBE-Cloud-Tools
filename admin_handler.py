import models
import csv

def UploadPeople(request):
    for row in csv.DictReader(request.POST['file'].file):
        print row

handlers = [
    ('/admin/person/upload', UploadPeople),
#    ('/admin/event/upload', UploadEvents),
]