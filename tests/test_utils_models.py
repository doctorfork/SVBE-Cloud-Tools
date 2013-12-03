import models

def createPerson(full_name='John Smith', email='fake@notreal.com', **kwargs):
    return models.Person(full_name=full_name, email=email, **kwargs)
