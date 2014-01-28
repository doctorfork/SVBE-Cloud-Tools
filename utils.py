""" Utility functions and classes. """

import json
import datetime
import models
import re
from google.appengine.ext import db # pylint: disable=F0401

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj): # pylint: disable=E0202
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%dT00:00:00Z")
        elif isinstance(obj, models.Event):
            obj_dict = db.to_dict(obj)
            obj_dict['key'] = obj.key()
            obj_dict['roles'] = {
                evt_role.role.role_type: evt_role.role_num
                for evt_role in obj.eventrole_set.ancestor(obj).run()}
            obj_dict = ConvertDictKeysToCamelCase(obj_dict)
            return obj_dict
        elif isinstance(obj, models.Person):
            obj_dict = db.to_dict(obj)
            obj_dict['key'] = obj.key()
            obj_dict['roles'] = [
                evt_role.role for evt_role in obj.roles.ancestor(obj).run()
                if evt_role.active]
            obj_dict = ConvertDictKeysToCamelCase(obj_dict)
            return obj_dict
        elif isinstance(obj, db.Model):
            obj_dict = db.to_dict(obj)
            obj_dict = ConvertDictKeysToCamelCase(obj_dict)
            obj_dict['key'] = obj.key()

            return obj_dict
        elif isinstance(obj, db.Key):
            return str(obj)
        else:
            return super(CustomJsonEncoder, self).default(obj)


def CreateJsonFromModel(model):#TODO(AttackCowboy):refactor function name
    return json.dumps(model, cls=CustomJsonEncoder)


def ParseISODate(date_string):
    """Parses the string form of a date, in ISO 8601 format. Returns a datetime.

    ISO 8601 dates look like '2013-08-14T02:15:38.204Z'
    """
    return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")


def ConvertDictKeysToCamelCase(dict_with_underscores):
    """Converts a dictionary's string keys to CamelCase."""

    map_result = {}
    for key, val in dict_with_underscores.iteritems():
        if isinstance(val, dict):
            val = ConvertDictKeysToCamelCase(val)
        map_result[re.sub(r'_(\w)', _ConvertStringToCamelCase, key)] = val
    return map_result

def _ConvertStringToCamelCase(match):
    return match.group(1).upper()
