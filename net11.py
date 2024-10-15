#!/usr/bin/env python

"""
Script requires python 3.8 and netmiko lib.
"""
print("COMPANY server room  data collection " )

from netmiko import Netmiko
from getpass import getpass
getpassword=getpass()
device_list =("company-wlc-1",
              "company-wlc-2",
              "company-agg-r1",
              "company-agg-r2",
              "company-edg-fw",
              "company-acc-v1",
              "company-acc-v2"

)

for i in device_list:
        
    net_connect = Netmiko(
        i,
        username="user",
        password=getpassword,
        secret=getpassword,
        device_type="cisco_xe",
    )
    if "wlc" in i:
        net_connect.enable()
        commands = ("show cdp neighbors",
                    "show ap summary",
                    "sh int sum" 
                    )
        for command in commands:
            output = net_connect.send_command(command)
            print(output)
            with open("log.txt", 'a') as f:
                print(net_connect.find_prompt(),command,  file=f)
                print(output, file=f)
                print(" ", file=f)
                print(" ", file=f)
                print(" ", file=f)
            
            
    if "dis" in i or "acc" and not 'v1' and not 'v2' in i:
        net_connect.enable()
        commands = ("show version | be Switch Ports Model",
                    "show switch detail",
                    "show int status",
                    "show interfaces trunk",
                    "show spanning-tree vlan 700",
                    "show vlan brief",
                    "show ip interface brief",
                    "show cdp neighbor",
                    "show authentication sessions"
                    )
        for command in commands:
            output = net_connect.send_command(command)
            print(output)
            with open("log.txt", 'a') as f:
                print(net_connect.find_prompt(),command, file=f)
                print(output, file=f)
                print(" ", file=f)
                print(" ", file=f)
                print(" ", file=f)
    if "agg" in i:
        commands = ("show processes cpu history",
                    "show processes cpu | i Core 0|Core 1",
                    "sh processes memory sorted",
                    "sh process cpu sort 5sec | ex 0.00 +0.00 +0.00",
                    "show int | i line|packets/sec",
                    "show int status | exclude disabled|notconnect",
                    "show etherchannel summary",
                    "show cdp neighbors",
                    "show standby brief",
                    "show ip ospf neighbor",
                    "show ip bgp all summary",
                    "show int status | include err",
                    "sh int desc | i acc-sw",
                    "sh int desc | i dis-sw"
                    )
        for command in commands:
            output = net_connect.send_command(command)
            print(output)
            with open("log.txt", 'a') as f:
                print(net_connect.find_prompt(),command, file=f)
                print(output, file=f)
                print(" ", file=f)
                print(" ", file=f)
                print(" ", file=f)
    if "v1"  in  i or "v2" in i:
        net_connect.enable()
        commands  = ("show run | include boot",
                     "show ip bgp summary",
                     "show ip ospf neighbor",
                     "show ip interface brief",
                     "show version | include register",
                     "ping vrf  LEIA 1.1.1.1",
                     "ping 1.1.1.1 source  GigabitEthernet0/0/2",
                     )
        for command in commands:
            output = net_connect.send_command(command)
            print(output)
            with open("log.txt", 'a') as f:
                print(net_connect.find_prompt(),command, file=f)
                print(output, file=f)
                print(" ", file=f)
                print(" ", file=f)
                print(" ", file=f)

    if "edg" in i:
        net_connect.enable()
        commands  = ("terminal pager 0",
                    "show failover state",
                     "show interface ip brief",
                     "show conn all",
                    )
        for command in commands:
            output = net_connect.send_command(command)
            print(output)
            with open("log.txt", 'a') as f:
                print(net_connect.find_prompt(),command, file=f)
                print(output, file=f)
                print(" ", file=f)
                print(" ", file=f)
                print(" ", file=f)

net_connect.disconnect()
    
            
    
    




