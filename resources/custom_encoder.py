from decimal import Decimal
import json

#Converts the Decimal instances to float
class CustomEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,Decimal):
            return float(obj)
        return json.JSONEncoder.default(self,obj)