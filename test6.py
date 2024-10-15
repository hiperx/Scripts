#
# Scheck open port
#

#!/usr/bin/env python
import socket

ip = '100.100.10.11'
port_list = [20, 80, 8080, 139, 445, 23, 21, 22]

for port in port_list:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((ip, port))

    if result == 0:
        print('-' * 60)
        print('Port: ', port, 'open')
        print('-' * 60)
    else:
        print('Port: ', port, 'closed')





