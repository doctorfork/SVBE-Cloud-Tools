import json
import datetime
import models
import re
from google.appengine.ext import db

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%dT00:00:00Z")
        elif isinstance(obj, models.Event):
            d = db.to_dict(obj)
            d['key'] = obj.key()
            d['roles'] = {er.role.role_type: er.role_num for er in obj.eventrole_set.ancestor(obj).run()}
            d = ConvertDictKeysToCamelCase(d)
            return d
        elif isinstance(obj, models.Person):
            d = db.to_dict(obj)
            d['key'] = obj.key()
            d['roles'] = [er.role for er in obj.roles.ancestor(obj).run()]
            d = ConvertDictKeysToCamelCase(d)
            return d
        elif isinstance(obj, db.Model):
            d = db.to_dict(obj)
            d = ConvertDictKeysToCamelCase(d)
            d['key'] = obj.key()
            
            return d
        elif isinstance(obj, db.Key):
            return str(obj)
        else:
            return super(CustomJsonEncoder, self).default(obj)

            
def CreateJsonFromModel(model):#TODO(AttackCowboy):refactor function name
    return(json.dumps(model, cls = CustomJsonEncoder))


def ParseISODate(date_string):
    """Parses the string form of a date, in ISO 8601 format. Returns a datetime.
    
    ISO 8601 dates look like '2013-08-14T02:15:38.204Z'
    """
    return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")

    
def ConvertDictKeysToCamelCase(map):
    map_result = {}
    for key,val in map.iteritems():
        if isinstance(val,dict):
            val = ConvertDictKeysToCamelCase(val)
        map_result[re.sub(r'_(\w)', _CovertStringToCamelCase, key)] = val
    return map_result
        
def _CovertStringToCamelCase(match):
    return match.group(1).upper()
