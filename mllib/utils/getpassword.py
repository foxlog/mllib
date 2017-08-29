import json
from pprint import pprint
import os
from os.path import expanduser
home = expanduser("~")

"""
#json
#password
"""
def get_key_value(k, k2):
    with open(os.path.join(home, 'config/' 'info.json')) as data_file:
        data = json.load(data_file)
        return data.get(k).get(k2)

