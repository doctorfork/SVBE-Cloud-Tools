import functools
import models
import datetime

def _Create(model_type, **kwargs):
    return getattr(models,model_type)(**kwargs)

person_args = {'full_name':'John Smith', 'email':'fake@notreal.com','birthday':datetime.date.today()}    

    
createPerson = functools.partial(_Create,'Person',**person_args) 
    
createOneOfUsPerson = functools.partial(_Create,'OneOfUsPerson',**person_args) 
    