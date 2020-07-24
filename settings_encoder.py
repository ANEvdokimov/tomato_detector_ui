import json
from json import JSONEncoder
from settings import Settings


class SettingsEncoder(JSONEncoder):
    def default(self, object):
        if isinstance(object, Settings):
            return object.__dict__

        else:
            return json.JSONEncoder.default(self, object)
