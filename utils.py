import json
import datetime
from google.appengine.ext import db

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%dT00:00:00Z")
        elif isinstance(obj, db.Model):
            d = db.to_dict(obj)
            d['key'] = str(obj.key())#TODO(AttackCowboy):Handle key separately?
            return d
        else:
            return super(CustomJsonEncoder, self).default(obj)
        
def CreateJsonFromModel(model):#TODO(AttackCowboy):refactor function name
	return(json.dumps(model, cls = CustomJsonEncoder))
