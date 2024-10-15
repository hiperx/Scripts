#!/usr/bin/python3
import json

class User:
        def __init__(self, Server_Name, Server_Port, Host_Name, conid):
                self.Server_Name = Server_Name
                self.Server_Port = Server_Port
                self.Host_Name = Host_Name
                self.conid = conid
        
        @classmethod
        def from_json(cls, json_string):
                json_dict = json.loads(json_string)
                return cls(**json_dict)
        
        def __repr__(self):
                return f'{ self.Host_Name }'

json_string = '''{
      "Server_Name" : "device-con-r1",
      "Server_Port" : "44",
      "Host_Name" : "device-switch-sw1",
      "conid" : "396103"
   }'''

user = User.from_json(json_string)
print(user)

users_list = []
i = 0
while i < len(users_list):
        print(users_list[i])
        i += 1




