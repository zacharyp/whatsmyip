#!/usr/bin/python

import httplib
import ConfigParser
import os
import boto.ses

def send_email(old, new):
    conf = ConfigParser.ConfigParser()
    conf.read(os.path.expanduser('~') + "/.currentip.config")
    addr = conf.get("email","address")
    conn = boto.ses.connect_to_region('us-east-1')
    conn.send_email(
         addr,
         '[Updated IP Address]',
         'old ip: %s, new ip: %s' % (old, new,),
         [addr]
    )

def stored_ip(update=None):
    with open(os.path.expanduser('~') + "/.currentip.txt", "r+") as f:
        if update:
            f.seek(0)
            f.write(update)
            f.truncate()
        else:
            content = f.readlines()
            return content[0].strip()

def main():
    old_ip = stored_ip()
    h1 = httplib.HTTPConnection('ipecho.net')
    h1.request("GET", "/plain")
    current_ip = h1.getresponse().read().strip()
    if current_ip and old_ip != current_ip:
        send_email(old_ip, current_ip)
        stored_ip(update=current_ip)

if __name__ == "__main__":
   main()
