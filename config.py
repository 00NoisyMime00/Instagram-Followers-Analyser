from getpass import getpass
import json
import os.path
from os import path

if path.exists('user.json') == False:
    with open('user.json', 'w') as f:
        details = {}
        details['id'] = ""
        details['password'] = ""
        json.dump(details, f)


with open('user.json', 'r') as f:
    details = json.loads(f.read())
    id = details['id']
    password = details['password']
    

def change():
    id = input('Enter you instagram handle : ')
    password = getpass()

    details={}
    details['id'] = id
    details['password'] = password

    with open('user.json', 'w') as f:
        json.dump(details, f)

    with open('followersList.json', 'w') as f:
        json.dump([], f)