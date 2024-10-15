# Run #python phone-tool-data.py -l username


#!/usr/bin/python3
import sys
import os
import json
import csv
import requests
import argparse
import getpass
from pprint import pprint
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse_args(args):

  parser = argparse.ArgumentParser(
    description='Get job history for user'
  )

  parser.add_argument(
    '-l',
    '--login',
    help='Username of person to search data for',
    required=True
  )

  return parser.parse_args(args)

def get_user_data(s, login):
  url = 'https://phonesite.company.xxx/users/%s.json' % login
  r = s.get(url, allow_redirects=True, verify=False)

  try:
    data = json.loads(r.content.decode('utf-8'))
  except json.decoder.JSONDecodeError:
    if "This request requires HTTP authentication." in r.content.decode('utf-8'):
      print("Authentication failed. Try running: mwinit -s")
      exit(False)
    elif "Company Access" in r.content.decode('utf-8'):
      print("Authentication failed. You might not be connected to corp.")
      exit(False)
    else:
      print("Unknown error from PhoneTool")
      print("----------------------------")
      print(r.content.decode('utf-8'))
      exit(False)
  except:
    print("Something went wrong")
    print("----------------------------")
    print(r.content.decode('utf-8'))
    exit(False)

  print()
  print('------------------------')
  print('%s %s' % (data["first_name"], data["last_name"]))
  print('%s %s' % (data["job_title"], data["department_name"]))
  print()
  print('Email        : %s' % (data["email"]))
  print('Pager Email  : %s' % (data["pager_email"]))
  print('------------------------')
  print('Location     : %s' % (data["building"]))
  print('               %s' % (data["building_room"]))
  print('------------------------')
  print('Desk Phone   : %s' % (data["office_number"]))
  print('Phone Number : %s' % (data["phone_number"]))
  print('Pager Number : %s' % (data["pager_number"]))
  print('------------------------')
  print('Level        : %s' % (data["job_level"]))
  print('Hire Date    : %s' % (data["hire_date_iso"]))
  print('Tenure Days  : %s' % (data["tenure_days"]))
  print('Tenure       : %s' % (data["total_tenure_formatted"]))
  print('Badge Type   : %s' % (data["badge_type"]))

def oldfart(s, login):
  url = 'https://corp.company.xxx/u/%s/rank' % login
  r = s.get(url, verify=False)

  data = json.loads(r.content.decode('utf-8'))
  rank = int(data['global']['rank'])
  total = int(data['global']['total'])
  behind = total - rank
  percent_ahead = '%.2f' % (rank/total*100)
  percent_behind = '%.2f' % (behind/total*100)

  print('------------------------')
  print('Worldwide summary: %s ( %s%% ) < %s > ( %s%% ) %s'
    % (rank, percent_ahead, login, percent_behind, behind)
  )

def main(args):

  args = parse_args(args)

  #start a requests session
  s = requests.Session()

  # Need to grab cookies from Midway,need to run `mwinit -s` first
  cookiefile = os.path.join(os.path.expanduser("~"), ".midway", "cookie")

  with open(cookiefile) as cf:
    reader = list(csv.reader(cf, delimiter='\t'))
    for row in reader:
      if len(row) > 2:
        if '#HttpOnly_' in row[0]:
          dom = row[0].split('_')[1]
        else:
          dom = row[0]

        sec = False
        if 'TRUE' in row[3]:
          sec = True

        required_args = {
          'name': row[5],
          'value': row[6],
        }
        optional_args = {
          'domain': dom,
          'path': row[2],
          'secure': sec,
          'expires': row[4],
          'discard': False,
        }
        new_cookie = requests.cookies.create_cookie(**required_args,**optional_args)
        s.cookies.set_cookie(new_cookie)

  get_user_data(s, args.login)
  

if __name__ == "__main__":
  main(sys.argv[1:])