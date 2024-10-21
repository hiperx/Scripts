# *-------------------------------------------------------------------*
# Autocut console connection scripy by Piotr Kulesza (company) - Python
# *-------------------------------------------------------------------*

import json,requests
import pexpect
import sys

#from pexpect import pxssh

#-|              |--------------------------------------------------------------*

request = requests.get("https://network-console.site.xxx/console-port-db/readonly-api.cgi?method=search&keywords=poz1", verify=False)
#request_text = request.text

#-|              |--------------------------------------------------------------*

data = json.loads(request.text)
#data_out = json.dump(data, open('data.json', "w"))

#-|              |--------------------------------------------------------------*


for dev in data:
        print('Server_Name: ' + dev['Server_Name'])
        print('Server_Port: ' + dev['Server_Port'])
        print('Host_Name: ' + dev['Host_Name'])

"""
sn = dev['Server_Name']
p = dev['Server_Port']
hn = dev['Host_Name']
"""

sn = dev['Server_Name']
p = '44'
hn = 'device-switch-sw1'


u = 'user'
pa = 'password'

print(sn)
print(hn)
print(p)

print(u)
print(pa)



sshAP = pexpect.spawn('ssh %s -c aes256-cbc -l %s:%s' % (sn,hn,p))
#sshAP.logfile = sys.stdout.buffer



