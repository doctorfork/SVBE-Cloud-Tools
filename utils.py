import json
import datetime

class CustomJsonEncoder(json.JSONEncoder):
     def default(self, obj):
         if isinstance(obj, datetime.datetime):
             return obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
         return json.JSONEncoder.default(self, obj)
