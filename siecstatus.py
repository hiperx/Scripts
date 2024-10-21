#
# Testowanie polaczenia w sieci domowej e4net
#

#!/usr/bin/env python
import os
with open('ip-source.txt') as file:
    dump = file.read()
    dump = dump.splitlines()

    for ip in dump:

        os.system('clear')
        print('Pinging now:', ip)
        print('-' * 60)
        os.system('ping -c 5 {}'.format(ip))
        print('-' * 60)
        time.sleep(5)


        