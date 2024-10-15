#!/usr/bin/python

# -----------------------------------------------------------------------*
# Read file and ping host from file - Piotr Kulesza 
# -----------------------------------------------------------------------*

import csv
import os
import argparse
from termcolor import colored


def read_hosts(csv_filename):
    
    # read file in
    host_list = []
    with open(csv_filename, 'r') as  f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == "name":
                pass
            else:
                host_list.append(row)
    return host_list
    

def is_host_alive(host_item):

    ping_response = os.system("ping -c 3 " + host_item[1] + " > /dev/null 2>&1")
    is_alive = False
    if ping_response == 0:
        is_alive = True
    return is_alive


# --------------------------------------------------------*
# Main
# --------------------------------------------------------*


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Pings host from SCV file")
    parser.add_argument("-f", metavar="FILENAME", dest="csv_filename", required=True, help="Input CSV file containig hosts to ping")

    args = parser.parse_args()

    # CSV filename
    filename = args.csv_filename

    # list of hosts 
    host_list = read_hosts(filename)

    #print(host_list)
    
    os.system('clear')
    for item in host_list:
        print('-'  * 60)
        print("Pinging {}...".format(item[0]))
        
        alive = is_host_alive(item)
        if alive:
            print colored("\n{}".format(item[0]), "green") + (" is alive")
            print('-'  * 60)
        else:
            print colored("\n{}".format(item[0]), "red") + (" is not alive")
            print('-'  * 60)

            

